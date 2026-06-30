import unittest

from ui.theme import visible_items


class ThemeHelpersTests(unittest.TestCase):
    def test_visible_items_filters_empty_content(self):
        self.assertEqual(
            visible_items(["Strong skill", "", "   ", None, "Needs work"]),
            ["Strong skill", "Needs work"],
        )


if __name__ == "__main__":
    unittest.main()
