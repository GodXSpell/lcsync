# LeetCode Sync Setup Sc# Create universal command file that works in both CMD and PowerShell
Write-Host "🔧 Creating universal command wrapper..." -ForegroundColor Yellow

$cmdContent = '@echo off
python "%~dp0lcsync.py" %*'
Set-Content -Path "lcsync.cmd" -Value $cmdContent -Encoding ASCII
Write-Host "✅ Created lcsync.cmd (works in CMD and PowerShell)" -ForegroundColor Green

# Clean up conflicting files if they exist
if (Test-Path "lcsync.ps1") { Remove-Item "lcsync.ps1" -Force }
if (Test-Path "lcsync.bat") { Remove-Item "lcsync.bat" -Force }
Write-Host "🧹 Cleaned up conflicting script files" -ForegroundColor Grayor Windows PowerShell

Write-Host "🚀 Setting up LeetCode Sync (lcsync) for Windows..." -ForegroundColor Green

# Check if Python is available
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Python not found. Please install Python from python.org" -ForegroundColor Red
    exit 1
}

# Install Python dependencies
if (Test-Path "requirements.txt") {
    Write-Host "📦 Installing Python dependencies..." -ForegroundColor Yellow
    & python -m pip install -r requirements.txt
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
}
else {
    Write-Host "⚠️  requirements.txt not found" -ForegroundColor Yellow
}

# Create universal .cmd file that works in both CMD and PowerShell
Write-Host "🔧 Creating universal command wrapper..." -ForegroundColor Yellow
$cmdContent = '@echo off
python "%~dp0lcsync.py" %*'
Set-Content -Path "lcsync.cmd" -Value $cmdContent -Encoding ASCII
Write-Host "✅ Created lcsync.cmd (works in CMD and PowerShell)" -ForegroundColor Green

# Test the installation
Write-Host "🧪 Testing installation..." -ForegroundColor Yellow
& python lcsync.py help

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Available command options:" -ForegroundColor Cyan
Write-Host "  lcsync init                   # Universal (CMD/PowerShell)" -ForegroundColor White  
Write-Host "  python lcsync.py init         # Direct Python (all platforms)" -ForegroundColor White
Write-Host "  .\lcsync.sh init              # Mac/Linux (after chmod +x)" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 If 'lcsync' command not found:" -ForegroundColor Yellow
Write-Host "  - In CMD: Use 'lcsync.cmd' or 'python lcsync.py'" -ForegroundColor White
Write-Host "  - In PowerShell: Use '.\lcsync.cmd' or 'python lcsync.py'" -ForegroundColor White
Write-Host "  - To enable 'lcsync' globally, add this folder to your PATH" -ForegroundColor White
Write-Host ""
Write-Host "🔧 To add to PATH (optional):" -ForegroundColor Cyan
Write-Host "  1. Copy this path: $((Get-Location).Path)" -ForegroundColor Gray
Write-Host "  2. Add to Windows PATH environment variable" -ForegroundColor Gray
Write-Host "  3. Restart terminal, then 'lcsync' will work from anywhere" -ForegroundColor Gray
Write-Host ""
Write-Host "🚀 Next step: Run 'lcsync init' (or '.\lcsync.cmd init') to initialize the tool" -ForegroundColor Green