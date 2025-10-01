# LeetCode Sync - PowerShell wrapper script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir
python lcsync.py $args