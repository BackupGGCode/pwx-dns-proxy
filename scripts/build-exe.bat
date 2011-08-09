set PATH=C:\bin\pyinstaller-1.5.1;%PATH%
cd ..
Makespec.py --onefile --out=win32 --name=dnsproxy --console src/dnsproxy.py
Build.py win32/dnsproxy.spec