@echo off
REM Script to provide simple CLI to LPCScrypt.exe

setlocal
setlocal enabledelayedexpansion

set version=v2.1.2 Nov 2020

set ScriptHome=%~d0%~p0
set BinHome=%ScriptHome%\..\bin
set path=%ScriptHome%;%ScriptHome%\..\bin;%path%
set ScryptLog=%temp%\Scrypt.log

if /i "%1" == "Help" (
    goto :Usage
)

CLS
echo LPCScrypt - %version% - Command line Environment.
echo.
echo Connect target via USB then press Space.
pause

:while1
echo.

lpcscrypt print 0x1234 2>&1 | findstr /r "1234" >NUL
if %errorlevel% equ 0 goto :Label1

Call boot_lpcscrypt.cmd 
if %errorlevel% equ 1 (
    echo Boot Failed:
    echo Ensure a single LPC18xx or LPC43xx MCU is connected and configured to boot from USB.
    echo.
    goto :end
    )
Call :CheckReady

:Label1
echo.
:ScriptApp
set scrypt_options=-h
set /P scrypt_options=LPCScrypt 
if /i "%scrypt_options%" == "Exit"  (
    goto :end
)
if /i "%scrypt_options%" == "CMSIS"  (
    start program_CMSIS
	set scrypt_options=""
)
if /i "%scrypt_options%" == "JLINK"  (
    start program_JLINK
	set scrypt_options=""
)

REM lpcscrypt %scrypt_options% > %ScryptLog% 2>&1
lpcscrypt %scrypt_options%
if %errorlevel% equ 0 (
    echo Successful
) else (
    echo Error
)

goto :while1

:Usage
    echo Usage:
    echo Connect an LPC18xx or LPC43xx MCU configured to DFU-Boot from USB.
    echo This script will boot LPCScrypt and then process LPCScrypt commands.
    goto :end

:end
    endlocal
    pause
    goto :eof

:CheckReady
    timeout /T 1 >NUL
    echo | set /p none=.
    lpcscrypt print 0x1234 2>&1 | findstr /r "1234" >NUL
    REM echo  %errorlevel%  
    if %errorlevel% equ 1 goto :CheckReady
    goto :eof

:eof
