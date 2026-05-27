# Settings

The reusable settings live in `settings/copyq.conf`. This file is copied from
the non-private sections of `~/.config/copyq/copyq.conf`; it does not include
clipboard history, tab item data, sockets, locks, backups, or key files.

## How to Use

Review and merge the parts you want into your local CopyQ config while CopyQ is
closed. On Linux, the target file is usually:

```bash
~/.config/copyq/copyq.conf
```

Copying the whole file is possible, but it will replace personal preferences
like editor command, theme, tab limits, window behavior, and keyboard shortcuts.
For most people, the safest path is to merge `[Plugins]`, `[Tabs]`, and any
specific `[Options]` values they want.

## General

The `[General]` section sets plugin priority:

```ini
plugin_priority=itemencrypted, itemfakevim, itemnotes, itempinned, itemsync, itemtags, itemtext, itemimage
```

The important part for this collection is that `itemtags`, `itemtext`, and
`itemimage` are available for the command scripts and display behavior.

## Options

The `[Options]` section controls the general CopyQ behavior. Notable choices:

- `clipboard_tab=&Clipboard` stores normal clipboard text in the `&Clipboard`
  tab.
- `check_clipboard=true` keeps clipboard history enabled.
- `check_selection=false` leaves raw primary-selection monitoring off; the
  custom processor handles selected text when automatic commands run.
- `run_selection=true` lets automatic commands process selection content.
- `tabs=&Clipboard, &Primary Selection, &Images` defines the main tab order.
- `maxitems=50000` allows a large text clipboard history.
- `row_index_from_one=true` makes UI row numbers start from 1.
- `hide_toolbar=true`, `hide_toolbar_labels=true`, and related values keep the
  UI compact.
- `script_paste_delay_ms=250` and the `window_*` paste timings affect scripted
  paste reliability.

## Plugins

The `[Plugins]` section is the most important settings block for this command
collection.

Enabled plugins:

- `itemtags\enabled=true` powers visible tags such as language labels, line
  counts, timestamps, and upload links.
- `itemtext\enabled=true` enables rich text previews.
- `itemimage\enabled=true` enables image preview handling.

Disabled plugins:

- encryption, fake vim mode, notes, pinned items, and sync are present but
  disabled in this setup.

### Tag Styles

`itemtags\tags` defines the visible tag formatting used by the commands:

- `Markdown: ...` and `Hastebin: ...` tags display upload links with distinct
  icons and bold styling.
- `python`, `javascript`, `golang`, `html`, `markdown`, and `java` have
  language-specific colors and icons.
- `json`, `php`, `csharp`, `cpp`, `yaml`, `css`, and `bash` are grouped through
  one regex-based tag style.
- `Lines: N` is styled as a line-count tag.
- the final catch-all timestamp tag uses a muted clock style.

These tag styles pair with `Globals and Processors`, which detects languages,
adds line counts, and writes upload-link tags.

## Shortcuts

The `[Shortcuts]` section contains CopyQ UI shortcuts. Notable bindings:

- `commands=f6` opens the CopyQ command dialog.
- `preferences=f5` opens preferences.
- `find_items=ctrl+f` searches items.
- `show_item_content=f1` shows item content.
- `show_item_preview=f4` shows preview.
- `delete_item=del` deletes selected items.
- `reverse_selected_items=ctrl+r` reverses selected items.

Command-specific shortcuts, such as `Alt+V` for sequential paste and
`Alt+Shift+U` for unwrap text, live in the command INI files rather than this
section.

## Tabs

The `[Tabs]` section defines the working tabs:

- `Paste &Queue`: temporary queue for sequential paste.
- `&Images`: stores image clipboard items, capped at 100 items.
- `&Clipboard`: main text clipboard history, capped at 50000 items.
- `&Primary Selection`: stores processed primary-selection items and is marked
  `store_items=false`.
- `Selections`: an extra selection-oriented tab.

The queue tab is also created and removed dynamically by the paste queue
commands.

## Theme

The `[Theme]` section is a compact Solarized-style setup:

- dark background (`#002b36`) with blue selected rows (`#268bd2`);
- monospace item and search fonts;
- hidden scrollbars;
- compact item spacing and small tab counters;
- custom CSS for menus, search bar, tabs, toolbar buttons, and selected items.

These theme values are personal preference rather than a hard dependency. The
commands work without them, but the tag colors and compact UI are tuned for this
theme.

## Secrets

Secrets are not stored in `settings/copyq.conf`. The upload command expects
CopyQ to inherit this environment variable:

```bash
export PAPER_WF_TOKEN="..."
```

Set that variable wherever your desktop/session launches CopyQ from. This
repository does not assume a specific shell startup file.
