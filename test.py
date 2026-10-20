"""
Unit tests for shortcut detection and math template formatting.
Run with: python3 test.py
"""

import unittest
import shortcutDetection
import mathShortcuts

class TestShortcutDetection(unittest.TestCase):
    def setUp(self):
        shortcutDetection.shortcuts['//alpha'] = 'α'
        shortcutDetection.shortcuts['//pi'] = 'π'
        shortcutDetection.shortcuts['//deg'] = '°'
        shortcutDetection.shortcuts['//degree'] = '°'
        shortcutDetection.shortcuts['//in'] = '∈'
        shortcutDetection.shortcuts['//infty'] = '∞'

    def test_direct_symbol_lookup(self):
        self.assertEqual(shortcutDetection.getSymbol('//alpha'), 'α')
        self.assertEqual(shortcutDetection.getSymbol('//pi'), 'π')

    def test_find_shortcut_exact(self):
        match = shortcutDetection.findShortcut('//alpha', allowAmbiguous=False)
        self.assertIsNotNone(match)
        shortcut, start, end = match
        self.assertEqual(shortcut, '//alpha')
        self.assertEqual(start, 0)
        self.assertEqual(end, 7)

    def test_find_shortcut_in_sentence(self):
        match = shortcutDetection.findShortcut('angle is //theta rad', allowAmbiguous=False)
        self.assertIsNotNone(match)
        self.assertEqual(match[0], '//theta')

    def test_ambiguous_shortcuts_deferred(self):
        # '//deg' is a prefix of '//degree', so allowAmbiguous=False should defer it
        match_unambig = shortcutDetection.findShortcut('//deg', allowAmbiguous=False)
        self.assertIsNone(match_unambig, '//deg should be deferred because //degree exists')
        
        # When debounce expires (allowAmbiguous=True), it should match
        match_ambig = shortcutDetection.findShortcut('//deg', allowAmbiguous=True)
        self.assertIsNotNone(match_ambig)
        self.assertEqual(match_ambig[0], '//deg')

    def test_non_existent_shortcut(self):
        match = shortcutDetection.findShortcut('notashortcut', allowAmbiguous=True)
        self.assertIsNone(match)

class TestMathShortcuts(unittest.TestCase):
    def test_superscript_formatting(self):
        res = mathShortcuts.finalText('//pow', ['x', '2'])
        self.assertEqual(res, 'x²')

    def test_superscript_multichar(self):
        res = mathShortcuts.finalText('//pow', ['n', '10'])
        self.assertEqual(res, 'n¹⁰')

    def test_subscript_formatting(self):
        res = mathShortcuts.finalText('//_', ['i'])
        self.assertEqual(res, 'ᵢ')

    def test_fraction_formatting(self):
        res = mathShortcuts.finalText('//frac', ['a', 'b'])
        self.assertEqual(res, '(a)/(b)')

    def test_limit_formatting(self):
        res = mathShortcuts.finalText('//lim', ['x', '0', 'sin(x)/x'])
        self.assertEqual(res, 'lim_(x→0) sin(x)/x')

    def test_derivative_formatting(self):
        res = mathShortcuts.finalText('//ddx', ['x^2'])
        self.assertEqual(res, 'd/dx(x^2)')

if __name__ == '__main__':
    unittest.main()
