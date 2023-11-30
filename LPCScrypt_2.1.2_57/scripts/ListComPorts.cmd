@echo off
set GET=Name
if "%1" == "-v" set GET=Name,PnpDeviceId
wmic path Win32_PnPEntity where (service like "%%ser%%") get %GET%
