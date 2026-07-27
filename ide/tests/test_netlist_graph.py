import json
from pathlib import Path
import tempfile
import unittest

from ide.netlist_graph import NetlistError, cell_category, load_yosys_netlist


class NetlistGraphTests(unittest.TestCase):
    def make_netlist(self) -> tuple[Path, Path]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "rtl").mkdir()
        (root / "build").mkdir()
        (root / "rtl" / "top.sv").write_text("module top; endmodule", encoding="utf-8")
        payload = {
            "creator": "Yosys test",
            "modules": {
                "top": {
                    "attributes": {"top": "0001"},
                    "ports": {
                        "clk": {"direction": "input", "bits": [2]},
                        "led": {"direction": "output", "bits": [5]},
                    },
                    "cells": {
                        "logic_cell": {
                            "type": "LUT2",
                            "attributes": {"src": "rtl/top.sv:3.1-3.20"},
                            "port_directions": {"I0": "input", "I1": "input", "O": "output"},
                            "connections": {"I0": [2], "I1": ["1"], "O": [4]},
                        },
                        "register": {
                            "type": "DFF",
                            "attributes": {"src": "rtl/top.sv:4.1-4.20"},
                            "port_directions": {"CLK": "input", "D": "input", "Q": "output"},
                            "connections": {"CLK": [2], "D": [4], "Q": [5]},
                        },
                    },
                    "netnames": {
                        "clk": {"hide_name": 0, "bits": [2]},
                        "next_led": {"hide_name": 0, "bits": [4]},
                        "led": {"hide_name": 0, "bits": [5]},
                    },
                }
            },
        }
        target = root / "build" / "top.json"
        target.write_text(json.dumps(payload), encoding="utf-8")
        return root, target

    def test_loads_cells_categories_sources_and_connections(self):
        root, target = self.make_netlist()
        graph = load_yosys_netlist(target, root, "top")
        self.assertEqual("top", graph.module_name)
        self.assertEqual(2, len(graph.cells))
        self.assertEqual("Logic", graph.cells["logic_cell"].category)
        self.assertEqual("Sequential", graph.cells["register"].category)
        self.assertEqual((root / "rtl" / "top.sv").resolve(), graph.cells["register"].source.path)
        self.assertTrue(any(edge.source == "logic_cell" and edge.target == "register" for edge in graph.connections))
        self.assertTrue(any(edge.source == "register" and edge.target == "port:led" for edge in graph.connections))
        self.assertTrue(any(edge.source == "port:clk" and edge.target == "register" for edge in graph.connections))

    def test_category_classification_and_bad_payload(self):
        self.assertEqual("Memory", cell_category("RAM16SDP4"))
        self.assertEqual("Clock/reset", cell_category("rPLL"))
        self.assertEqual("I/O", cell_category("OBUF"))
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        target = root / "bad.json"
        target.write_text("{}", encoding="utf-8")
        with self.assertRaises(NetlistError):
            load_yosys_netlist(target, root)


if __name__ == "__main__":
    unittest.main()
