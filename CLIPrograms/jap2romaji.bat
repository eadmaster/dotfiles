@echo off
setlocal

REM TODO: fix unicode output
chcp 65001  > NUL

kagome -json | jq -r ".[].pronunciation" | call busybox paste -sd' ' - | uconv -f utf-8 -t utf-8 -x "Any-Latin;Latin-ASCII"

REM TODO: merge lines, keep parenthesis  (e.g. echo "[34:34:34]ローマ字変換プログラム" | ...)
REM kagome -json | jq -r ".[].pronunciation | join(\".\")" | uconv -f utf-8 -t utf-8 -x "Any-Latin;Latin-ASCII"
