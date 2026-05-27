# CopyQ Scripts

Reusable CopyQ commands, processors, and helpers from my daily clipboard setup.

The repository keeps the full CopyQ command export in `all_scripts.ini` and also
splits each command into `commands/*.ini` so people can inspect or import one
command at a time. The split files keep CopyQ's native INI command format.

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

It writes `all_scripts.ini` and refreshes the per-command files in `commands/`.
It does not fall back to `copyq-commands.ini`, because the `eval` export is the
native format CopyQ can import from the UI.

## Import

In CopyQ, open the command dialog and use the import action with either:

- `all_scripts.ini` to import everything.
- one file from `commands/` to import a single command.

Review scripts before importing them. Some commands call local programs or web
services.

## Commands

| Command | File | Description |
| --- | --- | --- |
| Prepare Paste Queue | `commands/01-prepare-paste-queue.ini` | Queues the selected clipboard items into a temporary `&Queue` tab for sequential pasting. |
| Sequential Paste Action | `commands/02-sequential-paste-action.ini` | Global `Alt+V` action that pastes the next queued item and removes it from the queue. Uses Python `evdev` to inject `Shift+Insert`. |
| Globals and Processors | `commands/03-globals-and-processors.ini` | Main processor script for clipboard routing, recent duplicate removal, image handling, language detection, code highlighting, and item tagging metadata. |
| Copy PNG File Contents | `commands/04-copy-png-file-contents.ini` | Helper for loading PNG file bytes into the `&Images` tab and the system clipboard. |
| Upload to Write.as or Hastebin | `commands/05-upload-to-write-as-or-hastebin.ini` | Defines `upload()` for posting selected text to a Markdown publishing endpoint or a Hastebin-compatible code endpoint, then tagging the item with the resulting link. |
| Join Items | `commands/06-join-items.ini` | Defines `joinLines()` to trim non-empty clipboard lines, join them with a prompted separator, copy the result, and add it to history. |
| Highlight Items | `commands/07-highlight-items.ini` | Toggles a yellow highlight color on selected clipboard items. |
| Wrap with Code Block | `commands/08-wrap-with-code-block.ini` | Defines `codeblock()` to dedent clipboard text, detect a likely language, and wrap it in a Markdown fenced code block. |
| Diff Selected Items | `commands/09-diff-selected-items.ini` | Opens the selected two clipboard items, or the last two items, in `meld` using temporary files. |
| Delete 50 Biggest Items | `commands/10-delete-50-biggest-items.ini` | Removes the 50 largest text items from the current tab and reports the total removed size. |
| Unwrap Text | `commands/11-unwrap-text.ini` | Cleans copied multiline text: unwraps quoted strings, removes REPL prompts, handles continuation glyphs, and joins wrapped paragraphs. |
| Toggle Tag "python" | `commands/12-toggle-tag-python.ini` | Built-in item tag toggle for `python`. Disabled in this export. |
| Toggle Tag "javascript" | `commands/13-toggle-tag-javascript.ini` | Built-in item tag toggle for `javascript`. Disabled in this export. |
| Toggle Tag "golang" | `commands/14-toggle-tag-golang.ini` | Built-in item tag toggle for `golang`. Disabled in this export. |
| Toggle Tag "html" | `commands/15-toggle-tag-html.ini` | Built-in item tag toggle for `html`. Disabled in this export. |
| Toggle Tag "markdown" | `commands/16-toggle-tag-markdown.ini` | Built-in item tag toggle for `markdown`. Disabled in this export. |
| Toggle Tag "java" | `commands/17-toggle-tag-java.ini` | Built-in item tag toggle for `java`. Disabled in this export. |
| Add a Tag | `commands/18-add-a-tag.ini` | Built-in CopyQ item-tags command for adding a tag interactively. Disabled in this export. |
| Remove a Tag | `commands/19-remove-a-tag.ini` | Built-in CopyQ item-tags command for removing tags from selected items. Disabled in this export. |
| Clear all tags | `commands/20-clear-all-tags.ini` | Built-in CopyQ item-tags command for clearing all tags from selected items. Disabled in this export. |

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
