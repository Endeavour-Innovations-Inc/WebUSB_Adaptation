@echo off
setlocal
set ScriptHome=%~d0%~p0
set path=%ScriptHome%;%ScriptHome%\..\bin;%path%

rem this example shows how to assign the output of a command to a variable
rem usage: aeskey 
if "%1" == "" goto :usage

rem Generate an aeskey on the target device and assign it to a variable
rem Makes use of the -x option to execute a single command
rem This strange command just assigns the output of a command to a variable
for /f "delims=" %%a in ('lpcscrypt -x genkeytarget') do set aesKey=%%a
rem now display that value
echo Generated AES key: %aesKey%
goto :eof

:usage
echo usage %0 device
