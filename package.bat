@ECHO OFF
IF EXIST "dist" RMDIR /S /Q "dist"
IF EXIST "build" RMDIR /S /Q "build"
IF EXIST "choose.spec" DEL /F /Q "choose.spec"
IF EXIST "choose.exe" DEL /F /Q "choose.exe"
IF EXIST "choose.onefile-build" RMDIR /S /Q "choose.onefile-build"
IF EXIST "choose.build" RMDIR /S /Q "choose.build"
IF EXIST "choose.dist" RMDIR /S /Q "choose.dist"
IF EXIST "__pycache__" RMDIR /S /Q "__pycache__"
IF "%1" == "--nuitka" (
    IF "%2" == "--onefile" (
        python -m nuitka --follow-imports --standalone --enable-plugin=tk-inter --include-data-dir=assets=assets --windows-icon-from-ico=./assets/favicon.ico --windows-console-mod=disable --product-version=1.0.2 --company-name=hanhan_boy --onefile choose.py
    ) ELSE (
        python -m nuitka --follow-imports --standalone --enable-plugin=tk-inter --include-data-dir=assets=assets --windows-icon-from-ico=./assets/favicon.ico --windows-console-mod=disable --product-version=1.0.2 --company-name=hanhan_boy choose.py
    )
)ELSE IF "%1" == "--pyinstaller" (
    IF "%2" == "--onefile" (
        pyinstaller --clean --noconfirm --onefile --windowed --icon=./assets/favicon.ico --add-data "assets;assets" choose.py
    ) ELSE (
        pyinstaller --clean --noconfirm --windowed --icon=./assets/favicon.ico --add-data "assets;assets" choose.py
    )
) ELSE (
    echo Invalid argument. Use --nuitka or --pyinstaller.
)