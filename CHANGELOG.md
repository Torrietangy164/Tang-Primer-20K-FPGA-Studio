# Changelog

All notable user-facing changes are recorded here.

## Unreleased

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
