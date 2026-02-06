# AGENTS.md - Session Handoff for `SABnzbPPS`

Use this file to bootstrap a new AI session without losing project context.

## Scope
- Repository: `SABnzbPPS`
- Purpose: Post-processing and manual reencode pipeline using HandBrake + ffprobe.
- Runtime target: Windows deployment.
- Current working environment in this workspace may be macOS for editing/testing file layout.

## Project Summary
- `.bat` scripts receive paths from download clients and write queue/input text files.
- `.py` scripts read those text files, inspect media with `ffprobe`, encode with `HandBrakeCLI`, and optionally call Sonarr/Radarr.
- Manual mode uses `Shrink.bat` + `Shrink.py` and does not call APIs.

## Expected Structure
- `App/`:
  - `HandBrakeCLI.exe`
  - `ffprobe.exe`
- `Presets/`:
  - `SuperShrinkHD.json`
  - `SuperShrink4K.json`
- `TXT/`: script input lists
- `ReEncodedFiles/`: output media
- `Log/`: runtime logs

## Script Mapping
- SABnzbd flow:
  - `Movies.bat` -> `Movies.py` (Radarr)
  - `TVShows.bat` -> `TVShows.py` (Sonarr)
- qBittorrent flow:
  - `Torrent.bat` -> `Torrents.py`
- Manual flow:
  - `Shrink.bat` -> `Shrink.py`

## Client Input Conventions
- SAB scripts typically rely on first arg (final path) and ignore extra args.
- qBittorrent run-program format should pass path + category.
- `Torrents.py` category mapping is strict unless updated in code (`Movies`, `Shows`).

## Output and Logging
- Reencoded outputs go to `ReEncodedFiles/`.
- Log naming pattern: `Log/encode_log_YYYYMMDD_HHMMSS.txt`.
- `.gitignore` currently ignores:
  - `Log/`
  - `ReEncodedFiles/`
  - `__pycache__/`
  - `*.pyc`

## Working Rules for Future Sessions
- Keep behavior stable unless requested; do not change script interfaces casually.
- Preserve Windows compatibility when editing on macOS.
- Prefer minimal, targeted changes and keep script names/entry points unchanged.
- When changing automation behavior, update both implementation and docs/wiki notes.
- Avoid embedding secrets/tokens in tracked files.

## Open/Useful Validation Checklist
1. Confirm required binaries exist in `App/`.
2. Confirm preset files exist in `Presets/`.
3. Confirm input TXT files are created by `.bat` scripts.
4. Confirm Python scripts resolve paths correctly and process folder recursion as expected.
5. Confirm logs are written and include command/error details.
6. Confirm category mapping for torrents matches actual client labels.

## Copy/Paste Bootstrap Prompt for New Session
Use the block below at the start of a new chat:

```text
You are resuming work on the `SABnzbPPS` project.
Read `SABnzbPPS/AGENTS.md` first and follow it as the session handoff.
Constraints:
- Preserve existing script behavior unless I explicitly ask to change it.
- Keep changes Windows-compatible.
- Make minimal, targeted edits and explain exactly what changed.
- If changing workflow behavior, update docs accordingly.
Current goal for this session: <replace with your goal>
```

## Notes
- If this repo is moved to another machine/session, this file is intended to restore context quickly.
- If workflow rules change, update this file first so future sessions stay aligned.
