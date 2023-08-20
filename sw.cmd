@echo off

REM Student Welfare Backend
if "%1" == "local" (
    shift
    set "env=local"
    set "file=local.yml"
) else (
    set "env=production"
    set "file=production.yml"
)

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%student_welfare_backend\" && docker-compose -f "%file%" %*
