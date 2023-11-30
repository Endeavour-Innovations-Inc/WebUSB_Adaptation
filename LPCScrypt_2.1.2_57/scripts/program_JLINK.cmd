@echo off
REM Script to autodetect then program J-Link image onto LPC-Link2 or LPCXpresso V2/V3 board
REM Arguments: Null, Path to binary, Help

setlocal
setlocal enabledelayedexpansion

set version=v2.1.2 Nov 2020

set ScriptHome=%~d0%~p0
set BinHome=%ScriptHome%\..\bin
REM set Home=%ScriptHome%\..\probe_firmware\LPCLink2
set path=%ScriptHome%;%ScriptHome%\..\bin;%path%
set ScryptLog=%temp%\Scrypt.log

if /i "%1" == "Help" (
    goto :Usage
)

REM Opening Banner
CLS
echo LPCScrypt - J-Link firmware programming script %version%.
echo.
echo Connect an LPC-Link2 or LPCXpresso V2/V3 Board via USB then press Space.

:while1
echo.
pause
echo.

REM check to see if part already booted
lpcscrypt print 0x1234 2>&1 | findstr /r "1234" >NUL
if %errorlevel% equ 0 goto :label1

REM call external boot command
Call boot_lpcscrypt.cmd 
if %errorlevel% equ 1 (
    echo Boot Failed:
    echo Ensure One Debug Probe is configured to DFU-Boot and connected via USB.
    echo  - For LPC-Link2: remove link JP1 ^(nearest USB^) and power cycle
    echo  - For LPCXpresso V2/V3: make DFU link and power cycle
    echo.
    goto :end
    )

:label1
Call :CheckReady
echo.
Call :CheckPart

if /i "%Part%" == "Link2" (
    set Link2Home=%ScriptHome%\..\probe_firmware\LPCLink2
    set DeviceName= LPC-Link2
    set Flash= SPIFI
    if /i "%1" == "" (
        set Link2ImageWild=Firmware_JLink_LPC-Link2_*.bin
    )
    call :getLink2Image
)

if /i "%Part%" == "Lpcx" (
    set Link2Home=%ScriptHome%\..\probe_firmware\LPCXpressoV2
    set DeviceName= LPCXpresso V2/V3
    set Flash= BANKA
    if /i "%1" == "" (
        set Link2ImageWild=Firmware_JLink_LPCXpressoV2_*.bin
    )
    call :getLink2Image
)

REM if no match, %1 may contain path to image, but flash type won't be set

if "%Link2Image%" == "" set Link2Image=%1
if "%Link2Image%" == "" goto :NoLink2Image

REM echo %Link2Image%

:ScriptApp
REM get actual filename
for %%i in (%Link2Image%) do set ShortLink2Image="%%~nxi"

echo Programming%DeviceName% with %ShortLink2Image%
set scrypt_options=program "%Link2Image%" %Flash%
call :ProgramPart

echo Connect Next Board then press Space (or CTRL-C to Quit)
goto :while1

:Usage
    echo Usage:
    echo Connect a LPC-Link2 or LPCXpresso debug probe configured to DFU-Boot.
    echo This script will program the probe with the J-Link image.
    echo The following arguments are accepted:
    echo                 [Programs JLink Image]
    echo "path to bin"   [Programs the chosen binary]
    goto :end

:end
    endlocal
    pause
    goto :eof

:NoLink2Image
    echo No Probe image found
    goto :Usage

:getLink2Image
    for /r "%Link2Home%" %%f in (%Link2ImageWild%) do (
        set Link2Image=%%f
    )
    goto :eof

:CheckPart
    lpcscrypt querypart | findstr /r "LPC43.0" >NUL
    if %errorlevel% equ 0 set Part=Link2
    if %errorlevel% equ 1 set Part=Lpcx
    REM echo %Part%
    goto :eof

:CheckReady
    timeout /T 1 >NUL
    echo | set /p none=.
    lpcscrypt print 0x1234 2>&1 | findstr /r "1234" >NUL
    REM echo  %errorlevel%  
    if %errorlevel% equ 1 goto :CheckReady
    goto :eof

:ProgramPart
    SET LOOP=0        
:progloop
    lpcscrypt %scrypt_options% >NUL 2>%ScryptLog%
    if %errorlevel% equ 0 goto :progsuccess
    type %ScryptLog%
    echo
    echo Retrying ...
    SET /A LOOP+=1
    if "%LOOP%" == "2" goto :progloopend
    goto :progloop
	
:progloopend
    echo Slowing clock ...
    lpcscrypt clockslow
    lpcscrypt %scrypt_options%
    if %errorlevel% equ 0 goto :progsuccess
    echo.
    echo Programming %Link2Image% to %Flash% has failed!
    goto :eof

:progsuccess
    echo.
    echo %DeviceName% programmed successfully: 
    if /i "%Part%" == "Link2" echo - To use: make link JP1 ^(nearest USB^) and reboot.
    if /i "%Part%" == "Lpcx"  echo - To use: remove DFU link and reboot.
    echo.
    goto :eof

:eof

