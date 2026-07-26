# Contributing

Thank you for helping make FPGA development more approachable.

## Development setup

1. Use Windows 10/11 and Python 3.10 or later with Tk support.
2. Clone the repository and run `./fpga.ps1 setup` from PowerShell.
3. Start the UI with `./FPGA-IDE.ps1 -Console` while developing.
4. Work in a focused branch and keep generated `build/`, waveform, cache, and
   `.fpga-studio/` files out of commits.

## Required checks

Run the release gate before opening a pull request:

```powershell
.\scripts\release-check.ps1
```

At minimum, changes must preserve:

- Python compilation and all unit tests.
- Clean smart checks for `projects/_template` and `01_button_led_pwm`.
- Verilator lint and the self-checking Icarus simulation.
- Path containment, flash confirmation, and JTAG Interface A guidance.
- Keyboard accessibility and usability at 100–200% Windows display scaling.

For UI changes, regenerate screenshots with
`./scripts/capture-screenshots.ps1` and inspect every image before committing.

## Change style

- Keep the Python UI dependency-free unless a dependency has a clear release,
  security, and maintenance justification.
- Prefer deterministic diagnostics over suggestions that guess hardware intent.
- Never invent board pins or voltage standards.
- Add a focused test for every parser, safety, or telemetry behavior change.
- Document user-facing changes in `CHANGELOG.md` and the relevant README.

By contributing, you agree that your contribution is provided under the MIT
License in this repository.
