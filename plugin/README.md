# OrcaSlicer Nightly plugin

This is an offline Script plugin for OrcaSlicer Nightly. The generated installable file embeds the converter modules, ten U1 reference projects and five filament tuning rules. It declares no pip dependencies and makes no network or subprocess calls.

The plugin opens an HTML window with a file picker. The selected 3MF is passed to the existing converter in chunks; the converted project is downloaded by Orca's embedded browser. The plugin uses the `create_window` / `postMessage` host UI API and leaves the conversion algorithm unchanged.

## Build

From the repository root, run:

```powershell
python plugin/snapmaker_u1_converter/build_plugin.py
```

The output is `plugin/snapmaker_u1_converter/SnapmakerU1Converter.py`.

## Install

1. In OrcaSlicer Nightly, open **File → Plugins → Install local plugin**.
2. Select `SnapmakerU1Converter.py` and activate the plugin.
3. Open **File → Plugins**, expand **Snapmaker U1 Project Converter**, then click **Run**. Select a 3MF file, choose a U1 profile and conversion options, click **Конвертировать и скачать**, then click **Скачать** when conversion finishes. The browser saves `converted_<source name>.3mf` to its configured download folder. You can pin the script in Speed Dial with **Space**, search for the converter, then press **Ctrl+B**.
4. Open the converted project in Snapmaker Orca and slice it again before printing.

The original file is never modified. Bundled reference profiles and temporary conversion files are kept in the plugin's Orca data folder; the temporary files are removed after conversion.

## Layout

- `snapmaker_u1_converter/build_plugin.py` assembles the single-file plugin from the existing dependency-free conversion modules.
- `snapmaker_u1_converter/SnapmakerU1Converter.py` is the generated Orca entry file; rebuild it after changing converter code or bundled data.
- `snapmaker_u1_converter/data/profiles/` contains source U1 `.3mf` references copied from the project's `profiles/` folder.
- `snapmaker_u1_converter/data/rules/` contains standard-library JSON equivalents of the web app's YAML filament rules.

The final `.py` embeds the data, so those folders are only build inputs and do not need to be installed alongside it.

## Current scope

The plugin converts Bambu/Orca, Prusa, Cura and geometry-only 3MF projects using the same conversion pipeline as the web app. It strips slicing caches, so the result is a project to review and re-slice, not a print-ready sliced file. User-defined reference profiles and editing rules are not yet exposed in the plugin UI; the built-in U1 reference profiles and matching rules ship with the plugin.
