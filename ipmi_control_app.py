import tkinter as tk
from tkinter import messagebox
from tkinter import ttk, filedialog
import subprocess
import json
import os

CONFIG_FILE = "machines_config.json"

class IPMIControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("IPMI Control")
        self.root.geometry("500x300")  # Reduce the size of the window

        self.load_configurations()

        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=0)

        # Machine List
        self.machine_listbox = tk.Listbox(root, font=("Helvetica", 12), width=40, height=10, selectmode=tk.MULTIPLE)
        self.machine_listbox.grid(row=0, column=0, columnspan=4, padx=20, pady=10, sticky="nsew")
        self.machine_listbox.bind('<<ListboxSelect>>', self.on_machine_select)

        self.refresh_machine_list()

        # Buttons
        button_font = ("Helvetica", 12)
        self.start_button = ttk.Button(root, text="Start", command=self.start_servers)
        self.start_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_servers)
        self.stop_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.cycle_button = ttk.Button(root, text="Power Cycle", command=self.power_cycle_servers)
        self.cycle_button.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
        self.clear_button = ttk.Button(root, text="Clear SEL", command=self.clear_sel_servers)
        self.clear_button.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        self.settings_button = ttk.Button(root, text="Edit Machine", command=self.open_settings)
        self.settings_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        self.add_button = ttk.Button(root, text="Add Machine", command=self.add_machine)
        self.add_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.delete_button = ttk.Button(root, text="Delete Machine", command=self.delete_machine)
        self.delete_button.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

        self.selected_machines = []
        self.ipmi_executable = self.machines.get("ipmi_executable", "C:\ipmi\ipmitool.exe")

    def load_configurations(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as file:
                self.machines = json.load(file)
        else:
            self.machines = {}

    def save_configurations(self):
        with open(CONFIG_FILE, 'w') as file:
            json.dump(self.machines, file)

    def refresh_machine_list(self):
        self.machine_listbox.delete(0, tk.END)
        for machine_name in self.machines.keys():
            if machine_name != "ipmi_executable":
                self.machine_listbox.insert(tk.END, machine_name)

    def on_machine_select(self, event):
        selection = event.widget.curselection()
        self.selected_machines = [event.widget.get(i) for i in selection]

    def run_command(self, command):
        try:
            subprocess.run(command, check=True, shell=True)
            messagebox.showinfo("Success", "Command executed successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to execute command: {e}")

    def start_servers(self):
        for machine_name in self.selected_machines:
            machine = self.machines[machine_name]
            command = f'start "" {self.ipmi_executable} -H {machine["ip"]} -U {machine["user"]} -P {machine["password"]} -I lanplus chassis power on'
            self.run_command(command)

    def stop_servers(self):
        for machine_name in self.selected_machines:
            machine = self.machines[machine_name]
            command = f'start "" {self.ipmi_executable} -H {machine["ip"]} -U {machine["user"]} -P {machine["password"]} -I lanplus chassis power off'
            self.run_command(command)

    def power_cycle_servers(self):
        for machine_name in self.selected_machines:
            machine = self.machines[machine_name]
            command = f'start "" {self.ipmi_executable} -H {machine["ip"]} -U {machine["user"]} -P {machine["password"]} -I lanplus chassis power cycle'
            self.run_command(command)

    def clear_sel_servers(self):
        for machine_name in self.selected_machines:
            machine = self.machines[machine_name]
            command = f'start "" {self.ipmi_executable} -H {machine["ip"]} -U {machine["user"]} -P {machine["password"]} -I lanplus sel clear'
            self.run_command(command)

    def open_settings(self):
        if not self.selected_machines:
            messagebox.showerror("Error", "No machine selected.")
            return
        self.open_machine_settings(self.machines[self.selected_machines[0]], self.selected_machines[0])

    def add_machine(self):
        self.open_machine_settings()

    def delete_machine(self):
        if not self.selected_machines:
            messagebox.showerror("Error", "No machine selected.")
            return
        for machine_name in self.selected_machines:
            if messagebox.askyesno("Delete Machine", f"Are you sure you want to delete {machine_name}?"):
                del self.machines[machine_name]
        self.save_configurations()
        self.refresh_machine_list()
        self.selected_machines = []

    def open_machine_settings(self, machine=None, original_name=None):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")  # Increase the size of the settings window

        label_font = ("Helvetica", 12)
        entry_font = ("Helvetica", 12)

        tk.Label(settings_window, text="Machine Name", font=label_font).grid(row=0, column=0, padx=10, pady=10)
        machine_name_entry = ttk.Entry(settings_window, font=entry_font)
        machine_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(settings_window, text="IP Address", font=label_font).grid(row=1, column=0, padx=10, pady=10)
        ip_entry = ttk.Entry(settings_window, font=entry_font)
        ip_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(settings_window, text="Username", font=label_font).grid(row=2, column=0, padx=10, pady=10)
        user_entry = ttk.Entry(settings_window, font=entry_font)
        user_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(settings_window, text="Password", font=label_font).grid(row=3, column=0, padx=10, pady=10)
        pass_entry = ttk.Entry(settings_window, show="*", font=entry_font)
        pass_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(settings_window, text="IPMI Executable", font=label_font).grid(row=4, column=0, padx=10, pady=10)
        ipmi_executable_entry = ttk.Entry(settings_window, font=entry_font)
        ipmi_executable_entry.grid(row=4, column=1, padx=10, pady=10)
        ipmi_executable_entry.insert(0, self.ipmi_executable)

        def browse_ipmi_executable():
            file_path = filedialog.askopenfilename(title="Select IPMI Executable", filetypes=[("Executable Files", "*.exe")])
            if file_path:
                ipmi_executable_entry.delete(0, tk.END)
                ipmi_executable_entry.insert(0, file_path)

        browse_button = ttk.Button(settings_window, text="Browse", command=browse_ipmi_executable)
        browse_button.grid(row=5, column=0, padx=10, pady=10)

        def save_machine():
            machine_name = machine_name_entry.get()
            ip = ip_entry.get()
            user = user_entry.get()
            password = pass_entry.get()
            ipmi_executable = ipmi_executable_entry.get()
            if machine_name and ip and user and password:
                if original_name and machine_name != original_name:
                    del self.machines[original_name]
                self.machines[machine_name] = {"ip": ip, "user": user, "password": password}
                self.machines["ipmi_executable"] = ipmi_executable
                self.ipmi_executable = ipmi_executable
                self.save_configurations()
                self.refresh_machine_list()
                settings_window.destroy()
            else:
                messagebox.showerror("Error", "All fields are required.")

        save_button = ttk.Button(settings_window, text="Save", command=save_machine)
        save_button.grid(row=5, column=1, padx=10, pady=10)

        if machine:
            machine_name_entry.insert(0, original_name)
            ip_entry.insert(0, machine.get("ip", ""))
            user_entry.insert(0, machine.get("user", ""))
            pass_entry.insert(0, machine.get("password", ""))

if __name__ == "__main__":
    root = tk.Tk()
    app = IPMIControlApp(root)
    root.mainloop()
