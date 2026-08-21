# Windows PowerShell wrapper for sync_agent_template.py
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PyScript = Join-Path $ScriptDir "sync_agent_template.py"

python $PyScript @args
exit $LASTEXITCODE
