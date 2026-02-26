param(
    [string]$PythonPath = ".\.venv\Scripts\python.exe"
)

if (-not (Test-Path $PythonPath)) {
    Write-Error "Python not found at '$PythonPath'. Pass -PythonPath or create a venv first."
    exit 1
}

$check = & $PythonPath -c "import PyInstaller" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Error "PyInstaller is not installed in this environment. Run: $PythonPath -m pip install pyinstaller"
    exit 1
}

& $PythonPath -m PyInstaller --noconfirm --clean --windowed --onefile --name FileOrganizer file_organizer_v2.py
if ($LASTEXITCODE -ne 0) {
    Write-Error "Build failed."
    exit $LASTEXITCODE
}

Write-Host "Build complete: dist\FileOrganizer.exe"
