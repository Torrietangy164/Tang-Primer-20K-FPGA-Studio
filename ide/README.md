# Tang Primer FPGA Studio

This is a polished, offline desktop IDE for the repository's Tang Primer 20K
workflow. It uses Python's built-in Tk interface, so it has no package-manager,
account, telemetry, or web-service dependency.

Start it from the repository root:

```powershell
.\FPGA-IDE.ps1
```

On Windows, a beginner can also double-click `Open-FPGA-IDE.cmd` in File
Explorer. The PowerShell launcher starts the GUI without a console window.

Use `-Project projects/02_uart_terminal` to select another project at startup.
Use `-Console` when diagnosing a GUI startup problem.

## What is included

- Branded dark workspace, custom icon system, searchable project explorer,
  open-file tabs, breadcrumbs, bracket matching, and rich editor chrome.
- Module hierarchy plus module, port, signal, parameter, and instance indexing.
- `Ctrl+Space` completions for HDL keywords, modules, ports, internal signals,
  and smart snippet aliases such as `fsm`, `sync2`, and `counter`.
- `F12` or `Ctrl+Click` navigation to recognized module definitions.
- Searchable `Ctrl+Shift+P` command palette and whole-project
  `Ctrl+Shift+F` text search.
- Reviewed HDL Pattern Library for sequential logic, combinational logic,
  counters, synchronizers, finite-state machines, and assertions.
- Offline contextual code explanation for selected HDL constructs and symbols.
- Beginner diagnostics for missing top modules, duplicate modules, incomplete
  constraints/electrical standards, duplicate pins, recursive hierarchy,
  missing/self-checking simulations, incomplete cases, and common RTL hazards.
- Safe one-click fixes for strict-net directives and missing testbench skeletons.
- Contextual Beginner Coach with suggested fixes and the safe FPGA workflow.
- Project Insights with a health score, verification readiness, module graph,
  timing margin, device utilization, pin coverage, and artifact status.
- Pin Assignment Inspector showing each signal, package pin, electrical
  properties, and source line without guessing board connections.
- New-project wizard based on `projects/_template` and a new-module wizard.
- Streaming console output for simulate, GTKWave, lint, debug, build, SRAM
  upload, persistent flash, JTAG detection, doctor, UART, setup, and driver
  configuration.
- Confirmation before persistent flash and a Stop button for running commands.

## Where code belongs

For each folder under `projects/`:

- Put synthesizable `.v` and `.sv` modules under `rtl/`.
- Put the configured top module in `rtl/top.sv` unless you deliberately change
  `Top` in `fpga.config.psd1`.
- Put a self-checking `tb_top` testbench in `sim/tb_top.sv`.
- Assign every top-level hardware port in `constraints/primer20k_dock.cst`.
- Treat `build/` as generated output; do not write source code there.

The editor intelligence is intentionally lightweight assistance. It
recognizes the common Verilog/SystemVerilog patterns used by these learning
projects, but it is not a standards-complete language server or a replacement
for Verilator lint and simulation.

## Keyboard shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+S` | Save the current file |
| `Ctrl+Space` | Show project-aware completions |
| `F12` / `Ctrl+Click` | Go to a project module definition |
| `Ctrl+Shift+P` | Open the searchable command palette |
| `Ctrl+Shift+F` | Search text throughout the project |
| `Ctrl+Alt+S` | Open the HDL Pattern Library |
| `Ctrl+Shift+E` | Explain selected HDL context |
| `Ctrl+/` | Toggle line comments |
| `Ctrl+D` | Duplicate the current line |
| `F5` | Simulate |
| `F6` | Simulate and open GTKWave |
| `F7` | Run Verilator lint |
| `F8` | Run the debug flow |
| `F9` | Build and upload to SRAM |
| `Ctrl+B` | Build the bitstream |

For automated checks without opening a window:

```powershell
python ide\fpga_ide.py --check projects\01_button_led_pwm
.\FPGA-IDE.ps1 -SmokeTest -Project projects/01_button_led_pwm
python -m unittest discover -s ide\tests -v
```
