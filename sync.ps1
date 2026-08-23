# 홈페이지 동기화 스크립트 (동기화.bat 이 이 파일을 실행합니다)
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Set-Location -LiteralPath $PSScriptRoot

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   홈페이지 동기화 중... 잠시만 기다리세요" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/3] 다른 PC에서 한 작업 받아오는 중..."
git pull --rebase
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Red
    Write-Host "   잠깐! 양쪽 PC에서 같은 파일을 고쳤습니다" -ForegroundColor Red
    Write-Host "==========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "이건 자동으로 고칠 수 없습니다."
    Write-Host "클로드에게 '동기화하다 충돌났어' 라고 말해주세요."
    Write-Host ""
    exit 1
}
Write-Host "    -> 받기 완료" -ForegroundColor Green
Write-Host ""

Write-Host "[2/3] 이 PC에서 한 작업 저장하는 중..."
git add -A
$changes = (git status --porcelain) -join ""
if ([string]::IsNullOrWhiteSpace($changes)) {
    Write-Host "    -> 새로 바뀐 파일이 없습니다" -ForegroundColor Yellow
} else {
    $stamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    $msgFile = Join-Path $env:TEMP "uengine-sync-msg.txt"
    $enc = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($msgFile, "작업 저장 $stamp", $enc)
    git commit -F $msgFile | Out-Null
    Remove-Item $msgFile -Force -ErrorAction SilentlyContinue
    if ($LASTEXITCODE -ne 0) {
        Write-Host "    -> 저장 실패" -ForegroundColor Red
        exit 1
    }
    Write-Host "    -> 저장 완료" -ForegroundColor Green
}
Write-Host ""

Write-Host "[3/3] 인터넷에 올리는 중..."
git push
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "   올리기 실패 - 인터넷 연결을 확인하고 다시 실행해보세요." -ForegroundColor Red
    Write-Host "   계속 안 되면 클로드에게 알려주세요."
    Write-Host ""
    exit 1
}
Write-Host "    -> 올리기 완료" -ForegroundColor Green
Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "   모두 끝났습니다! 홈페이지에 반영됩니다." -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
