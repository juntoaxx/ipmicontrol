from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine-tuning.
build_exe_options = {
    "packages": ["os", "tkinter", "subprocess", "json"],
    "excludes": [],
}

# Base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI"

setup(
    name="IPMI Control",
    version="1.0",
    description="IPMI Control Application",
    options={"build_exe": build_exe_options},
    executables=[Executable("ipmi_control_app.py", base=base)],
)