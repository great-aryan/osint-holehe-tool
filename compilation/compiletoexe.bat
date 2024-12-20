@echo off

set /p filename=Please enter the file name:

pyinstaller --onefile --noconsole --icon=osint.ico --splash "splashsc.png" %filename%.py

pause