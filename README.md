Description for Your GitHub Repository
Android Storage Backup using ADB & Python

This Python application allows users to backup the internal storage of an Android device using ADB (Android Debug Bridge). The tool provides a GUI interface built with Tkinter, enabling users to select a connected device, choose an output folder, and start the backup process with a single click.
Features:

✅ Detects connected Android devices using ADB
✅ Allows users to refresh the device list
✅ Select output folder for storing the backup
✅ Backs up /sdcard contents as a .tar archive
✅ Real-time status updates during the process
Requirements:
    Python 3.x
    ADB installed (adb devices should list your phone)
    USB Debugging enabled on your Android device

Usage:
    Connect your Android device via USB.
    Enable USB Debugging in Developer Options.
    Run the script:
    python Drive.py
    Select your device and choose an output folder.
    Click Start to begin the backup process.

Future Enhancements (To-Do):
    Add progress bar for backup status.
    Support for custom folders instead of full /sdcard backup.
    Allow Wi-Fi ADB connection instead of USB.
