# IPMI Control Application

## Overview
The IPMI Control Application is a graphical user interface (GUI) tool that allows you to manage and control IPMI-enabled machines. You can start, stop, power cycle, and clear the System Event Log (SEL) of the machines. Additionally, you can add, edit, and delete machine configurations.

## Features
- Start, stop, and power cycle IPMI-enabled machines
- Clear the System Event Log (SEL) of machines
- Add, edit, and delete machine configurations
- Edit the IPMI executable path

## Requirements
- Python 3.11
- cx_Freeze
- Inno Setup

## Installation
1. Build the executable using `cx_Freeze`:
   ```
   python setup.py build
   ```
2. Create the installer using Inno Setup:
   ```
   iscc IpmiControl.iss
   ```

## Usage
1. Run the IPMI Control application from the installed location.
2. The main window will display a list of configured machines.

### Commands
- **Start**: Start the selected machines.
- **Stop**: Stop the selected machines.
- **Power Cycle**: Power cycle the selected machines.
- **Clear SEL**: Clear the System Event Log (SEL) of the selected machines.
- **Edit Machine**: Edit the configuration of the selected machine.
- **Add Machine**: Add a new machine configuration.
- **Delete Machine**: Delete the selected machine configuration.

### Selecting Machines
- Click on a machine in the list to select it. You can select multiple machines by holding the `Ctrl` key while clicking.

### Adding a Machine
1. Click the `Add Machine` button.
2. Fill in the machine details (Name, IP Address, Username, Password, IPMI Executable).
3. Click the `Save` button to save the configuration.

### Editing a Machine
1. Select a machine from the list.
2. Click the `Edit Machine` button.
3. Modify the machine details as needed.
4. Click the `Save` button to save the changes.

### Deleting a Machine
1. Select a machine from the list.
2. Click the `Delete Machine` button.
3. Confirm the deletion when prompted.

## Configuration File
The machine configurations are stored in the `machines_config.json` file. This file is automatically created and updated by the application.

## External Softwware Requirements
This is the Dell official link you need this tool to communicate with BMC. My tool sends commands to this executable and it executes and sends them to the machines.
A quick google search multiple sources.
https://www.dell.com/support/home/en-us/drivers/driversdetails?driverid=m63f3

## License
This project is licensed under the MIT License.
