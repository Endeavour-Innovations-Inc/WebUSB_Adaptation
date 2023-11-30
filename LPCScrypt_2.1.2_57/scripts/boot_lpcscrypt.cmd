@echo off
setlocal
setlocal enabledelayedexpansion
set ScriptHome=%~d0%~p0
set BinHome=%ScriptHome%\..\bin
set path=%ScriptHome%;%ScriptHome%\..\bin;%path%
set exitval=0

set DeviceName=LPCScrypt target
set BootImageWild=LPCScrypt*.hdr 
set DfuLog=%temp%\dfu-util.log
call :getDfuVidPid
if "%DfuVidPid%" == "" goto :NoDfus

if "%1" == "" (
	call :getBootImage
) else (
	set BootImage=%1
) 

if "%BootImage%" == "" goto :NoBootImage

:DfuApp
for %%i in (%BootImage%) do set ShortBootImage="%%~nxi"
echo Booting %DeviceName% with %ShortBootImage%
set boot_options=-d 0x1fc9:c -c 0 -i 0 -t 2048 -R -D "%BootImage%"

dfu-util %boot_options% >NUL 2>%DfuLog%
if %errorlevel% equ 0 (
  echo %DeviceName% booted
) else (
  echo %DeviceName% boot failed:
  type %DfuLog%
  set exitval=3
)
goto :end

:Usage
echo Usage: %0
goto :end

:end
exit /b %exitval%

:NoDfus
echo Nothing to boot!
set exitval=1
goto :end

:NoBootImage
echo No boot image found
set exitval=2
goto :end

:getDfuVidPid
for /f "skip=6 tokens=3" %%a in ('dfu-util -l') do (
  set DfuVidPid=%%a
)
:eof

:getBootImage
for /r "%BinHome%" %%f in (%BootImageWild%) do (
  set BootImage=%%f
)
:eof

