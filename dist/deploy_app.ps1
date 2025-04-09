$projectRoot = Join-Path (Split-Path -Parent $PSScriptRoot) ""
Set-Location -Path $projectRoot

$pythonPath = Join-Path $projectRoot "python39\python.exe"

if (-not (Test-Path $pythonPath)) {
    Write-Host "找不到python3.9, 文件可能已损坏，请重新下载。"
    exit 1
}

& $pythonPath -m pip install uv

Write-Host "正在创建虚拟环境..."
& $pythonPath -m uv venv create --python $pythonPath

& "$projectRoot\.venv\Scripts\Activate.ps1"

& $pythonPath -m uv pip install -r requirements.txt

& $pythonPath -m uv pip install pyinstaller

$mainPath = Join-Path $projectRoot "src\main.py"
$distPath = Join-Path $projectRoot "dist"
pyinstaller --onefile --windowed --distpath $distPath $mainPath

Write-Host "已在项目的dist文件夹下创建main.exe文件。"