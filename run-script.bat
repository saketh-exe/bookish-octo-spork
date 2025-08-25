@echo off
set "ScriptDir=%~dp0"
powershell.exe -File "%ScriptDir%\create-and-open.ps1" "%ScriptDir%"
