Set WshShell = CreateObject("WScript.Shell")
strPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

' Créer le raccourci
Set shortcut = WshShell.CreateShortcut(WshShell.SpecialFolders("Programs") & "\Blind Test\BlindTest.lnk")
shortcut.TargetPath = "pythonw.exe"
shortcut.Arguments = """" & strPath & "\blind_test.py"""
shortcut.WorkingDirectory = strPath
shortcut.IconLocation = strPath & "\logo.ico"
shortcut.Description = "Application de Blind Test Musical"
shortcut.Save

MsgBox "Le raccourci a été installé dans le menu démarrer !", 64, "Installation terminée" 