"""Oba konce přes skutečné herní akce, ochrana postupu a restart v hlavní smyčce."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
import unittest
from unittest.mock import patch
import pygame
import main
from pribeh import proved, novy_stav, aktualni_ukol
from zavery import AKCE_ZAVERU


def cela_cesta():
    stav = novy_stav()
    for akce in ['sebrat','vyplnit','odevzdat','archiv','cerveny','modry','zeleny','cerveny',
                 'zaznam','recepce','kancelar','platba','evidence','pecet','podpis','schvaleni',
                 'spravce','recepce','skola','archiv','rozpis','recepce','kancelar',
                 'den_ct','cas_15','delka_120','odeslat_termin','recepce']:
        proved(akce, stav)
    return stav


class TestZaveru(unittest.TestCase):
    def test_obe_cesty_od_zacatku(self):
        for volba, konec in [('opravit_ucel','povoleno'), ('ponechat_ucel','zamitnuto')]:
            s = cela_cesta()
            d = proved('urednice', s)
            self.assertIn(volba, [a for _, a in d['moznosti']])
            d = proved(volba, s)
            self.assertFalse(s.get('zaver'))
            self.assertIn('potvrdit_zaver', [a for _, a in d['moznosti']])
            d = proved('potvrdit_zaver', s)
            self.assertEqual(s['zaver'], konec)
            self.assertEqual([a for _, a in d['moznosti']], ['restart','konec'])
            self.assertIn('povolen' if konec == 'povoleno' else 'zamítnuto', aktualni_ukol(s))

    def test_predcasny_konec_a_spatna_mistnost(self):
        hotovo = cela_cesta()
        for klic in ['formular','zaznam','uctenka','kontrola','schvaleno','termin']:
            s = hotovo.copy()
            s[klic] = 0
            puvodni = s.copy()
            for a in AKCE_ZAVERU:
                proved(a, s)
            self.assertEqual(s, puvodni)
        for mistnost in ['archiv','kancelar']:
            s = hotovo | {'mistnost': mistnost}
            for a in AKCE_ZAVERU:
                proved(a, s)
            self.assertNotIn('zaver', s)
        s = hotovo.copy()
        proved('potvrdit_zaver', s)
        self.assertNotIn('zaver', s)

    def test_zmena_rozhodnuti_a_zavreni(self):
        s = cela_cesta()
        proved('ponechat_ucel', s)
        self.assertIsNone(proved('zavrit', s))
        proved('urednice', s)
        self.assertNotIn('volba_zaveru', s)
        proved('opravit_ucel', s)
        proved('potvrdit_zaver', s)
        self.assertEqual(s['zaver'], 'povoleno')

    def test_konec_nejde_prepsat_ani_zavrit(self):
        for volba in ['opravit_ucel','ponechat_ucel']:
            s = cela_cesta()
            proved(volba, s)
            d = proved('potvrdit_zaver', s)
            puvodni = s.copy()
            for a in ['zavrit','pauza','urednice','recepce','archiv','kancelar','den_pa','sebrat',*AKCE_ZAVERU]:
                self.assertEqual(proved(a, s), d)
                self.assertEqual(s, puvodni)
            restart = proved('novy_zacatek', s)
            self.assertIn('restart', [a for _, a in restart['moznosti']])
            self.assertEqual(proved('zavrit', s), d)

    def test_dialogy_se_vejdou(self):
        pygame.font.init()
        s = cela_cesta()
        for a in ['urednice','opravit_ucel','zaver','ponechat_ucel','potvrdit_zaver','novy_zacatek','zavrit']:
            d = proved(a, s)
            panel, radky, tlacitka = main.rozlozeni_dialogu(d)
            self.assertGreaterEqual(panel.top, 0)
            self.assertLessEqual(panel.bottom, main.VYSKA)
            self.assertTrue(all(panel.contains(t) for t in tlacitka))
            self.assertLessEqual(pygame.font.Font(None,32).size(d['nadpis'])[0],620)
            for popisek, _ in d['moznosti']:
                self.assertLessEqual(pygame.font.Font(None,24).size(popisek)[0],590)

    def test_restart_klavesnici_v_hlavni_smycce_po_obou_koncich(self):
        # Skutečná smyčka: ESC neuzavře konec, R otevře potvrzení, šipka+Enter restartuje.
        for volba in ['opravit_ucel','ponechat_ucel']:
            s = cela_cesta()
            proved(volba, s)
            proved('potvrdit_zaver', s)
            stavy = []
            puvodni_mapa = main.aktivni_mapa
            def mapa(stav, prekazky, predmety):
                stavy.append(stav.copy())
                return puvodni_mapa(stav, prekazky, predmety)
            def klavesa(k):
                return pygame.event.Event(pygame.KEYDOWN, key=k)
            udalosti = [[klavesa(pygame.K_ESCAPE)], [klavesa(pygame.K_r)],
                        [klavesa(pygame.K_DOWN),klavesa(pygame.K_RETURN)],
                        [pygame.event.Event(pygame.QUIT)]]
            with patch.object(main,'novy_stav',side_effect=[s,novy_stav()]), \
                 patch.object(main,'aktivni_mapa',side_effect=mapa), \
                 patch.object(pygame.event,'get',side_effect=udalosti):
                main.main()
            self.assertEqual(stavy[-1], {'formular':0})
            self.assertTrue(any(stav.get('zaver') for stav in stavy))
