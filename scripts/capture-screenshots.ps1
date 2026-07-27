[CmdletBinding()]
param(
    [string] $Project = 'projects/01_button_led_pwm',
    [string[]] $Only = @()
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$workspace = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$ideScript = Join-Path $workspace 'ide\fpga_ide.py'
$outputDirectory = Join-Path $workspace 'docs\images'
New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null

Add-Type @'
using System;
using System.Drawing;
using System.Runtime.InteropServices;
using System.Text;

public static class StudioScreenshot {
    public delegate bool EnumWindowsProc(IntPtr hwnd, IntPtr parameter);

    [StructLayout(LayoutKind.Sequential)]
    public struct RECT { public int Left; public int Top; public int Right; public int Bottom; }

    [DllImport("shcore.dll")]
    public static extern int SetProcessDpiAwareness(int awareness);

    [DllImport("user32.dll")]
    public static extern bool EnumWindows(EnumWindowsProc callback, IntPtr parameter);

    [DllImport("user32.dll")]
    public static extern uint GetWindowThreadProcessId(IntPtr hwnd, out uint processId);

    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    public static extern int GetWindowText(IntPtr hwnd, StringBuilder value, int length);

    [DllImport("user32.dll")]
    public static extern bool IsWindowVisible(IntPtr hwnd);

    [DllImport("user32.dll")]
    public static extern bool GetWindowRect(IntPtr hwnd, out RECT rect);

    [DllImport("user32.dll")]
    public static extern bool PrintWindow(IntPtr hwnd, IntPtr hdc, uint flags);

    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hwnd);

    public static IntPtr FindWindow(int processId, string titlePart) {
        IntPtr result = IntPtr.Zero;
        EnumWindows(delegate(IntPtr hwnd, IntPtr parameter) {
            uint owner;
            GetWindowThreadProcessId(hwnd, out owner);
            if (owner != processId || !IsWindowVisible(hwnd)) return true;
            StringBuilder title = new StringBuilder(512);
            GetWindowText(hwnd, title, title.Capacity);
            if (title.ToString().IndexOf(titlePart, StringComparison.OrdinalIgnoreCase) >= 0) {
                result = hwnd;
                return false;
            }
            return true;
        }, IntPtr.Zero);
        return result;
    }
}
'@

try { [void] [StudioScreenshot]::SetProcessDpiAwareness(1) } catch { }
Add-Type -AssemblyName System.Drawing

$python = Get-Command pythonw -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command python -ErrorAction Stop }
$views = @(
    @{ Demo = 'main';     Theme = 'dark';  Title = 'Tang Primer FPGA Studio'; File = 'studio-main.png' },
    @{ Demo = 'insights'; Theme = 'dark';  Title = 'Tang Primer FPGA Studio'; File = 'studio-insights.png' },
    @{ Demo = 'commands'; Theme = 'dark';  Title = 'Command Palette';          File = 'studio-command-palette.png' },
    @{ Demo = 'snippets'; Theme = 'dark';  Title = 'HDL Pattern Library';      File = 'studio-pattern-library.png' },
    @{ Demo = 'pins';     Theme = 'dark';  Title = 'Pin Assignment Inspector'; File = 'studio-pin-inspector.png' },
    @{ Demo = 'verification'; Theme = 'dark'; Title = 'Verification center'; File = 'studio-verification-center.png' },
    @{ Demo = 'hardware'; Theme = 'dark'; Title = 'Tang Primer 20K hardware setup'; File = 'studio-hardware-setup.png' },
    @{ Demo = 'uart'; Theme = 'dark'; Title = 'UART terminal'; File = 'studio-uart-terminal.png' },
    @{ Demo = 'tutorial'; Theme = 'light'; Title = 'First-project tutorial'; File = 'studio-first-project-tutorial.png' },
    @{ Demo = 'netlist'; Theme = 'dark'; Title = 'Synthesized netlist viewer'; File = 'studio-netlist-viewer.png' },
    @{ Demo = 'release-notes'; Theme = 'dark'; Title = "What's new in 1.2.0"; File = 'studio-release-notes.png' },
    @{ Demo = 'main';     Theme = 'light'; Title = 'Tang Primer FPGA Studio'; File = 'studio-main-light.png' },
    @{ Demo = 'snippets'; Theme = 'light'; Title = 'HDL Pattern Library'; File = 'studio-pattern-library-light.png' }
)
if ($Only.Count -gt 0) {
    $views = @($views | Where-Object { $Only -contains $_.Demo })
    if ($views.Count -eq 0) {
        throw "No screenshot view matched -Only: $($Only -join ', ')"
    }
}

foreach ($view in $views) {
    $argumentLine = '"{0}" --project "{1}" --theme {2} --demo-view {3} --skip-startup-release-notes' -f $ideScript, $Project, $view.Theme, $view.Demo
    $process = Start-Process -FilePath $python.Source -ArgumentList $argumentLine -WorkingDirectory $workspace -PassThru
    try {
        $handle = [IntPtr]::Zero
        $deadline = [DateTime]::UtcNow.AddSeconds(20)
        while ($handle -eq [IntPtr]::Zero -and [DateTime]::UtcNow -lt $deadline) {
            Start-Sleep -Milliseconds 200
            $handle = [StudioScreenshot]::FindWindow($process.Id, $view.Title)
        }
        if ($handle -eq [IntPtr]::Zero) {
            throw "Timed out waiting for '$($view.Title)'"
        }
        [void] [StudioScreenshot]::SetForegroundWindow($handle)
        Start-Sleep -Milliseconds 650
        $rect = New-Object StudioScreenshot+RECT
        $width = 0
        $height = 0
        $boundsDeadline = [DateTime]::UtcNow.AddSeconds(5)
        while (($width -lt 100 -or $height -lt 100) -and [DateTime]::UtcNow -lt $boundsDeadline) {
            [void] [StudioScreenshot]::GetWindowRect($handle, [ref] $rect)
            $width = $rect.Right - $rect.Left
            $height = $rect.Bottom - $rect.Top
            if ($width -lt 100 -or $height -lt 100) { Start-Sleep -Milliseconds 150 }
        }
        if ($width -lt 100 -or $height -lt 100) {
            throw "Invalid capture bounds for '$($view.Title)': ${width}x${height}"
        }
        $bitmap = New-Object Drawing.Bitmap($width, $height)
        $graphics = [Drawing.Graphics]::FromImage($bitmap)
        try {
            $deviceContext = $graphics.GetHdc()
            try {
                $printed = [StudioScreenshot]::PrintWindow($handle, $deviceContext, 2)
            } finally {
                $graphics.ReleaseHdc($deviceContext)
            }
            if (-not $printed) {
                $graphics.CopyFromScreen($rect.Left, $rect.Top, 0, 0, $bitmap.Size)
            }
            $target = Join-Path $outputDirectory $view.File
            $bitmap.Save($target, [Drawing.Imaging.ImageFormat]::Png)
            Write-Host "Captured $($view.Demo) [$($view.Theme)]: $target (${width}x${height})" -ForegroundColor Green
        } finally {
            $graphics.Dispose()
            $bitmap.Dispose()
        }
    } finally {
        if (-not $process.HasExited) {
            Stop-Process -Id $process.Id -Force
        }
    }
}
