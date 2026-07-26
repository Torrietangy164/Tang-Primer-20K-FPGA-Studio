[CmdletBinding()]
param(
    [string] $Project = 'projects/01_button_led_pwm'
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
    @{ Demo = 'main';     Title = 'Tang Primer FPGA Studio'; File = 'studio-main.png' },
    @{ Demo = 'insights'; Title = 'Tang Primer FPGA Studio'; File = 'studio-insights.png' },
    @{ Demo = 'commands'; Title = 'Command Palette';          File = 'studio-command-palette.png' },
    @{ Demo = 'snippets'; Title = 'HDL Pattern Library';      File = 'studio-pattern-library.png' },
    @{ Demo = 'pins';     Title = 'Pin Assignment Inspector'; File = 'studio-pin-inspector.png' }
)

foreach ($view in $views) {
    $argumentLine = '"{0}" --project "{1}" --demo-view {2}' -f $ideScript, $Project, $view.Demo
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
        [void] [StudioScreenshot]::GetWindowRect($handle, [ref] $rect)
        $width = $rect.Right - $rect.Left
        $height = $rect.Bottom - $rect.Top
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
            Write-Host "Captured $($view.Demo): $target (${width}x${height})" -ForegroundColor Green
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
