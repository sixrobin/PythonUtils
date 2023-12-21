import os
import sys
import winreg as reg

cwd = os.getcwd()
python_exe = sys.executable
KEY_PATH = r'Directory\\Background\\shell\\unity_utils\\'

key1 = reg.CreateKeyEx(reg.HKEY_CLASSES_ROOT, KEY_PATH)
reg.SetValue(key1, '', reg.REG_SZ, '&Unity Files Scan')

key2 = reg.CreateKeyEx(key1, r'command')
reg.SetValue(key2, '', reg.REG_SZ, python_exe + f' "{cwd}\\unity_files_scan.py"')
