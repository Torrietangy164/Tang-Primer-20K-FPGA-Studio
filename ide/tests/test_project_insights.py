from pathlib import Path
import json
import tempfile
import unittest

from ide.hdl_intelligence import ProjectIndex
from ide.project_insights import load_project_insights, workflow_steps


class ProjectInsightTests(unittest.TestCase):
    def test_timing_and_resource_metrics(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "build").mkdir()
        (root / "fpga.config.psd1").write_text("@{ ClockMHz = 27 }", encoding="utf-8")
        (root / "build" / "timing.json").write_text(json.dumps({
            "fmax": {"clk": {"achieved": 81.5, "constraint": 27}},
            "utilization": {"LUT4": {"used": 100, "available": 1000}},
        }), encoding="utf-8")
        index = ProjectIndex(root, "top", {}, [], [])
        insights = load_project_insights(root, index)
        self.assertEqual(100, insights.score)
        self.assertEqual(81.5, insights.achieved_mhz)
        self.assertEqual(27.0, insights.target_mhz)
        self.assertEqual(10.0, insights.resources[0].percent)

    def test_workflow_reflects_artifacts_and_session(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "build").mkdir()
        (root / "build" / "top.fs").write_bytes(b"fs")
        index = ProjectIndex(root, "top", {}, [], [])
        states = {name: state for name, state, _detail in workflow_steps(root, index, {"lint"})}
        self.assertEqual("ready", states["Smart checks"])
        self.assertEqual("ready", states["Lint"])
        self.assertEqual("ready", states["Bitstream"])
        self.assertEqual("next", states["JTAG"])


if __name__ == "__main__":
    unittest.main()
