pip3 install pyinstaller
New-Item -ItemType Directory -Force -Path export
Set-Location export
Copy-Item -Path ..\sfx -Destination .\dist -Force -Recurse
Copy-Item -Path ..\FFFFORWA.TTF -Destination .\dist -Force
python3 -m PyInstaller ..\main.py --onefile --noconsole
Set-Location ..