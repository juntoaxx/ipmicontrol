[Setup]
AppName=IPMI Control
AppVersion=1.0
DefaultDirName={pf}\IPMI Control
DefaultGroupName=IPMI Control
OutputDir=.
OutputBaseFilename=IPMIControlInstaller

[Files]
Source: "build\exe.win-amd64-3.11\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "machines_config.json"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\IPMI Control"; Filename: "{app}\ipmi_control_app.exe"