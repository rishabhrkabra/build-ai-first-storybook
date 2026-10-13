"""Synthetic decision/closure regressions, not native Figma acceptance evidence."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from validate_change_sync import digest, pointer, validate


class ChangeSyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        # A separate brand teal is legitimate: the decision applies to neutrals.
        self.write("tokens.json", {"neutrals": ["color/neutral/50", "color/neutral/600"],
                                   "hex": ["#F8F8F8", "#657170"], "brand": "color/teal/500"})
        self.write("foundations.json", {"names": ["color/neutral/50", "color/neutral/600"],
                                        "hex": ["#F8F8F8", "#657170"]})
        self.write("guide.md", "Current guide: color/neutral/600 is #657170.\n")
        self.write("archive.md", "Historical slate and teal specimens remain.\n")
        # Not an image: this fixture tests evidence binding only, never visual QA.
        self.write("capture.fixture", "synthetic capture identity")
        self.data = {
            "schemaVersion": 1,
            "change": {"id": "fixture-1", "decision": "One neutral family, values retained",
                       "approvalSource": "synthetic owner decision", "roots": ["tokens"]},
            "surfaces": [self.surface("tokens", "tokens.json", []),
                         self.surface("foundations", "foundations.json", ["tokens"], True),
                         self.surface("guide", "guide.md", ["foundations"]),
                         self.surface("archive", "archive.md", ["tokens"])],
            "checks": [
                {"id": "family", "actual": {"surface": "tokens", "pointer": "/neutrals"},
                 "op": "every_match", "expected": "color/neutral/[0-9]+"},
                {"id": "names", "actual": {"surface": "foundations", "pointer": "/names"},
                 "op": "equals", "expectedFrom": {"surface": "tokens", "pointer": "/neutrals"}},
                {"id": "values", "actual": {"surface": "foundations", "pointer": "/hex"},
                 "op": "equals", "expectedFrom": {"surface": "tokens", "pointer": "/hex"}},
                {"id": "guide", "actual": {"surface": "guide", "pointer": ""},
                 "op": "contains", "expected": "color/neutral/600 is #657170"}],
            "requirements": [{"id": "intent", "statement": "One neutral family, current docs match",
                              "checks": ["family", "names", "values", "guide"]}],
            "coverage": []}
        for s in self.data["surfaces"]:
            c = {"id": s["id"], "status": "verified", "reason": "Fixture scoped check",
                 "inputs": {dep: self.hash_for(dep) for dep in s["dependsOn"]}}
            if s["id"] == "archive":
                c.update(status="historical-preserved", beforeSha256=s["sha256"])
            else:
                c["checks"] = {"tokens": ["family"], "foundations": ["names", "values"],
                               "guide": ["guide"]}[s["id"]]
            if s["visual"]:
                c["review"] = {"reviewer": "synthetic fixture", "notes": "Binding test only",
                               "result": "pass", "sourceSha256": s["sha256"],
                               "capture": {"path": "capture.fixture",
                                           "sha256": digest(self.base / "capture.fixture")}}
            self.data["coverage"].append(c)

    def write(self, path, value):
        (self.base / path).write_text(json.dumps(value) if isinstance(value, (dict, list)) else value)

    def surface(self, sid, path, deps, visual=False):
        return {"id": sid, "source": f"fixture:{sid}", "path": path,
                "sha256": digest(self.base / path), "dependsOn": deps, "visual": visual}

    def hash_for(self, sid):
        return next(s["sha256"] for s in self.data["surfaces"] if s["id"] == sid)

    def refresh(self, sid):
        s = next(s for s in self.data["surfaces"] if s["id"] == sid)
        s["sha256"] = digest(self.base / s["path"])
        for c in self.data["coverage"]:
            if sid in c["inputs"]:
                c["inputs"][sid] = s["sha256"]
            if c["id"] == sid and "review" in c:
                c["review"]["sourceSha256"] = s["sha256"]

    def assertFails(self, phrase):
        self.assertIn(phrase, "\n".join(validate(self.data, self.base)))

    def test_valid_closure_preserves_history_and_unrelated_brand_family(self):
        self.assertEqual(validate(self.data, self.base), [])

    def test_correct_values_do_not_hide_wrong_family(self):
        tokens = json.loads((self.base / "tokens.json").read_text())
        tokens["neutrals"][1] = "color/gray/600"
        self.write("tokens.json", tokens)
        self.refresh("tokens")
        self.assertFails("family: decision assertion failed")

    def test_stale_document_names_fail_even_with_updated_receipt_hash(self):
        self.write("foundations.json", {"names": ["color/gray/50", "color/gray/600"],
                                        "hex": ["#F8F8F8", "#657170"]})
        self.refresh("foundations")
        self.assertFails("names: decision assertion failed")

    def test_wrong_document_hex_fails(self):
        self.write("guide.md", "Current guide: color/neutral/600 is #697687.")
        self.refresh("guide")
        self.assertFails("guide: decision assertion failed")

    def test_changed_file_and_stale_upstream_fail(self):
        self.write("tokens.json", {"neutrals": ["color/neutral/600"], "hex": ["#657170"]})
        self.assertFails("stale artifact digest")
        self.assertFails("stale or missing upstream evidence")

    def test_missing_transitive_consumer_fails(self):
        self.data["coverage"] = [c for c in self.data["coverage"] if c["id"] != "guide"]
        self.assertFails("guide: affected surface has no coverage")

    def test_pending_or_unchecked_unaffected_cannot_pass(self):
        for status in ("pending", "blocked", "unaffected"):
            with self.subTest(status=status):
                self.data["coverage"][0]["status"] = status
                self.data["coverage"][0]["checks"] = []
                self.assertTrue(validate(self.data, self.base))

    def test_unaffected_with_real_evidence_is_valid(self):
        self.data["coverage"][2]["status"] = "unaffected"
        self.data["coverage"][2]["reason"] = "Guide already has this approved name/value."
        self.assertEqual(validate(self.data, self.base), [])

    def test_history_must_be_preserved(self):
        self.write("archive.md", "Rewritten without authorization")
        self.refresh("archive")
        self.assertFails("history not preserved")

    def test_empty_or_unbound_requirements_fail(self):
        for requirements in ([], [{"id": "a", "statement": "approval", "checks": []}]):
            self.data["requirements"] = requirements
            self.assertTrue(validate(self.data, self.base))

    def test_missing_or_stale_visual_evidence_fails(self):
        original = copy.deepcopy(self.data)
        del self.data["coverage"][1]["review"]
        self.assertTrue(validate(self.data, self.base))
        self.data = original
        self.write("capture.fixture", "different capture")
        self.assertFails("stale visual capture")

    def test_check_must_inspect_its_surface(self):
        self.data["coverage"][2]["checks"] = ["family"]
        self.assertFails("checks do not inspect this surface")

    def test_cycles_unknown_deps_and_duplicates_fail(self):
        original = copy.deepcopy(self.data)
        self.data["surfaces"][0]["dependsOn"] = ["guide"]
        self.assertFails("dependency cycle")
        self.data = copy.deepcopy(original)
        self.data["surfaces"][0]["dependsOn"] = ["missing"]
        self.assertFails("unknown dependency")
        self.data = original
        self.data["surfaces"].append(copy.deepcopy(self.data["surfaces"][0]))
        self.assertFails("duplicate id")

    def test_invalid_pointer_self_parity_and_empty_matches_fail(self):
        self.data["checks"][0]["actual"]["pointer"] = "/missing"
        self.assertFails("invalid assertion")
        self.data["checks"][1]["expectedFrom"] = self.data["checks"][1]["actual"]
        self.assertFails("self-comparison")
        self.write("tokens.json", {"neutrals": [], "hex": []})
        self.refresh("tokens")
        self.data["checks"][0]["actual"]["pointer"] = "/neutrals"
        self.assertFails("family: decision assertion failed")

    def test_pointer_escaping_and_array_bounds(self):
        self.assertEqual(pointer({"a/b": {"x~y": [42]}}, "/a~1b/x~0y/0"), 42)
        for path in ("/-1", "/01", "/1", "/~2"):
            with self.subTest(path=path), self.assertRaises((ValueError, IndexError)):
                pointer([42], path)

    def test_cli_exit_codes(self):
        receipt = self.base / "receipt.json"
        script = str(Path(__file__).with_name("validate_change_sync.py"))
        for expected in (0, 1):
            self.write("receipt.json", self.data)
            result = subprocess.run([sys.executable, script, str(receipt)], capture_output=True, text=True)
            self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)["ok"], expected == 0)
            self.data["coverage"][0]["status"] = "blocked"


if __name__ == "__main__":
    unittest.main()
