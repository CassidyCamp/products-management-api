# .env fayldan o'zgaruvchilarni o'qish
Get-Content .env | ForEach-Object {
    if ($_ -notmatch '^\s*#' -and $_ -match '^(.*?)=(.*)$') {
        Set-Item -Path Env:$($matches[1]) -Value $matches[2]
    }
}

# uvicornni ishga tushirish
.\.venv\Scripts\python.exe -m uvicorn src.main:app --host $env:HOST --port $env:PORT --reload
