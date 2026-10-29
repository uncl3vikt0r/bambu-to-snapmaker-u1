# OrcaSlicer Nightly plugin

This is an offline Script plugin for OrcaSlicer Nightly. The generated installable file embeds the converter modules, ten U1 reference projects and five filament tuning rules. It declares no pip dependencies and makes no network or subprocess calls.

The plugin opens a modal HTML window for paths and conversion options. It uses OrcaSlicer's `create_window(..., style=WINDOW_MODAL, on_submit=...)` API, not the removed `show_dialog` API. Orca's plugin UI does not expose a native file picker, so copy each full path in Explorer with Shift+right-click → **Copy as path** and paste it into the dialog.

## Build

From the repository root, run:

```powershell
python plugin/snapmaker_u1_converter/build_plugin.py
```

The output is `plugin/snapmaker_u1_converter/SnapmakerU1Converter.py`.

## Install

1. In OrcaSlicer Nightly, open **File → Plugins → Install local plugin**.
2. Select `SnapmakerU1Converter.py` and activate the plugin.
3. Open **File → Plugins**, expand **Snapmaker U1 Project Converter**, then click **Run**. In the dialog, paste the source path, select a U1 profile and conversion options, and click **Convert**. The output defaults to `converted_<source name>.3mf` beside the source; you can enter a different output path. Orca may ask for file access.
4. Open the converted project in Snapmaker Orca and slice it again before printing.

The output must differ from the source; conversion never overwrites the source file. Bundled reference profiles are cached in the plugin's Orca data folder, and conversion runs inside the plugin execution context so Orca's file-access prompts apply to the selected source and output paths.

## Layout

- `snapmaker_u1_converter/build_plugin.py` assembles the single-file plugin from the existing dependency-free conversion modules.
- `snapmaker_u1_converter/SnapmakerU1Converter.py` is the generated Orca entry file; rebuild it after changing converter code or bundled data.
- `snapmaker_u1_converter/data/profiles/` contains source U1 `.3mf` references copied from the project's `profiles/` folder.
- `snapmaker_u1_converter/data/rules/` contains standard-library JSON equivalents of the web app's YAML filament rules.

The final `.py` embeds the data, so those folders are only build inputs and do not need to be installed alongside it.

## Current scope

The plugin converts Bambu/Orca, Prusa, Cura and geometry-only 3MF projects using the same conversion pipeline as the web app. It strips slicing caches, so the result is a project to review and re-slice, not a print-ready sliced file. User-defined reference profiles and editing rules are not yet exposed in the plugin UI; the built-in U1 reference profiles and matching rules ship with the plugin.
