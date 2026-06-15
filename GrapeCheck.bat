@echo off
color 57

:menu
cls
echo    _____                       _____ _               _    
echo   / ____(                     / ____( (             ( (   
echo  ( (  __ _ __ __ _ _ __   ___( (    ( (__   ___  ___( ( __
echo  ( ( (_ ( '__/ _` ( '_ \ / _ \ (    ( '_ \ / _ \/ __( (/ /
echo  ( (__( ( ( ( (_( ( (_) (  __/ (____( ( ( (  __/ (__(   / 
echo   \_____(_(  \__,_( .__/ \___(\_____(_( (_(\___(\___(_(\_\
echo                   ( (                                     
echo                   (_(                                                                                              
echo GrapeCheck Pre-alpha.
echo Copyright (c) 2026 LB-Studio (TM)
echo.

set /p user_input="Enter command (Press "Enter" to see commands): "

if /i "%user_input%"=="run alpha" (
    start cmd /k "python data\py\check.py"
    goto menu
)

if /i "%user_input%"=="exit" (
    exit
)

echo Invalid command. Type "run alpha" or "exit".
pause
goto menu