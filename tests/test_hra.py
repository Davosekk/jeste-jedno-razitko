"""Kontroly pravidel a kolizí; neotvírají herní okno."""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import unittest
import pygame
from pribeh import novy_stav, proved
from main import posun_hrace, nejblizsi_predmet, PREKAZKY, rozlozeni_dialogu


class TestPribehu(unittest.TestCase):
    def setUp(self):
        self.stav = novy_stav()

    def test_cely_ukol(self):
        proved("sebrat", self.stav)
        proved("vyplnit", self.stav)
        konec = proved("odevzdat", self.stav)
        self.assertEqual(self.stav["formular"], 3)
        self.assertEqual(konec["nadpis"], "První úkol hotový!")

    def test_zadost_bez_formulare(self):
        self.assertEqual(proved("odevzdat", self.stav)["nadpis"], "Něco chybí")
        self.assertEqual(self.stav["formular"], 0)

    def test_prazdna_zadost_se_neztrati(self):
        proved("sebrat", self.stav)
        self.assertEqual(proved("odevzdat", self.stav)["nadpis"], "Vráceno k doplnění")
        self.assertEqual(self.stav["formular"], 1)

    def test_spatny_formular(self):
        proved("spatny", self.stav)
        self.assertEqual(self.stav["formular"], 0)

    def test_opakovane_sebrani_nevrati_stav(self):
        proved("sebrat", self.stav)
        proved("vyplnit", self.stav)
        proved("sebrat", self.stav)
        self.assertEqual(self.stav["formular"], 2)

    def test_vyplneni_bez_formulare(self):
        proved("vyplnit", self.stav)
        self.assertEqual(self.stav["formular"], 0)

    def test_opakovane_odevzdani(self):
        self.stav["formular"] = 3
        proved("odevzdat", self.stav)
        self.assertEqual(self.stav["formular"], 3)

    def test_novy_stav_je_nezavisly(self):
        proved("sebrat", self.stav)
        self.assertEqual(novy_stav(), {"formular": 0})

    def test_vsechny_dialogove_vetve(self):
        # Každé tlačítko musí odkazovat na existující akci.
        pygame.font.init()
        akce = ["uvod", "pauza", "novy_zacatek", "urednice", "napoveda", "nastenka",
                "formulare", "spatny", "sebrat", "stolek", "vyplnit", "odevzdat"]
        for formular in range(4):
            for nazev in akce:
                dialog = proved(nazev, {"formular": formular})
                panel, radky, tlacitka = rozlozeni_dialogu(dialog)
                self.assertGreaterEqual(panel.top, 0)
                self.assertLessEqual(panel.bottom, 720)
                for tlacitko in tlacitka:
                    self.assertTrue(panel.contains(tlacitko))
                for popisek, cil in dialog["moznosti"]:
                    self.assertTrue(popisek)
                    if cil not in ("restart", "konec"):
                        proved(cil, {"formular": formular})


class TestPohybu(unittest.TestCase):
    def test_stani(self):
        bod = pygame.Vector2(576, 440)
        self.assertEqual(posun_hrace(bod, pygame.Vector2(0, 0), 0.02), bod)

    def test_stejna_rychlost_sikmo(self):
        bod = pygame.Vector2(576, 440)
        rovne = posun_hrace(bod, pygame.Vector2(1, 0), 0.02)
        sikmo = posun_hrace(bod, pygame.Vector2(1, 1), 0.02)
        self.assertAlmostEqual(bod.distance_to(rovne), bod.distance_to(sikmo))

    def test_zed(self):
        bod = pygame.Vector2(90, 400)
        for _ in range(100):
            bod = posun_hrace(bod, pygame.Vector2(-1, 0), 0.016)
        self.assertGreaterEqual(bod.x, 75)

    def test_stul(self):
        bod = pygame.Vector2(204, 380)
        for _ in range(100):
            bod = posun_hrace(bod, pygame.Vector2(0, -1), 0.016)
        self.assertGreaterEqual(bod.y, 351)

    def test_limit_casu_pri_zaseku(self):
        bod = pygame.Vector2(576, 440)
        vysledek = posun_hrace(bod, pygame.Vector2(1, 0), 10)
        self.assertLessEqual(bod.distance_to(vysledek), 9.51)

    def test_interakce_z_dalky(self):
        self.assertIsNone(nejblizsi_predmet(pygame.Vector2(576, 532)))

    def test_interakce_zblizka(self):
        self.assertEqual(nejblizsi_predmet(pygame.Vector2(576, 360)), "urednice")

    def test_interakce_pres_prekazku(self):
        zed = pygame.Rect(550, 344, 50, 5)
        PREKAZKY.append(zed)
        try:
            self.assertIsNone(nejblizsi_predmet(pygame.Vector2(576, 370)))
        finally:
            PREKAZKY.remove(zed)





class TestMistnosti(unittest.TestCase):
    def test_postup_a_zamky(self):
        s = novy_stav()
        proved('archiv', s)
        proved('kancelar', s)
        proved('zaznam', s)
        proved('schvaleni', s)
        self.assertNotIn('mistnost', s)
        self.assertFalse(s.get('schvaleno'))
        for a in ['sebrat', 'vyplnit', 'odevzdat', 'archiv']:
            proved(a, s)
        self.assertEqual(s['mistnost'], 'archiv')
        proved('spatny_zaznam', s)
        self.assertFalse(s.get('zaznam'))
        for a in ['cerveny', 'modry', 'zeleny', 'cerveny']:
            proved(a, s)
        proved('zaznam', s)
        proved('recepce', s)
        proved('kancelar', s)
        self.assertEqual(s['mistnost'], 'kancelar')
        for a in ['platba', 'evidence', 'pecet', 'podpis']:
            proved(a, s)
        proved('schvaleni', s)
        proved('schvaleni', s)
        self.assertTrue(s['schvaleno'])
        proved('recepce', s)
        self.assertTrue(s['zaznam'])
        self.assertEqual(novy_stav(), {'formular': 0})

    def test_pruchodnost_vsech_interakci(self):
        # Prohledání skutečně průchozí plochy: každý předmět musí jít oslovit.
        from collections import deque
        from main import telo, PREDMETY, START
        from mistnosti import aktivni_mapa
        for mistnost, mriz in [('recepce', False), ('archiv', False), ('archiv', True), ('kancelar', True)]:
            prekazky, predmety = aktivni_mapa({'formular': 3, 'mistnost': mistnost, 'mriz': mriz}, PREKAZKY, PREDMETY)
            fronta = deque([START])
            navstiveno = {START}
            nalezeno = set()
            while fronta:
                x, y = fronta.popleft()
                bod = pygame.Vector2(x, y)
                nalezeno.add(nejblizsi_predmet(bod, predmety, prekazky))
                for dx, dy in [(8,0),(-8,0),(0,8),(0,-8)]:
                    dalsi = (x+dx, y+dy)
                    if dalsi in navstiveno or not (60 < dalsi[0] < 1090 and 190 < dalsi[1] < 585):
                        continue
                    if not any(telo(pygame.Vector2(dalsi)).colliderect(r) for r in prekazky):
                        navstiveno.add(dalsi)
                        fronta.append(dalsi)
            cil = set(predmety)
            if mistnost == 'archiv' and not mriz:
                cil.remove('kartoteka')
                cil.remove('rozpis')
                self.assertNotIn('rozpis', nalezeno)
                self.assertNotIn('kartoteka', nalezeno)
            self.assertTrue(cil <= nalezeno, (mistnost, cil-nalezeno))

    def test_nove_dialogy_se_vejdou(self):
        pygame.font.init()
        for mistnost in ['recepce', 'archiv', 'kancelar']:
            for formular in range(4):
                for zaznam in [False, True]:
                    for akce in ['archiv','recepce','kancelar','kartoteka','spatny_zaznam','zaznam','schvaleni']:
                        s = {'formular': formular, 'mistnost': mistnost, 'zaznam': zaznam}
                        d = proved(akce, s)
                        if d:
                            panel, _, tlacitka = rozlozeni_dialogu(d)
                            self.assertGreaterEqual(panel.top, 0)
                            self.assertLessEqual(panel.bottom, 720)
                            self.assertTrue(all(panel.contains(t) for t in tlacitka))


if __name__ == "__main__":
    unittest.main()
