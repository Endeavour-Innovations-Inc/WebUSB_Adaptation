@echo off
setlocal
set ScriptHome=%~d0%~p0
set path=%ScriptHome%;%ScriptHome%\..\bin;%path%

rem this example shows how to create a random AES key, encrypt the image
rem program into the target flash, and set the AES key on the target
rem usage: encrypt_and_program  image
if "%1" == "" goto :usage

set binary=%1
set binary_hdr=%binary%.AES.hdr 

rem Generate an aeskey on the target device and assign it to a variable
rem Makes use of the -x option to execute a single command
echo Generating AES key
for /f "delims=" %%a in ('lpcscrypt -x genkeytarget') do set aesKey=%%a
if not %errorlevel% == 0 goto :failed

rem now display that value
echo Generated AES key: %aeskey%

echo
image_manager --key %aeskey% -i %binary% -o %binary_hdr% --bin

lpcscrypt -e s -v "binary_hdr=%binary_hdr%" -v aeskey=%aeskey% -s "%ScriptHome%encrypt_and_program.scy"

if not %errorlevel% == 0 goto :failed
goto :eof

:usage
	echo usage: %0 binary_image
	goto :eof

:failed
	echo script failed
	goto :eof
