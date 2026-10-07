import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

import generate_card as card


class StatsTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 7, 15, 0, tzinfo=timezone.utc)
        first = self.now.date() - timedelta(days=364)
        self.days = [
            {"date": (first + timedelta(days=i)).isoformat(),
             "contributionCount": 1 if i in (0, 1, 2, 200, 201) else 0}
            for i in range(365)
        ]
        self.payload = {"data": {"user": {"contributionsCollection": {
            "contributionCalendar": {"weeks": [{"contributionDays": self.days}]}
        }}}}

    def fetch(self, payload=None, repos=None):
        with patch.object(card, "_get", side_effect=[
            {"public_repos": 10, "followers": 4},
            [{"pushed_at": "2026-10-06T22:15:00Z"}] if repos is None else repos,
        ]), patch.object(card, "_graphql", return_value=(
            self.payload if payload is None else payload
        )) as graphql:
            result = card.fetch_live_stats("example", "unused", now=self.now)
            return result, graphql.call_args.args[1]

    def test_explicit_window_and_streak(self):
        result, variables = self.fetch()
        self.assertEqual(variables["from"], "2025-10-08T00:00:00Z")
        self.assertEqual(variables["to"], "2026-10-07T15:00:00Z")
        self.assertEqual(result["LONGEST_STREAK"], 3)
        self.assertEqual(result["LAST_PUSH"], "2026-10-06")
        self.assertEqual(result["PUBLIC_REPOS"], 10)

    def test_days_outside_window_do_not_extend_streak(self):
        first = self.now.date() - timedelta(days=365)
        self.days.insert(0, {"date": first.isoformat(), "contributionCount": 1})
        self.days.reverse()
        self.assertEqual(self.fetch()[0]["LONGEST_STREAK"], 3)

    def test_empty_repositories_and_zero_activity(self):
        for day in self.days:
            day["contributionCount"] = 0
        result, _ = self.fetch(repos=[])
        self.assertEqual(result["LAST_PUSH"], "n/a")
        self.assertEqual(result["LONGEST_STREAK"], 0)

    def test_graphql_error_is_not_zero_activity(self):
        with self.assertRaises(ValueError):
            self.fetch(payload={"errors": [{"message": "Unavailable"}]})
        with self.assertRaises(ValueError):
            self.fetch(payload={"data": {"user": None}})

    def test_incomplete_calendar_is_rejected(self):
        self.days.pop(4)
        with self.assertRaises(ValueError):
            self.fetch()

    def test_update_preserves_surrounding_readme_and_is_idempotent(self):
        before = '<img src="./github_profile_banner_full.webp" width="85%">\n\n'
        after = '\n\n## How I work\n\n[About](https://d1d2dopamine.is-a.dev/about.html)\n'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "README.md"
            path.write_text(before + card.START_MARKER + '\nold\n' + card.END_MARKER + after)
            card.update_readme(path, card.sample_stats())
            updated = path.read_text()
            self.assertEqual(updated, before + card.build_badges_line(card.sample_stats()) + after)
            self.assertIn('last_push-', updated)
            self.assertIn('longest_streak_%28365d%29-', updated)
            card.update_readme(path, card.sample_stats())
            self.assertEqual(path.read_text(), updated)

    def test_invalid_markers_leave_readme_untouched(self):
        samples = ["no markers", card.END_MARKER + card.START_MARKER,
                   card.START_MARKER * 2 + card.END_MARKER]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "README.md"
            for source in samples:
                path.write_text(source)
                with self.assertRaises(ValueError):
                    card.update_readme(path, card.sample_stats())
                self.assertEqual(path.read_text(), source)


if __name__ == "__main__":
    unittest.main()
