import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading
import os

def list_devices():
    # List connected Android devices
    try:
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
        devices = [line.split("\t")[0] for line in result.stdout.splitlines() if "device" in line and not line.startswith("List")]
    except Exception as e:
        devices = []
    return devices

def select_output_folder():
    folder = filedialog.askdirectory()
    if folder:
        output_var.set(folder)

def refresh_devices():
    device_menu['menu'].delete(0, 'end')
    new_devices = list_devices()
    for device in new_devices:
        device_menu['menu'].add_command(label=device, command=tk._setit(device_var, device))
    if new_devices:
        device_var.set(new_devices[0])

def start_imaging():
    device = device_var.get()
    output_folder = output_var.get()
    if not device or not output_folder:
        messagebox.showerror("Error", "Please select a device and an output folder.")
        return

    # Create the temporary backup directory
    temp_dir = os.path.join(output_folder, "Android_Backup")
    os.makedirs(temp_dir, exist_ok=True)

    # Pull data from the device using adb
    cmd_pull = ["adb", "pull", "/sdcard", temp_dir]

    def run_imaging():
        try:
            # Pull data from device
            process_pull = subprocess.Popen(cmd_pull, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            for line in process_pull.stdout:
                status_var.set(line.strip())
            
            # Now use dc3dd to create E01 file from pulled data
            e01_output = f"{output_folder}/Android_Backup.E01"
            cmd_dc3dd = ["dc3dd", f"if={temp_dir}/", f"of={e01_output}", "format=raw"]

            process_dc3dd = subprocess.Popen(cmd_dc3dd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            for line in process_dc3dd.stdout:
                status_var.set(f"Creating E01: {line.strip()}")

            process_dc3dd.communicate()

            if process_dc3dd.returncode == 0:
                messagebox.showinfo("Success", "Android storage backup to E01 completed successfully!")
            else:
                messagebox.showerror("Error", "Failed to create E01 image.")
            
            # Clean up the temporary backup folder
            for root, dirs, files in os.walk(temp_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

        except Exception as e:
            messagebox.showerror("Error", f"Backup failed: {e}")

    threading.Thread(target=run_imaging, daemon=True).start()

# GUI Setup
root = tk.Tk()
root.title("Android Storage Backup to E01")
root.geometry("400x300")

device_var = tk.StringVar()
output_var = tk.StringVar()
status_var = tk.StringVar(value="Status: Waiting...")

tk.Label(root, text="Select Device:").pack()
device_menu = tk.OptionMenu(root, device_var, "")
device_menu.pack()
tk.Button(root, text="Refresh Devices", command=refresh_devices).pack()

refresh_devices()

tk.Label(root, text="Output Folder:").pack()
tk.Entry(root, textvariable=output_var, width=40).pack()
tk.Button(root, text="Browse", command=select_output_folder).pack()

tk.Button(root, text="Start", command=start_imaging).pack()
tk.Label(root, textvariable=status_var).pack()

root.mainloop()
