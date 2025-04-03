Set WshShell = CreateObject("WScript.Shell")
strPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
Set shortcut = WshShell.CreateShortcut(strPath & "\BlindTest.lnk")
shortcut.TargetPath = "pythonw.exe"
shortcut.Arguments = """" & strPath & "\blind_test.py"""
shortcut.WorkingDirectory = strPath
shortcut.IconLocation = strPath & "\logo.ico"
shortcut.Save

Set shell = CreateObject("Shell.Application")
shell.ShellExecute shortcut.TargetPath, shortcut.Arguments, shortcut.WorkingDirectory, "", 0 