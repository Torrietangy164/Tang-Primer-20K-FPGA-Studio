# Deployment and operations

## Supported deployment

The supported distribution is a complete repository checkout on Windows 10 or
11. Keeping the UI, project templates, PowerShell runner, constraints, and
documentation together prevents version skew.

Requirements:

- Python 3.10 or later with Tk enabled (included by default in python.org's
  Windows installer).
- PowerShell 5.1 or later.
- A supported Tang Primer 20K + Dock connection for hardware commands.
- The pinned OSS CAD Suite installed by `./fpga.ps1 setup`.

Launch with `./FPGA-IDE.ps1` or double-click `Open-FPGA-IDE.cmd`. Use
`./FPGA-IDE.ps1 -Console` when diagnosing startup problems.

## Release gate

Run this before distributing a checkout or publishing a tag:

```powershell
.\scripts\release-check.ps1
.\scripts\capture-screenshots.ps1
git diff --check
```

The release check compiles Python, runs unit and project-intelligence tests,
parses all PowerShell scripts, validates JSON, and runs HDL lint/simulation.
GitHub Actions repeats platform-independent gates for every push and pull
request.

## Runtime data

The application stores local state under `.fpga-studio/`:

- `settings.json` remembers the last selected project.
- `logs/studio.log` is a rotating diagnostic log, capped at approximately
  1 MB per file with three backups.

This directory is ignored by Git. The application sends no telemetry and does
not require an account or network connection after toolchain setup.

## Recovery

- UI callback errors are logged and reported without terminating the editor.
- Build artifacts can be recreated with `./fpga.ps1 clean` followed by build.
- Upload uses volatile SRAM and is the preferred hardware validation path.
- Persistent flash is guarded by a confirmation and blocked when smart checks
  contain red errors.
- If programming is interrupted, power-cycle the board, run `detect`, then
  retry SRAM upload before attempting persistent flash.

No software can guarantee immunity from faulty HDL, damaged hardware, driver
failures, or power loss. These controls make failures observable, contained,
and recoverable rather than claiming the system is literally unbreakable.
