\# Fallout 4 ESM Patcher



\## Version 1.0.0



A standalone tool to patch Next-Gen Fallout4.esm files for mod compatibility. This will downgrade your Fallout4.esm to a compatible format without having to download the whole ESM file from Steam. I developed this to prevent Fallout: London VR from crashing when it's trying to access DLC content. It might also be useful for other VR mods, and mods that require the older ESM format.



\## ✨ Features



\- \*\*Auto-Detection\*\*: Automatically finds Fallout 4 installations on your system

\- \*\*Smart Detection\*\*: Identifies if your ESM file needs patching or is already compatible

\- \*\*Safe Patching\*\*: Always creates a backup before making changes

\- \*\*Restore Function\*\*: Easy one-click restore from backup if needed

\- \*\*GUI \& CLI\*\*: User-friendly interface with command-line support for advanced users

\- \*\*Detailed Logging\*\*: Creates log files for troubleshooting



\## 📋 Requirements



\- Windows 7/8/10/11

\- Fallout 4 with Next-Gen update

\- ~350 MB free disk space for the patching process



\### GUI Mode 

1. Launch `Esm Patcher.exe`

2\. Click \*\*"Auto-Detect Fallout 4 Installations"\*\* or browse manually to your Fallout4.esm

3\. The tool will analyze your file and show if patching is needed

4\. If patching is required, click \*\*"Apply Patch"\*\*

5\. Wait for the process to complete (usually takes 10-30 seconds)

6\. Done! Your ESM is now compatible with mods



\### Command Line Mode



For advanced users or batch processing:



```bash

ESM\_Patcher.exe "C:\\Path\\To\\Fallout4.esm"

```



\## 🔍 Supported ESM Versions



The patcher supports the following Next-Gen ESM versions:

\- \*\*330,777,465 bytes\*\* (323,025 KB variant)

\- \*\*330,553,163 bytes\*\* (322,806 KB variant)



\## ⚠️ Important Notes



\- \*\*Always close Fallout 4/Fallout 4 VR\*\* before patching

\- The tool creates a `.backup` file automatically - do not delete this until you're sure the patch works

\- If you verify game files through Steam/GOG, you'll need to re-patch


\## 🛠️ Troubleshooting



\### "Unknown ESM version"

Your Fallout4.esm is not a recognized Next-Gen version. This tool only patches specific Next-Gen versions.



\### "Patch failed"

1\. Make sure Fallout 4 is not running

2\. Check you have write permissions to the game folder

3\. Try running the patcher as Administrator

4\. Check the log file for detailed error messages



\### Game crashes after patching

Use the "Restore Backup" button to revert to your original ESM, then verify the ESM was the correct Next-Gen version before patching.



\## 🤝 Credits



\- \*\*xdelta3\*\* by Joshua MacDonald for delta compression



\## 📜 License



This tool is provided as-is for the Fallout modding community. The patches are derived from the Fallout: London installer.



\## 🐛 Bug Reports \& Support



Please report issues in the Posts section with:

\- Your Fallout4.esm file size (in bytes)

\- The error message you received

\- The log file (created in the same folder as the exe)



\*\*Essential for Next-Gen Fallout 4 users who want to access DLC or play Fallout: London or other mods requiring the older ESM format!\*\*

