# Blender Runtime Probe
# Probes repo-local blender.exe, bundled Python, and PATH commands.
# Does not install or modify anything.

$ErrorActionPreference = "Continue"
$repo_root = (Get-Location).Path
$timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ss"

"=== Blender Runtime Probe ==="
"  Time: $timestamp"
"  Repo root: $repo_root"
"=== === === === === === ==="
""

# --- Section 1: repo-local blender.exe ---
"--- [1] Repo-local blender.exe ---"
$blender_paths = @(
    "blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\blender.exe",
    "blender\blender-5.1.1\blender-5.1.1\blender.exe"
)

foreach ($bp in $blender_paths) {
    $full = Join-Path $repo_root $bp
    $exists = Test-Path $full
    "  Path: $full"
    "  Exists: $exists"
    if ($exists) {
        $info = Get-Item $full
        "  Size (MB): $([math]::Round($info.Length / 1MB, 2))"
        "  Modified: $($info.LastWriteTime)"

        # Attempt --version
        try {
            $ver_out = & $full --version 2>&1 | Out-String
            if ($LASTEXITCODE -eq 0) {
                "  --version output: $($ver_out.Trim())"
            } else {
                "  --version FAILED (exit code: $LASTEXITCODE)"
                $lines = $ver_out -split "`r?`n" | Where-Object { $_.Trim() } | Select-Object -First 3
                foreach ($line in $lines) { "    $line" }
            }
        } catch {
            "  --version ERRORED: $($_.Exception.Message)"
        }
    }
    ""
}

# --- Section 2: repo-local bundled Python ---
"--- [2] Repo-local bundled Python ---"
$py_exe_path = Join-Path $repo_root "blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\bin\python.exe"
$py_zip_path = Join-Path $repo_root "blender\blender-5.1.1-windows-x64\blender-5.1.1-windows-x64\5.1\python\lib\python313.zip"

$py_exists = Test-Path $py_exe_path
$py_zip_exists = Test-Path $py_zip_path
"  Python exe exists: $py_exists"
"  python313.zip exists: $py_zip_exists"

if ($py_exists) {
    $py_info = Get-Item $py_exe_path
    "  Size (MB): $([math]::Round($py_info.Length / 1MB, 2))"

    # Version check
    $vout = & $py_exe_path --version 2>&1 | Out-String
    "  --version: $($vout.Trim())"

    # Can it import sys?
    $sys_out = & $py_exe_path -S -c "import sys; print(sys.version)" 2>&1 | Out-String
    if ($LASTEXITCODE -eq 0) {
        "  import sys: SUCCESS"
        "  sys.version: $($sys_out.Trim())"
    } else {
        "  import sys: FAILED"
        $err_lines = $sys_out -split "`r?`n" | Where-Object { $_.Trim() } | Select-Object -First 2
        foreach ($l in $err_lines) { "    $l" }
    }

    # Can it import tracking_worker?
    $fw_out = & $py_exe_path -S -m tracking_worker.cli --help 2>&1 | Out-String
    if ($LASTEXITCODE -eq 0) {
        "  import tracking_worker.cli: SUCCESS"
    } else {
        "  import tracking_worker.cli: FAILED"
        $err_lines = $fw_out -split "`r?`n" | Where-Object { $_.Trim() } | Select-Object -First 2
        foreach ($l in $err_lines) { "    $l" }
    }
}
""

# --- Section 3: PATH commands ---
"--- [3] PATH commands ---"
$commands = @("python", "python3", "blender", "ffprobe", "ffmpeg")

foreach ($cmd in $commands) {
    try {
        $resolved = Get-Command $cmd -CommandType Application -ErrorAction Stop
        "  $cmd : $($resolved.Source)"
    } catch {
        "  $cmd : NOT FOUND in PATH"
    }
}
""

# --- Section 4: Test data presence ---
"--- [4] Test data ---"
$test_video = Join-Path $repo_root "test_data\green_field.mp4"
$tv_exists = Test-Path $test_video
"  test_data/green_field.mp4 exists: $tv_exists"
if ($tv_exists) {
    $tv_info = Get-Item $test_video
    "  Size (MB): $([math]::Round($tv_info.Length / 1MB, 2))"
}
""

# --- Section 5: Output directory ---
"--- [5] Output directory ---"
$outputs_dir = Join-Path $repo_root "outputs"
$od_exists = Test-Path $outputs_dir
"  outputs/ exists: $od_exists"
if ($od_exists) {
    $files = Get-ChildItem $outputs_dir -File 2>$null
    if ($files) {
        foreach ($f in $files) {
            "    $($f.Name) ($([math]::Round($f.Length / 1KB, 1)) KB)"
        }
    } else {
        "    (empty)"
    }
}
""

"=== Blender Runtime Probe ==="
"  Probe complete."
"=== === === === === === ==="
