@echo off
setlocal
if not exist content mkdir content

echo [?] Checking for compilers...

where cl >nul 2>nul
if %errorlevel% equ 0 goto use_cl

where g++ >nul 2>nul
if %errorlevel% equ 0 goto use_gpp

where clang++ >nul 2>nul
if %errorlevel% equ 0 goto use_clang

echo [-] No compiler found.
exit /b 1

:use_cl
echo [+] Found MSVC. Compiling...
cl /EHsc /Fe:content/LicenseVM.exe main.cpp
if %errorlevel% equ 0 goto success
goto fail

:use_gpp
echo [+] Found G++. Compiling...
g++ -o content/LicenseVM.exe main.cpp
if %errorlevel% equ 0 goto success
goto fail

:use_clang
echo [+] Found Clang++. Compiling...
clang++ -o content/LicenseVM.exe main.cpp
if %errorlevel% equ 0 goto success
goto fail

:success
echo [+] Build successful: content/LicenseVM.exe
exit /b 0

:fail
echo [-] Compilation failed.
exit /b 1
