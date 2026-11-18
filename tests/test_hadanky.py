"""Hádanky musí být řešitelné i po chybě, návratu a opakované interakci."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
import unittest
from itertools import product
import pygame
from pribeh import proved, novy_stav, HADANKY, SPINACE, STANOVISTE
from main import rozlozeni_dialogu


class TestHadanek(unittest.TestCase):
    def test_vsechna_poradi_spinacu(self):
        # Jen jediná ze všech 81 čtyřkrokových kombinací smí otevřít mříž.
        for poradi in product(['cerveny', 'modry', 'zeleny'], repeat=4):
            s = {'formular': 3, 'mistnost': 'archiv'}
            for a in poradi:
                proved(a, s)
            self.assertEqual(bool(s.get('mriz')), list(poradi) == SPINACE)

    def test_chyba_a_navrat_neztrati_dokument(self):
        s = {'formular': 3, 'mistnost': 'archiv'}
        proved('zaznam', s)
        self.assertFalse(s.get('zaznam'))
        for a in ['cerveny', 'zeleny']:
            proved(a, s)
        self.assertEqual(s['spinace'], 0)
        for a in SPINACE:
            proved(a, s)
        proved('zaznam', s)
        for a in ['recepce', 'archiv', 'modry']:
            proved(a, s)
        self.assertTrue(s['mriz'])
        self.assertTrue(s['zaznam'])
        self.assertEqual(s['spinace'], 4)

    def test_poplatek_a_kontrola(self):
        s = {'formular': 3, 'mistnost': 'kancelar', 'zaznam': True}
        proved('evidence', s)
        proved('schvaleni', s)
        self.assertFalse(s.get('kontrola'))
        self.assertFalse(s.get('schvaleno'))
        proved('spatna_platba', s)
        self.assertFalse(s.get('uctenka'))
        proved('platba', s)
        for a in ['evidence', 'podpis']:
            proved(a, s)
        self.assertEqual(s['stanoviste'], 0)
        self.assertTrue(s['uctenka'])
        for a in STANOVISTE + ['schvaleni', 'pecet', 'platba', 'schvaleni']:
            proved(a, s)
        self.assertTrue(s['schvaleno'])
        self.assertEqual(s['stanoviste'], 3)
        self.assertEqual(novy_stav(), {'formular': 0})

    def test_akce_mimo_mistnost_nezmeni_stav(self):
        for akce in HADANKY:
            s = {'formular': 3, 'mistnost': 'recepce'}
            proved(akce, s)
            self.assertEqual(s, {'formular': 3, 'mistnost': 'recepce'})

    def test_dialogy_a_odkazy(self):
        pygame.font.init()
        for mistnost in ['archiv', 'kancelar']:
            for uctenka in [False, True]:
                for krok in range(4):
                    for akce in HADANKY:
                        s = {'formular': 3, 'mistnost': mistnost, 'zaznam': True,
                             'uctenka': uctenka, 'spinace': krok, 'stanoviste': min(krok, 2)}
                        d = proved(akce, s)
                        panel, _, tlacitka = rozlozeni_dialogu(d)
                        self.assertGreaterEqual(panel.top, 0)
                        self.assertLessEqual(panel.bottom, 720)
                        self.assertTrue(all(panel.contains(t) for t in tlacitka))
                        for _, cil in d['moznosti']:
                            proved(cil, s.copy())
