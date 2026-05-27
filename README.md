# CopyQ Scripts

Reusable CopyQ commands, processors, settings, and helpers from my daily
clipboard setup.

The export script writes a local full CopyQ command export to `all_commands.ini`
and splits each command into `commands/*.ini` so people can inspect or import
one command at a time. The split files keep CopyQ's native INI command format.
It also keeps reusable settings in `settings/copyq.conf`, including tag styles,
tab definitions, theme values, plugin settings, and shortcuts.

`all_commands.ini` is ignored because it is a generated aggregate backup. The
per-command files are the versioned source for browsing and sharing commands.

## Regenerate

CopyQ needs to be running for the native export command:

```bash
python3 scripts/export_commands.py
```

If you want the script to start the CopyQ server before exporting:

```bash
python3 scripts/export_commands.py --start-server
```

The script runs:

```bash
copyq eval "exportCommands(commands())"
```

It writes the ignored aggregate backup `all_commands.ini`, refreshes the
per-command files in `commands/`, and copies reusable settings to
`settings/copyq.conf`.

For commands, the script does not fall back to `copyq-commands.ini`, because the
`eval` export is the native format CopyQ can import from the UI. Settings are
copied from `~/.config/copyq/copyq.conf`, because CopyQ stores tag definitions,
tabs, theme values, plugin settings, and shortcuts there.

## Import

In CopyQ, open the command dialog and use the import action with either:

- a locally generated `all_commands.ini` to import everything.
- one file from `commands/` to import a single command.

Review scripts before importing them. Some commands call local programs or web
services.

See [COMMANDS.md](COMMANDS.md) for details and examples for each command.

## Settings

`settings/copyq.conf` contains reusable CopyQ settings:

- `[General]` plugin load order.
- `[Options]` behavior such as clipboard tabs, selection handling, item limits,
  UI behavior, and paste timing.
- `[Plugins]` plugin enablement and configuration, including `itemtags\tags`.
- `[Shortcuts]` CopyQ UI shortcuts.
- `[Tabs]` tab names, icons, item limits, and persistence flags.
- `[Theme]` colors, fonts, spacing, and CSS snippets.

To use these settings, review the file and merge the parts you want into your
CopyQ config while CopyQ is closed. On Linux this is usually:

```bash
~/.config/copyq/copyq.conf
```

Copying the entire file is possible, but it will also overwrite personal UI
preferences such as window behavior, editor command, theme, and tab limits.

## Local Requirements

Some commands expect these tools or Python packages to exist locally:

- `copyq`
- `python3`
- Python `evdev`, used by the sequential paste injector
- Python `pygments`, used for syntax highlighting
- `curl`, used by the upload helper
- `meld`, used by the diff helper

The upload helper contains a placeholder Paper/Write.as token value
(`REPLACE_WITH_PAPER_WF_TOKEN`). Replace it locally or adapt the command to read
a secret from your environment before using Markdown uploads.

## Privacy

This repo is for commands and reusable configuration only. Do not commit CopyQ
tab data, clipboard history, sockets, locks, local backup files, or key material.
