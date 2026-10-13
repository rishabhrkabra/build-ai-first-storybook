import copy
import unittest
from validate_composition import validate


class CompositionGateTests(unittest.TestCase):
    def check(self, kind, **values):
        return {'id': 'fixture', 'source': 'explicit-test', 'subjects': ['a', 'b'], 'kind': kind, **values}

    def test_equal_cards(self):
        self.assertFalse(validate({'checks': [self.check('card_row', items=[{'height': 314, 'footerY': 262}]*2)]}))

    def test_old_unequal_cards(self):
        self.assertTrue(validate({'checks': [self.check('card_row', items=[{'height': 294, 'footerY': 242}, {'height': 314, 'footerY': 262}])]}))

    def test_footer_mismatch(self):
        self.assertTrue(validate({'checks': [self.check('card_row', items=[{'height': 314, 'footerY': 242}, {'height': 314, 'footerY': 262}])]}))

    def test_deliberate_masonry(self):
        self.assertFalse(validate({'checks': [self.check('card_row', masonryApproved=True, items=[{'height': 250}, {'height': 350}])]}))

    def test_old_mixed_actions(self):
        self.assertTrue(validate({'checks': [self.check('action_row', items=[{'height': 28, 'y': 0}, {'height': 52, 'y': 0}])]}))

    def test_intentional_centred_icon(self):
        self.assertFalse(validate({'checks': [self.check('action_row', intentionalMixedSize=True, items=[{'height': 28, 'y': 12}, {'height': 52, 'y': 0}])]}))

    def test_nested_helper(self):
        self.assertFalse(validate({'checks': [self.check('field_helper', sameFieldAncestor=True, controlGap=8, nextFieldGap=24)]}))

    def test_old_orphan_helper(self):
        self.assertTrue(validate({'checks': [self.check('field_helper', sameFieldAncestor=False, controlGap=24, nextFieldGap=24)]}))

    def test_url_icon_missing(self):
        self.assertTrue(validate({'checks': [self.check('url_input', urlOnly=True, verifiedLinkIcon=False)]}))

    def test_mixed_input_exception(self):
        self.assertFalse(validate({'checks': [self.check('url_input', urlOnly=False, verifiedLinkIcon=False)]}))

    def test_wrong_state_foreground(self):
        self.assertTrue(validate({'checks': [self.check('state_icon', actualTokenId='icon/default', expectedTokenId='control/selected', actualStroke=1.5, expectedStroke=1.5)]}))

    def test_wrong_stroke(self):
        self.assertTrue(validate({'checks': [self.check('state_icon', actualTokenId='selected', expectedTokenId='selected', actualStroke=2, expectedStroke=1.5)]}))

    def test_vertical_overflow_cannot_hide_behind_horizontal_pass(self):
        self.assertTrue(validate({'checks': [self.check('bounds', horizontalOverflow=False, verticalOverflow=True, unintendedOverlap=False)]}))

    def test_zero_or_missing_subjects(self):
        self.assertTrue(validate({'checks': []}))
        self.assertTrue(validate({'checks': [self.check('bounds', subjects=[], horizontalOverflow=False, verticalOverflow=False, unintendedOverlap=False)]}))



if __name__ == '__main__':
    unittest.main()
