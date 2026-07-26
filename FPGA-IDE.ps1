[CmdletBinding()]
param(
    [string] $Project = 'projects/01_button_led_pwm',
    [switch] $Console,
    [switch] $SmokeTest
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ideScript = Join-Path $PSScriptRoot 'ide\fpga_ide.py'
if (-not (Test-Path -LiteralPath $ideScript -PathType Leaf)) {
    throw "The FPGA IDE entry point is missing: $ideScript"
}

$pythonCommand = Get-Command $(if ($Console -or $SmokeTest) { 'python' } else { 'pythonw' }) -ErrorAction SilentlyContinue
if (-not $pythonCommand) {
    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
}
if (-not $pythonCommand) {
    throw 'Python 3 is required. Install Python 3.10 or later and enable Add Python to PATH.'
}

if ($Console -or $SmokeTest) {
    $arguments = @($ideScript, '--project', $Project)
    if ($SmokeTest) {
        $arguments += '--ui-smoke-test'
    }
    & $pythonCommand.Source @arguments
    exit $LASTEXITCODE
}

$argumentLine = '"{0}" --project "{1}"' -f $ideScript, $Project
Start-Process -FilePath $pythonCommand.Source -ArgumentList $argumentLine -WorkingDirectory $PSScriptRoot
Write-Host 'Tang Primer FPGA Studio started.' -ForegroundColor Green
