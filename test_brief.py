import unittest

from pydantic import ValidationError
from brief_schema import Brief

class BriefTests(unittest.TestCase):
    def test_rejects_two_steps(self):
        with self.assertRaises(ValidationError):
            Brief(
                title="Learn Python",
                steps=["Review loops", "Practice functions"],
                deadline=None,
            )

    def test_rejects_missing_title(self):
        with self.assertRaises(ValidationError):
            Brief(
                steps=["Review loops", "Practice functions", "Take a quiz"],
                deadline=None,
            )  # type: ignore
    def test_accepts_valid_brief(self):
        brief = Brief(
            title="Learn Python",
            steps=["Review loops", "Practice functions", "Take a quiz"],
            deadline=None,
        )

        self.assertEqual(brief.title, "Learn Python")

if __name__ == "__main__":
    unittest.main()