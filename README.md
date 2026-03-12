# GrabYT

<p align="center">
  <img src="assets/favicon.svg" alt="GrabYT" width="96" height="96"/>
</p>

Desktop application to download YouTube videos or audio tracks from a file of URLs. PyQt6 interface (borderless windows, pastel theme), backed by yt-dlp.

---

## Features

- **URL file**: a text file (default `urls.txt`) with one YouTube URL per line; lines starting with `#` are ignored. You can choose the file and open it in your default editor directly from the UI.
- **Validation**: before downloading, an initialization step validates all links and displays the total, valid and invalid counts, with a progress bar while scanning.
- **Download**: one-click start once validation is done; detailed progress (current track, percentage, ETA) in a dedicated window; cancellation supported.
- **History**: a window listing past downloads (from `download.json`) with quick access to the YouTube link of each entry.
- **Interface**: custom title bar (move, minimize/restore/close), application icon from `assets/favicon.svg`, rounded tooltips for circular buttons, consistent theme across all windows.
- **Languages**: UI available in French, English, German or Spanish (see `language` in configuration).
- **URL file encoding**: automatic detection of text encoding (UTF-8, UTF-8 BOM, CP1252).
- **Logs**: structured logs (configurable level and optional file), written by default to `log/log.txt`.
- **Update check**: optional check for a new version on startup (JSON URL in config).
- **Batch completion**: system notification (via `notify-py`) showing the percentage of successful downloads; interrupted downloads can be resumed (yt-dlp) and each URL is retried up to 3 times on error.

---

## Usage

1. **Run the application**  
   Executable: `dist\GrabYT-full.exe` or `dist\GrabYT-slim.exe` depending on the build. For development: `python main.py`.

2. **Choose the URL file**  
   The field shows the file in use (default `urls.txt` at the project root). Use “Browse” to select another one. The circular button on the right opens the file in the system default editor.

3. **Initialize**  
   Click “Initialize (count, valid / invalid links)”. URL validation runs and a progress bar shows how far along it is. When finished, statistics (total, valid, invalid) are displayed and the same button becomes “Start download”.

4. **Start the download**  
   Click “Start download”. A progress window opens (current track, percentage, ETA). At the end, a button lets you open the download folder.

5. **History**  
   The circular “History” button (to the right of the main action button) opens the list of past downloads. Clicking a card opens the corresponding YouTube link.

**Requirement (slim build only)**: ffmpeg must be installed and available in PATH. The “full” build bundles ffmpeg (via imageio-ffmpeg) and needs no extra system installation.

---

## Configuration

The `config/config.yaml` file lets you tune:

| Key | Description | Default |
|-----|-------------|---------|
| `app_name` | Title shown in the main window | `GRABYT` |
| `default_urls_file` | Default URL file | `urls.txt` |
| `downloads_dir` | Target folder for downloads | `downloads` |
| `max_concurrent_downloads` | Number of simultaneous downloads | `3` |
| `language` | UI language: `fr`, `en`, `de`, `es` | `fr` |
| `version_check_url` | URL of a JSON `{"version": "x.y.z"}` to notify when a new version is available (empty = disabled) | (empty) |
| `log_level` | Log level: `DEBUG`, `INFO`, `WARNING`, `ERROR` | `INFO` |
| `log_file` | Log file path (empty = console only) | (empty) |

Paths can be relative (to the project root or to the executable directory) or absolute.

---

## Build

Build Windows executables into `dist\`:

```bash
scripts\build\build.bat [--build full|slim]
```

| Option | Description |
|--------|-------------|
| `--build full` (default) | **Portable** exe: bundles imageio-ffmpeg. Heavier, but no ffmpeg installation required. Produces `dist\GrabYT-full.exe`. |
| `--build slim` | **Slim** exe: does not bundle ffmpeg. ffmpeg must be installed on the target machine. Produces `dist\GrabYT-slim.exe`. |

**Full build (full + slim, 4 languages)**: `scripts\packaging\build-all.bat` (Windows) or `scripts/packaging/build-all.sh` (Linux/macOS) runs the full and slim builds, then creates for each language (`fr`, `en`, `de`, `es`) a ready-to-use folder with the exe and a `config/config.yaml` whose language is already set:
- `dist\full-fr`, `dist\full-en`, `dist\full-de`, `dist\full-es`
- `dist\slim-fr`, `dist\slim-en`, `dist\slim-de`, `dist\slim-es`

**Prerequisites**: virtual environment activated, PyInstaller installed (`pip install pyinstaller`). The script calls `scripts/build_icon.py` to generate `assets/icon.ico` from `assets/favicon.svg`; if `icon.ico` is missing, the exe is still built but without a Windows shell icon. The application itself primarily uses `assets/favicon.svg` for the UI icon (windows and title bar).

---

## Project structure

```
grabyt/
  main.py                   # Entry point
  requirements.txt          # Python dependencies
  README.md                 # This file
  config/
    config.yaml             # Configuration (language, logs, version, etc.)
  assets/
    favicon.svg             # Application icon (preferred in UI)
    icon.ico                # Executable icon (generated by build_icon.py)
  src/
    config_loader.py        # Configuration loading
    file_encoding.py        # Text encoding detection (UTF-8 / BOM / CP1252) for the URL file
    i18n.py                 # Translations (FR / EN / DE / ES)
    logger.py               # Structured logging (level, file)
    version.py              # Current version and update check
    core/
      download_manager.py   # Downloads (resume, 3 retries, history)
      downloader.py         # yt-dlp integration
      url_parser.py         # URL file parsing (auto encoding)
      url_validator.py      # URL validation
    ui/
      main_window.py        # Main window
      progress_window.py    # Progress window
      history_window.py     # History window
      title_bar.py          # Custom title bar
      icons.py              # Icons (favicon.svg, icon.ico, internal SVGs)
      rounded_tooltip.py    # Rounded tooltips
      styles.py             # Stylesheets
  scripts/
    build/
      build_icon.py         # Generate icon.ico from favicon.svg
      build_full.spec       # PyInstaller spec (full)
      build_slim.spec       # PyInstaller spec (slim)
      build.spec            # Generic PyInstaller spec
      build.bat             # Windows build script (full or slim)
    packaging/
      prepare_lang_builds.py # Create language-specific full/slim bundles (after build)
      build-all.bat          # Build full + slim then 4-language bundles (Windows)
      build-all.sh           # Build full + slim then 4-language bundles (Linux/macOS)
      zipversion.bat         # Create zip archives in dist\
  dist/                     # Built executables
  build/                    # PyInstaller working directory
  venv/                     # Virtual environment (optional)
```

---

## License

This project is distributed under the **Apache 2.0** license. In short:

- **Use, modification and distribution**: you can use, modify and redistribute the software (including commercially), as long as you keep a copy of the license and copyright notices.
- **Attribution**: redistributions (source or binary) must state any significant changes and include the full license text. You are not required to show “Apache” in your UI.
- **Patents**: contributors grant a license to any patents they hold that are necessarily infringed by their contributions.
- **No warranty**: the software is provided “as is”, without any kind of warranty.

The full text is available in the [LICENSE](LICENSE) file.
