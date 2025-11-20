@ECHO off
rem ==============================================================================
rem Sample Batch File
rem ==============================================================================
set CHKPATH="c:\MyCheckerPath\IODD_V1.1.4_Checker.exe"
rem
%CHKPATH% -?
Pause
%CHKPATH% "C:\MyIODDPath\Vendor-DeviceName-20250213-IODD1.1.xml" -s -p -w
Pause
%CHKPATH% "C:\MyIODDPath\Vendor-DeviceName-20250213-IODD1.1-de.xml" -s -p -w
Pause
