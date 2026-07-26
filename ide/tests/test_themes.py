import unittest

from ide.themes import (
    DEFAULT_THEME,
    SEMANTIC_CONTRAST_PAIRS,
    TEXT_CONTRAST_PAIRS,
    THEME_KEYS,
    THEMES,
    contrast_ratio,
    normalize_theme,
    theme_colors,
    validate_themes,
)


class ThemeTests(unittest.TestCase):
    def test_both_release_palettes_are_complete_and_accessible(self):
        self.assertEqual({"dark", "light"}, set(THEMES))
        self.assertEqual([], validate_themes())
        for palette in THEMES.values():
            self.assertEqual(THEME_KEYS, frozenset(palette))

    def test_text_and_interaction_states_meet_contrast_targets(self):
        for name, palette in THEMES.items():
            for foreground, background in TEXT_CONTRAST_PAIRS:
                with self.subTest(theme=name, pair=f"{foreground}/{background}"):
                    self.assertGreaterEqual(
                        contrast_ratio(palette[foreground], palette[background]), 4.5,
                    )
            for foreground, background in SEMANTIC_CONTRAST_PAIRS:
                with self.subTest(theme=name, pair=f"{foreground}/{background}"):
                    self.assertGreaterEqual(
                        contrast_ratio(palette[foreground], palette[background]), 4.5,
                    )

    def test_invalid_or_corrupt_preferences_recover_to_dark(self):
        for value in (None, 7, {}, "", "neon", "system"):
            with self.subTest(value=value):
                self.assertEqual(DEFAULT_THEME, normalize_theme(value))
        self.assertEqual("light", normalize_theme(" LIGHT "))

    def test_palette_callers_receive_defensive_copies(self):
        first = theme_colors("light")
        first["text"] = "#000000"
        self.assertNotEqual(first["text"], THEMES["light"]["text"])
        self.assertEqual(THEMES["dark"], theme_colors("invalid"))

    def test_contrast_helper_rejects_malformed_colors(self):
        with self.assertRaises(ValueError):
            contrast_ratio("white", "#000000")


if __name__ == "__main__":
    unittest.main()
