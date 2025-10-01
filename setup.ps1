# LeetCode Sync Setup Script for Windows PowerShell

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

# Test the installation
Write-Host "🧪 Testing installation..." -ForegroundColor Yellow
& python lcsync.py help

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Quick usage:" -ForegroundColor Cyan
Write-Host "  lcsync init      # Initialize project"
Write-Host "  lcsync user      # Set up user"
Write-Host "  lcsync cookie    # Add LeetCode session"
Write-Host "  lcsync fetch     # Fetch submissions"
Write-Host "  lcsync push      # Push to GitHub"
Write-Host ""
Write-Host "💡 Alternative methods:" -ForegroundColor Yellow
Write-Host "  python lcsync.py <command>    # Direct Python"
Write-Host "  .\lcsync.ps1 <command>        # PowerShell script"