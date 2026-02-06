# Copilot instructions for Quarm NPC Overlay

## Big picture
- Single-app Python overlay with three core pieces: log watcher, SQLite NPC resist DB, and Tkinter GUI, all in eq_resist_overlay.py.
- Data flow: EverQuest log line -> regex parse (consider output) -> normalize NPC name (spaces→underscores, lower-case) -> SQLite lookup -> GUI update.
- DB is built from npc_types.sql into npc_data.db; app creates and populates DB on first run if empty.

## Key files to know
- eq_resist_overlay.py: main entry, ConfigManager, EQResistDatabase, EQLogWatcher, and GUI (ResistOverlayGUI).
- npc_types.sql: source data for NPC resist values.
- load_db.py: helper to load npc_types.sql into dist/npc_data.db (used for packaged builds).
- EQ_Resist_Overlay.spec: PyInstaller spec; includes npc_types.sql as data.
- build.bat: one-click release build (EXE + zip) using app_config.json name/version.
- test_*.py: standalone smoke tests for DB lookup and log parsing.

## Project-specific conventions
- Name normalization is essential: always convert spaces to underscores and strip leading “#” before DB lookup (see EQResistDatabase.get_npc_resists and EQLogWatcher.watch).
- DB schema uses name_lower for case-insensitive exact matches (no LIKE searches in app logic).
- Config is stored in config.json next to the script/exe; EQ log path can be auto-detected or user-specified via GUI.
- Logging is redirected to overlay.log next to the script/exe before any Tkinter import.

## Workflows
- Run from source: python eq_resist_overlay.py (Tkinter GUI).
- Build executable (Windows): run build.bat (PyInstaller onefile, windowed).
- Prepare packaged DB: python load_db.py (writes dist/npc_data.db).
- Quick checks: python test_complete.py, test_lookup_fixed.py, test_log_parsing.py.

## Integration points
- External dependency is the EverQuest log file (eqlog_*.txt); auto-detection uses common Windows install paths.
- When changing data paths or packaging, update EQ_Resist_Overlay.spec and verify db/sql lookup in eq_resist_overlay.py.
