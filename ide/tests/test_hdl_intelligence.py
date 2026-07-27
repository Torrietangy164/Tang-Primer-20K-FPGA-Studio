from pathlib import Path
import tempfile
import unittest

from ide.hdl_intelligence import matching_completions, scan_project


CONFIG = """@{
    Top = 'top'
    Constraint = 'constraints/board.cst'
}
"""


class HdlIntelligenceTests(unittest.TestCase):
    def make_project(self, top_text: str, constraints: str, testbench: str) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "rtl").mkdir()
        (root / "sim").mkdir()
        (root / "constraints").mkdir()
        (root / "fpga.config.psd1").write_text(CONFIG, encoding="utf-8")
        (root / "rtl" / "top.sv").write_text(top_text, encoding="utf-8")
        (root / "sim" / "tb_top.sv").write_text(testbench, encoding="utf-8")
        (root / "constraints" / "board.cst").write_text(constraints, encoding="utf-8")
        return root

    def test_modules_ports_instances_and_completion(self):
        root = self.make_project(
            """`default_nettype none
module child(input logic clk, output logic value); endmodule
module top(input logic clk, output logic led);
  logic internal_ready;
  child child_instance(.clk(clk), .value(led));
endmodule
""",
            'IO_LOC "clk" H11;\nIO_LOC "led" L16;\n',
            'module tb_top; initial begin $dumpfile("build/waves.vcd"); $dumpvars; $fatal; end endmodule',
        )
        index = scan_project(root)
        self.assertEqual({"child", "top"}, set(index.modules))
        self.assertEqual(["clk", "led"], [port.name for port in index.modules["top"].ports])
        self.assertEqual("child", index.modules["top"].instances[0].module_type)
        self.assertEqual("internal_ready", index.modules["top"].signals[0].name)
        self.assertIn("internal_ready", matching_completions(index, "internal"))
        self.assertIn("always_ff", matching_completions(index, "always_"))
        self.assertEqual([], [item for item in index.diagnostics if item.severity == "error"])

    def test_missing_pin_and_waveform_are_reported(self):
        root = self.make_project(
            "module top(input logic clk, output logic led); endmodule",
            'IO_LOC "clk" H11;\n',
            "module tb_top; endmodule",
        )
        codes = {item.code for item in scan_project(root).diagnostics}
        self.assertIn("PIN002", codes)
        self.assertIn("SIM002", codes)
        self.assertIn("STYLE001", codes)

    def test_go_to_module_definition(self):
        root = self.make_project(
            "module top(input logic clk); endmodule",
            'IO_LOC "clk" H11;\n',
            'module tb_top; initial begin $dumpfile("build/waves.vcd"); $dumpvars; $fatal; end endmodule',
        )
        index = scan_project(root)
        definition = index.definition("top")
        self.assertIsNotNone(definition)
        self.assertEqual("top.sv", definition[0].name)

    def test_symbol_navigation_references_and_instance_generation(self):
        root = self.make_project(
            """`default_nettype none
module child(input logic clk, input logic valid_i, output logic ready_o);
  logic local_state;
  assign ready_o = valid_i | local_state;
endmodule
module top(input logic clk, output logic led);
  logic valid_i;
  child child_instance(.clk(clk), .valid_i(valid_i), .ready_o(led));
endmodule
""",
            'IO_LOC "clk" H11;\nIO_LOC "led" L16;\n',
            'module tb_top; initial begin $dumpfile("build/waves.vcd"); $dumpvars; $fatal; end endmodule',
        )
        index = scan_project(root)
        signal_definition = index.definition("valid_i", root / "rtl" / "top.sv")
        self.assertIsNotNone(signal_definition)
        self.assertEqual("top.sv", signal_definition[0].name)
        references = index.references("valid_i")
        self.assertGreaterEqual(len(references), 3)
        self.assertTrue(all(location.column >= 1 for location in references))
        instance = index.module_instantiation("child", "u_child")
        self.assertIn("child u_child", instance)
        self.assertIn(".valid_i", instance)
        self.assertIn(".ready_o", instance)

    def test_repository_learning_project_is_clean(self):
        repository = Path(__file__).resolve().parents[2]
        index = scan_project(repository / "projects" / "01_button_led_pwm")
        self.assertEqual("top", index.top_name)
        self.assertIn("button_debouncer", index.modules)
        self.assertEqual([], index.diagnostics)

    def test_hierarchy_case_and_pin_safety_diagnostics(self):
        root = self.make_project(
            """`default_nettype none
module helper(input logic clk);
  top recurse(.clk(clk), .led());
endmodule
module top(input logic clk, output logic led);
  helper child(.clk(clk));
  always_comb begin case (clk) 1'b1: led = 1'b1; endcase end
endmodule
""",
            'IO_LOC "clk" H11;\nIO_PORT "clk" IO_TYPE=LVCMOS33;\nIO_LOC "led" H11;\n',
            'module tb_top; initial begin $dumpfile("build/waves.vcd"); $dumpvars; $fatal; end endmodule',
        )
        codes = {item.code for item in scan_project(root).diagnostics}
        self.assertIn("PIN003", codes)
        self.assertIn("PIN004", codes)
        self.assertIn("ARCH002", codes)
        self.assertIn("RTL001", codes)


if __name__ == "__main__":
    unittest.main()
