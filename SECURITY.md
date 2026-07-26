# Security policy

## Supported version

Security fixes are applied to the latest commit on the repository's default
branch. Older snapshots are not maintained separately.

## Reporting a vulnerability

Do not publish USB-programming, command-injection, path-validation, or unsafe
flash-write vulnerabilities in a public issue. Use GitHub's private
**Security > Report a vulnerability** flow when it is available for this
repository. If private reporting is unavailable, contact the repository owner
through their GitHub profile and request a private channel.

Include the affected version, reproduction steps, impact, and a proposed fix
when possible. Maintainers should acknowledge a report within seven days and
coordinate disclosure after a fix is available.

## Trust boundaries

- The Studio runs locally and has no telemetry, account, or cloud dependency.
- FPGA commands are limited to projects below the checked-out workspace.
- Persistent flash requires confirmation, and projects with blocking smart
  diagnostics cannot be uploaded or flashed from the UI.
- Toolchain archives and the Zadig installer are verified by the repository's
  setup scripts; do not bypass those checks for public distributions.
- HDL projects are executable input to local EDA tools. Review untrusted
  projects and scripts before running them.
