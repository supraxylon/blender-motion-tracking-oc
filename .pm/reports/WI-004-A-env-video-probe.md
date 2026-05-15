# WI-004-A - Environment and Video Probe

## Works

### Python
- `python` -> Python 3.12.10 (Windows Store build)
  - Path: `C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\python.exe`
- `pip` -> pip 25.0.1 (bundled with Python 3.12)
- `pip3` -> pip 25.0.1 (same install)
- `py` -> NOT found
- `python3` -> NOT found

### Video test data
- `test_data/green_field.mp4` exists (296,359,286 bytes ~283 MB)
- Pure-Python MP4 probe works (no external deps needed):
  - Box type: `ftyp`
  - Brand/vendor: `isom` (ISO Base Media v1)
  - Contains `moov`, `free`, `mdat` boxes
  - Container: MP4 (ISO 14496-12)

### Module imports (all absent, but Python can test them)
- `import MMPose` -> No (not installed)
- `import torch` -> No (not installed)
- `import cv2` -> No (not installed)

## Does not work

### ffprobe / ffmpeg
- `ffprobe` -> NOT found in PATH
- `ffmpeg` -> NOT found in PATH
- No obvious Windows alternative discovered (Chocolatey/msys2 paths not tested)

### Blender
- `blender` / `blender.exe` -> NOT found in PATH
- No Blender installation detected in:
  - `C:\Program Files\Blender Foundation\`
  - `$env:LOCALAPPDATA\Programs\`
  - Standard WindowsApps / Programs locations
- Blender bundled Python was NOT found (no `bl_launcher.py` or embedded Python)

### Libraries
- MMPose -> Not installed
- torch -> Not installed
- cv2 (OpenCV) -> Not installed

## Blockers

1. **Blender not installed or not in PATH** - Cannot verify Blender launch or access bundled Python (which includes numpy, bpy, etc.)
2. **ffprobe/ffmpeg not available** - Cannot read video metadata (codec, resolution, FPS, duration) easily. Pure-Python MP4 box parsing confirms container type but not codec info.
3. **No Python packages installed** - Clean environment; torch, opencv-python, MMPose all need pip install
4. **Windows Store Python** - May have restricted site-packages; `pip` works but some compiled packages (cv2, torch) may need special wheel URLs (CUDA vs CPU, ABI tags)

## Recommended next command

```
choco install blender ffmpeg 2>&1; if ($LASTEXITCODE -ne 0) { winget install Blender.Blender; winget install Gyan.FFmpeg }
```

Fallback if Chocolatey/Winget unavailable:
```
# 1. Install Blender to C:\Program Files\Blender Foundation\Blender 4.x\
#    Then add to PATH or use full path to verify:
& "C:\Program Files\Blender Foundation\Blender 4.x\4.x\blender.exe" --version

# 2. Verify Blender bundled Python:
& "C:\Program Files\Blender Foundation\Blender 4.x\4.x\blender.exe" -b --python-expr "import sys; print(sys.executable); import bpy; print('bpy OK')"

# 3. Install FFmpeg (standalone or via Blender's bundled ffmpeg at datafiles/ffmpeg/)
# 4. Then probe video metadata:
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,duration -of default=noprint_wrappers=1 test_data/green_field.mp4
```

If preferring no-system-install approach, the next minimal step is:
```
pip install opencv-python
```
Then use cv2 to read video properties instead of ffprobe.
