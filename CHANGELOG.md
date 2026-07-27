# Changelog

All notable user-facing changes are recorded here.

## Unreleased

- No changes yet.

## 1.2.0 — review build — 2026-07-27

### Added

- Added a root-level, literal-beginner `INSTALL.md` covering each Windows
  prerequisite through a first safe SRAM upload, with automated sequence,
  link, repository URL, and hardware-safety checks.
- Replaced the folder-name prompt with a safe New Project Wizard offering
  complete board-I/O and UART starting points plus an optional guided tutorial.
- Added HDL symbol navigation for modules, ports, signals, and instances,
  project-wide exact references, and named-port module-instantiation generation.
- Added a dependency-free integrated Windows UART terminal with COM-port
  discovery, transmit and receive, ASCII/hex views, timestamps, line endings,
  history, connection recovery, and UTF-8 log saving.
- Added a Verification Center for selecting testbenches and GTKWave layouts,
  running simulation/debug, and summarizing PASS/FAIL assertion lines.
- Added guided board/JTAG/UART/driver setup and an interactive six-step first
  FPGA workflow that persists progress per project.
- Added clickable Verilator/Icarus-style console locations and selection-safe
  PowerShell support for `-Testbench`, `-TestbenchTop`, and `-WaveLayout`.
- Added a complete UART greeting/echo learning project with RX, TX, physical
  UART constraints, waveform layout, documentation, and protocol-level tests.

### Changed

- Refined both themes into calmer, more natural professional palettes and
  replaced mechanical labels with clearer human language and workflow groups.
- Expanded CI and local release gates to validate the maintained UART project
  and retheme seven open feature dialogs across 30 live theme changes.

### Verified

- 29 Python tests, dark/light startup, theme rollback and contrast checks,
  Verilator lint, a 30-byte bidirectional UART simulation, and Tang Primer 20K
  synthesis/place/route/packing at 27 MHz (345.90 MHz reported maximum).

## 1.1.0 — 2026-07-26

### Added

- Added a complete accessible light theme alongside the refined dark theme,
  with a header control, View menu, `Ctrl+Alt+T` shortcut, startup override,
  and locally remembered preference.
- Added semantic color tokens, theme-aware custom icon regeneration, live
  retheming for open editors/dialogs/menus/canvases, and safe rollback when a
  platform-specific UI operation fails.
- Expanded the HDL Pattern Library from six snippets to 72 categorized,
  searchable references with difficulty, scope, explanations, code copying,
  editor insertion, and completion aliases.
- Added automated validation for library size, metadata, aliases, filtering,
  and separation of synthesizable RTL from testbench-only constructs.
- Added WCAG contrast validation, dark/light startup smoke tests, a 30-cycle
  live-switch stress test with dialogs open, state/icon checks, and injected
  failure recovery verification.

### Verified

- Complete release gate across Python, PowerShell, project intelligence,
  Verilator lint, self-checking Icarus simulation, both UI themes, and
  reproducible dark/light screenshots.

## 1.0.0 — 2026-07-26

### Added

- Premium, DPI-aware desktop workspace with custom iconography, searchable
  explorer, open-file tabs, editor breadcrumbs, bracket matching, tooltips,
  and grouped Create/Verify/Implement actions.
- Command palette, project-wide search, HDL Pattern Library, contextual HDL
  explanation, pin assignment inspector, safe quick fixes, and generated
  testbench skeletons.
- Module, port, signal, parameter, and instance indexing with hierarchy,
  constraint, electrical-standard, duplicate-pin, recursion, case-completeness,
  synthesis, and simulation diagnostics.
- Project health, workflow readiness, module hierarchy, Fmax, resource use,
  artifact status, session history, and live command timing.
- Rotating crash/diagnostic logs, remembered project selection, hardware-action
  validation, and safer interruption of programming commands.
- Reproducible screenshots, CI quality gates, release checks, security policy,
  contribution guide, code of conduct, and MIT license.

### Verified

- Tang Primer 20K Project 01 Verilator lint, self-checking Icarus simulation,
  nextpnr timing data, and open-source bitstream workflow.

## 0.1.0-beta — 2026-07-26

- Initial dependency-free desktop UI for the repository's verified PowerShell
  simulation, waveform, build, upload, flash, JTAG, UART, and diagnosis flow.
