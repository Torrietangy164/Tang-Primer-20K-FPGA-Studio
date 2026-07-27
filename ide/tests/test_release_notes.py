import unittest

from ide.release_notes import (
    mark_release_notes_seen,
    notes_for_version,
    release_notes_pending,
)


class ReleaseNotesTests(unittest.TestCase):
    def test_v12_notes_are_complete_and_use_known_icons(self):
        notes = notes_for_version("1.2.0")
        self.assertEqual("1.2.0", notes.version)
        self.assertEqual(6, len(notes.highlights))
        self.assertTrue(all(item.title and item.description and item.icon for item in notes.highlights))
        with self.assertRaises(ValueError):
            notes_for_version("99.0.0")

    def test_notes_are_pending_once_for_each_exact_version(self):
        settings: dict[str, object] = {}
        self.assertTrue(release_notes_pending(settings, "1.2.0"))
        mark_release_notes_seen(settings, "1.2.0")
        self.assertFalse(release_notes_pending(settings, "1.2.0"))
        self.assertTrue(release_notes_pending(settings, "1.3.0"))


if __name__ == "__main__":
    unittest.main()
