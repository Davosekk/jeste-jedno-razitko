"""Ověření nové rezervace, návaznosti a všech 27 návrhů."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
import unittest
from itertools import product
import pygame
from pribeh import proved, novy_stav
from rezervace import DNY, CASY, DELKY, PODKLADY, AKCE_REZERVACE, over_termin
from main import rozlozeni_dialogu


def priprav():
    s = {'formular': 3, 'mistnost': 'kancelar', 'schvaleno': True,
         'zaznam': True, 'uctenka': True, 'kontrola': True}
    for akce, (mistnost, _, _) in PODKLADY.items():
        s['mistnost'] = mistnost
        proved(akce, s)
    s['mistnost'] = 'kancelar'
    return s


class TestRezervace(unittest.TestCase):
    def test_jedine_reseni_ze_27(self):
        uspechy = []
        for den, cas, delka in product(DNY, CASY, DELKY):
            s = priprav()
            for a in [den, cas, delka, 'odeslat_termin']:
                proved(a, s)
            if s.get('termin'):
                uspechy.append((s['navrh_den'], s['navrh_cas'], s['navrh_delka']))
        self.assertEqual(uspechy, [('Čtvrtek', 15, 120)])

    def test_podklady_a_razitko_nelze_preskocit(self):
        s = novy_stav()
        for a in AKCE_REZERVACE:
            proved(a, s)
        self.assertEqual(s, novy_stav())
        for chybi in PODKLADY:
            s = priprav()
            s.pop('info_' + chybi)
            s.update(navrh_den='Čtvrtek', navrh_cas=15, navrh_delka=120)
            proved('odeslat_termin', s)
            self.assertFalse(s.get('termin'))
        s = priprav()
        s['mistnost'] = 'recepce'
        puvodni = s.copy()
        proved('den_ct', s)
        proved('odeslat_termin', s)
        self.assertEqual(s, puvodni)

    def test_oprava_navrat_a_restart(self):
        s = priprav()
        for a in ['den_ct', 'cas_16', 'delka_120', 'odeslat_termin']:
            proved(a, s)
        self.assertFalse(s.get('termin'))
        self.assertTrue(s['uctenka'] and s['kontrola'])
        for a in ['recepce', 'archiv', 'recepce', 'kancelar', 'den_ct', 'cas_15', 'delka_120', 'odeslat_termin']:
            proved(a, s)
        self.assertTrue(s['termin'])
        for a in ['den_pa', 'cas_14', 'delka_90', 'odeslat_termin']:
            proved(a, s)
        self.assertEqual((s['navrh_den'], s['navrh_cas'], s['navrh_delka']), ('Čtvrtek', 15, 120))
        self.assertEqual(novy_stav(), {'formular': 0})

    def test_neuplny_navrh(self):
        s = priprav()
        proved('odeslat_termin', s)
        self.assertFalse(s.get('termin'))
        self.assertTrue(over_termin(None, None, None))
        self.assertTrue(over_termin('Čtvrtek', 15, 90))
        self.assertFalse(over_termin('Čtvrtek', 15, 120))
        self.assertTrue(over_termin('Čtvrtek', 14, 120))
        self.assertTrue(over_termin('Čtvrtek', 16, 120))

    def test_vsechny_dialogy_a_tlacitka(self):
        pygame.font.init()
        for hotovo in [False, True]:
            for info in product([False, True], repeat=3):
                for a in AKCE_REZERVACE:
                    s = priprav()
                    s['termin'] = hotovo
                    s.update({'info_' + k: v for k, v in zip(PODKLADY, info)})
                    if a in PODKLADY:
                        s['mistnost'] = PODKLADY[a][0]
                    d = proved(a, s)
                    panel, _, tlacitka = rozlozeni_dialogu(d)
                    self.assertGreaterEqual(panel.top, 0, a)
                    self.assertLessEqual(panel.bottom, 720, a)
                    self.assertTrue(all(panel.contains(t) for t in tlacitka), a)
                    for _, cil in d['moznosti']:
                        proved(cil, s.copy())

    def test_cela_hra_az_k_rezervaci(self):
        s = novy_stav()
        for a in ['sebrat','vyplnit','odevzdat','archiv','cerveny','modry','zeleny','cerveny',
                  'zaznam','recepce','kancelar','platba','evidence','pecet','podpis','schvaleni',
                  'spravce','recepce','skola','archiv','rozpis','recepce','kancelar',
                  'den_ct','cas_15','delka_120','odeslat_termin']:
            proved(a, s)
        self.assertTrue(s['termin'])
