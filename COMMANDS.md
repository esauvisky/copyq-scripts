# Commands

This file documents the commands exported in `commands/*.ini`. Each file keeps
CopyQ's native command INI format, reindexed as a single-command import with
`size=1`.

## Prepare Paste Queue

File: `commands/01-prepare-paste-queue.ini`

Builds a temporary `&Queue` tab from the currently selected items. The command
copies the selected item data into that queue, clears any previous queue
contents, then switches back to the original tab.

Example use:

1. Select several clipboard items in CopyQ.
2. Run `Prepare Paste Queue`.
3. Use `Sequential Paste Action` repeatedly to paste each queued item.

## Sequential Paste Action

File: `commands/02-sequential-paste-action.ini`

Global shortcut: `Alt+V`

Pastes one item from `&Queue`, removes it, and deletes the queue tab when it is
empty. It uses a lock directory at `/tmp/copyq_queue_lock` to avoid overlapping
pastes and uses a small Python `evdev` helper to inject `Shift+Insert` while
preserving modifier state.

Example use: queue five snippets with `Prepare Paste Queue`, focus a target app,
then press `Alt+V` five times to paste them in order.

Requirements: `python3`, Python `evdev`, and permission to access Linux input
devices.

## Globals and Processors

File: `commands/03-globals-and-processors.ini`

Main automatic processor script. It routes normal clipboard text to
`&Clipboard`, primary selection text to `&Primary Selection`, and images to
`&Images`. It also removes recent duplicates, adds timestamp and line-count
tags, detects likely code language, and uses Pygments to generate HTML previews.

Example behavior:

- Copy Python code: item is tagged `python` and gets highlighted HTML.
- Copy a screenshot: item goes to `&Images`.
- Copy the same recent text twice: the older recent duplicate is removed so the
  new copy moves to the top.

Requirements: Python `pygments` for syntax highlighting.

## Copy PNG File Contents

File: `commands/04-copy-png-file-contents.ini`

Defines `copyImageToClipboard(path)`, a helper that reads PNG bytes from a file,
writes them into the `&Images` tab, and copies them as `image/png`.

Example use from another CopyQ command:

```javascript
copyImageToClipboard('/tmp/screenshot.png')
```

## Upload to Write.as or Hastebin

File: `commands/05-upload-to-write-as-or-hastebin.ini`

Defines `upload(type = "code")`. It posts the selected item text to a
Hastebin-compatible endpoint for code, or to a Paper/Write.as-style Markdown
endpoint for Markdown. After upload, it tags the item with the resulting link
and copies the link.

Example use from a command or action:

```javascript
upload('code')
upload('markdown')
```

The Markdown path contains the placeholder `REPLACE_WITH_PAPER_WF_TOKEN`.
Replace it locally or adapt the command to load a secret from your environment.

Requirements: `curl`.

## Join Items

File: `commands/06-join-items.ini`

Defines `joinLines()`. It reads clipboard text, trims each non-empty line,
prompts for a separator, joins the lines, copies the result, and adds it to
history. If the separator starts and ends with the same non-whitespace
character, the command wraps the final joined string with that character.

Example:

Input:

```text
alpha
beta
gamma
```

Separator: `, `

Output:

```text
alpha, beta, gamma
```

## Highlight Items

File: `commands/07-highlight-items.ini`

Toggles a yellow item color on the selected clipboard item. The menu text
changes between marking and unmarking based on the selected item state.

Example use: mark temporary snippets you need to find again during a session.

## Wrap with Code Block

File: `commands/08-wrap-with-code-block.ini`

Defines `codeblock(mode = "copy")`. It reads clipboard text, skips empty text or
text already wrapped in fences, removes common extra indentation, detects a
likely language through `detectLanguage()`, and wraps the content in a Markdown
fenced code block.

Example:

Input:

```text
    def hello():
        print("hi")
```

Output:

````text
```python
def hello():
    print("hi")
```
````

Use `codeblock('replace')` to replace the selected CopyQ item instead of only
copying the formatted text.

## Diff Selected Items

File: `commands/09-diff-selected-items.ini`

Opens two clipboard items in `meld` using temporary files. If two items are
selected, it compares those. If not, it falls back to the two most recent items.

Example use: copy two versions of a config snippet, then run this command to see
the diff.

Requirements: `meld`.

## Delete 50 Biggest Items

File: `commands/10-delete-50-biggest-items.ini`

Sorts all items in the current tab by text length, removes the 50 largest, and
shows a popup with the approximate total removed size.

Example use: quickly clean huge copied logs or generated blobs from a busy tab.

## Unwrap Text

File: `commands/11-unwrap-text.ini`

Shortcut: `Alt+Shift+U`

Cleans copied multiline text and replaces the selected item when possible. It
has three modes:

- quoted multiline strings are unquoted and joined into one line;
- REPL/console prompts are stripped while preserving code lines;
- generic wrapped paragraphs are joined while preserving paragraph breaks.

Example quoted input:

```text
"hello"
"world"
```

Output:

```text
hello world
```

Example REPL input:

```text
>>> def add(a, b):
...     return a + b
```

Output:

```text
def add(a, b):
    return a + b
```

## Toggle Tag Commands

Files:

- `commands/12-toggle-tag-python.ini`
- `commands/13-toggle-tag-javascript.ini`
- `commands/14-toggle-tag-golang.ini`
- `commands/15-toggle-tag-html.ini`
- `commands/16-toggle-tag-markdown.ini`
- `commands/17-toggle-tag-java.ini`

Built-in item-tags commands that toggle language tags on selected items. They
are disabled in this export, but they preserve the tag commands and metadata for
people who want menu-based manual tagging.

The visible tag styles come from `settings/copyq.conf`, especially the
`itemtags\tags` setting.

## Add a Tag

File: `commands/18-add-a-tag.ini`

Built-in CopyQ item-tags command for interactively adding a tag. Disabled in
this export.

## Remove a Tag

File: `commands/19-remove-a-tag.ini`

Built-in CopyQ item-tags command for removing tags from selected items. Disabled
in this export.

## Clear all tags

File: `commands/20-clear-all-tags.ini`

Built-in CopyQ item-tags command for clearing all tags from selected items.
Disabled in this export.
