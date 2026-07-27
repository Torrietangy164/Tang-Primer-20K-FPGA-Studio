from pathlib import Path
import tempfile
import unittest

from ide.project_wizard import (
    ProjectCreationError,
    ProjectTemplate,
    create_project,
    validate_project_name,
)
from ide.serial_backend import (
    SerialPortInfo,
    encode_terminal_input,
    format_terminal_bytes,
    natural_port_key,
    preferred_serial_port,
)
from ide.workflow_tools import (
    discover_verification_assets,
    parse_tool_diagnostic,
    summarize_verification_output,
)


class ProjectWizardTests(unittest.TestCase):
    def test_name_validation_blocks_traversal_and_mixed_case(self):
        self.assertEqual("04_uart_echo", validate_project_name(" 04_uart_echo "))
        for bad_name in ("../escape", "UART", "4_uart", "04-UART"):
            with self.subTest(name=bad_name), self.assertRaises(ProjectCreationError):
                validate_project_name(bad_name)

    def test_project_creation_is_complete_and_does_not_copy_build(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        template = root / "template"
        for relative in (
            "rtl/top.sv", "rtl/files.f", "sim/tb_top.sv",
            "constraints/primer20k_dock.cst", "fpga.config.psd1", "README.md",
            "build/generated.bin",
        ):
            path = template / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# Old title\n" if path.name == "README.md" else "ok", encoding="utf-8")
        spec = ProjectTemplate("test", "Test", "Test template", template)
        target = create_project(root / "projects", "04_created", spec, display_name="UART Echo Lab")
        self.assertTrue((target / "rtl" / "top.sv").is_file())
        self.assertFalse((target / "build").exists())
        self.assertTrue((target / "README.md").read_text(encoding="utf-8").startswith("# UART Echo Lab"))
        with self.assertRaises(ProjectCreationError):
            create_project(root / "projects", "04_created", spec)


class WorkflowToolTests(unittest.TestCase):
    def test_clickable_verilator_and_iverilog_diagnostics(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        rtl = root / "rtl"
        rtl.mkdir()
        source = rtl / "top.sv"
        source.write_text("module top; endmodule", encoding="utf-8")
        item = parse_tool_diagnostic("%Error: rtl/top.sv:12:7: Unexpected token", root)
        self.assertIsNotNone(item)
        self.assertEqual(source.resolve(), item.path)
        self.assertEqual((12, 7), (item.line, item.column))
        item = parse_tool_diagnostic("rtl/top.sv:9: warning: Width mismatch", root)
        self.assertIsNotNone(item)
        self.assertEqual("warning", item.severity)

    def test_verification_discovery_and_summary(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        sim = root / "sim"
        sim.mkdir()
        (sim / "tb_uart.sv").write_text("module tb_uart; endmodule", encoding="utf-8")
        (sim / "uart.gtkw").write_text("[*]", encoding="utf-8")
        benches, layouts = discover_verification_assets(root)
        self.assertEqual("tb_uart", benches[0].top_module)
        self.assertEqual("uart.gtkw", layouts[0].path.name)
        self.assertEqual(("Passed", 2, 0), summarize_verification_output("PASS: one\nPASS: two\n", 0))
        self.assertEqual("Failed", summarize_verification_output("FAIL: broken\n", 1)[0])


class SerialHelperTests(unittest.TestCase):
    def test_ascii_hex_and_natural_port_order(self):
        self.assertEqual(b"Hello", encode_terminal_input("Hello", "ascii"))
        self.assertEqual(b"Hello", encode_terminal_input("48 65 6c 6c 6f", "hex"))
        self.assertEqual("48 69", format_terminal_bytes(b"Hi", "hex"))
        self.assertLess(natural_port_key("COM9"), natural_port_key("COM15"))
        ports = [SerialPortInfo("COM4", "BthModem4"), SerialPortInfo("COM15", "VCP0")]
        self.assertEqual("COM15", preferred_serial_port(ports).port)
        self.assertIsNone(preferred_serial_port([SerialPortInfo("COM4", "BthModem4"), SerialPortInfo("COM5", "BthModem1")]))
        with self.assertRaises(ValueError):
            encode_terminal_input("ABC", "hex")


if __name__ == "__main__":
    unittest.main()
