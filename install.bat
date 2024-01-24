@echo off

:: Exit if embedded python is not found
if not exist ..\..\..\python_embeded\python.exe (
    echo Embedded python folder not found.
    echo Please check you placed this respitory in correct folder you should run it from ./ComfUI/custom_nodes/InstaSwapComfyUINode/
    pause
    exit /b 1
)

:: Install the packages
..\..\..\python_embeded\python.exe install.py
@pause
