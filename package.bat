IF EXIST "dist" RMDIR /S /Q "dist"
IF EXIST "build" RMDIR /S /Q "build"
IF EXIST "choose.spec" DEL /F /Q "choose.spec"
IF EXIST "choose.exe" DEL /F /Q "choose.exe"
IF EXIST "choose.onefile-build" RMDIR /S /Q "choose.onefile-build"
IF EXIST "choose.build" RMDIR /S /Q "choose.build"
IF EXIST "choose.dist" RMDIR /S /Q "choose.dist"
IF EXIST "__pycache__" RMDIR /S /Q "__pycache__"
IF %1 == "--nuitka" (
    IF %2 == "--onefile" (
        python -m nuitka --follow-imports --standalone --enable-plugin=tk-inter --include-data-dir=assets=assets --windows-icon-from-ico=./assets/bg_cs_r_00.ico --show-progress --windows-console-mod=disable choose.py
    ) ELSE (
        python -m nuitka --follow-imports --standalone --enable-plugin=tk-inter --include-data-dir=assets=assets --windows-icon-from-ico=./assets/bg_cs_r_00.ico --show-progress choose.py
    )
)ELSE IF %1 == "--pyinstaller" (
    IF %2 == "--onefile" (
        pyinstaller --noconfirm --onefile --windowed --icon=./assets/bg_cs_r_00.ico --add-data "assets;assets" choose.py
    ) ELSE (
        pyinstaller --noconfirm --windowed --icon=./assets/bg_cs_r_00.ico --add-data "assets;assets" choose.py
    )
) ELSE (
    echo Invalid argument. Use --nuitka or --pyinstaller.
)