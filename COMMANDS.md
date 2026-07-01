# Commands

This file documents the commands exported in `commands/*.ini`. Each file keeps
CopyQ's native command INI format, reindexed as a single-command import with
`size=1`.

## Globals and Processors

File: `commands/01-globals-and-processors.ini`

Main automatic processor script. It routes normal clipboard text to
`&Clipboard`, primary selection text to `&Primary Selection`, and images to
`&Images`. It removes recent duplicates, adds timestamp and line-count tags,
detects likely code language, and uses Pygments to generate HTML previews.

It also defines queue helpers used by the paste workflow:

- `removeIfExists(mime, contentData)` deduplicates against recent items.
- `enableQueueMode()` either queues the selected items manually or, when
  nothing is selected, clears `&Queue` and enters listen mode.
- In listen mode, copied clipboard items are intercepted, stored in `&Queue`,
  tagged with `application/x-copyq-listen-mode`, and kept out of normal
  history until playback.

Example behavior:

- Copy Python code: item is tagged `python` and gets highlighted HTML.
- Copy a screenshot: item goes to `&Images`.
- Enable queue listen mode, then copy several snippets: they accumulate in
  `&Queue` instead of `&Clipboard`.

Requirements: Python `pygments` for syntax highlighting.

## Sequential Paste Action

File: `commands/02-sequential-paste-action.ini`

Runs the queue playback and normal paste injector.

If `&Queue` does not exist, it behaves like a normal paste helper: it mirrors
the current clipboard to the primary selection and injects `Shift+Insert`
through a Python `evdev` helper.

If `&Queue` exists, it acquires `/tmp/copyq_queue_lock`, takes the oldest queued
item, forces it to row 0 to avoid CopyQ move-to-top quirks, sends it to the
system clipboard, removes it from the queue, and deletes the queue tab when it
becomes empty. Items captured in listen mode are first reinjected into
`&Clipboard` or `&Images` with fresh tags and deduplication, then pasted.

The command also uses `/tmp/copyq_queue_recording` to disable listen mode once
playback starts and `/tmp/copyq_queue_cooldown` to avoid repeated stray pastes
right after the queue finishes.

Example use:

1. Enter queue mode with `enableQueueMode()`.
2. Copy a few snippets or images.
3. Run `Sequential Paste Action` repeatedly to paste the queued items oldest
   first.

Requirements: `python3`, Python `evdev`, and permission to access Linux input
devices.

## Copy PNG File Contents

File: `commands/03-copy-png-file-contents.ini`

Defines `copyImageToClipboard(path)`, a helper that reads PNG bytes from a file,
writes them into the `&Images` tab, and copies them as `image/png`. This exists
mostly as a workaround for Chrome image-copy bugs where the browser does not put
image data on the clipboard in the shape CopyQ expects.

Example use from another CopyQ command:

```javascript
copyImageToClipboard('/tmp/screenshot.png')
```

## Upload to Write.as or Hastebin

File: `commands/04-upload-to-write-as-or-hastebin.ini`

Defines two helpers:

- `uploadMarkdown()` posts the selected item text to `https://write.as/api/posts`
  and returns a `.md` URL.
- `uploadCode()` posts the selected item text to
  `https://haste.zneix.eu/documents` and returns the resulting Haste URL.

Both commands refuse empty items, reuse an existing `Markdown:` or `Hastebin:`
tag if one is already present, tag the item with the new link, and copy the
link to the clipboard. Requests are made through `curl`, and invalid JSON or
missing keys are surfaced via CopyQ popups.

Example use from a command or action:

```javascript
uploadMarkdown()
uploadCode()
```

Requirements: `curl`.

## Join Items

File: `commands/05-join-items.ini`

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

File: `commands/06-highlight-items.ini`

Toggles a yellow item color on the selected clipboard item. The menu text
changes between marking and unmarking based on the selected item state.

Example use: mark temporary snippets you need to find again during a session.

## Wrap with Code Block

File: `commands/07-wrap-with-code-block.ini`

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

File: `commands/08-diff-selected-items.ini`

Opens two clipboard items in `meld` using temporary files. If two items are
selected, it compares those. If not, it falls back to the two most recent
items.

Example use: copy two versions of a config snippet, then run this command to see
the diff.

Requirements: `meld`.

## Delete 50 Biggest Items

File: `commands/09-delete-50-biggest-items.ini`

Sorts all items in the current tab by text length, removes the 50 largest, and
shows a popup with the approximate total removed size.

Example use: quickly clean huge copied logs or generated blobs from a busy tab.

## Unwrap Text

File: `commands/10-unwrap-text.ini`

Shortcut: `Alt+Shift+U`

Cleans copied multiline text and replaces the selected item when possible. It
has three modes:

- quoted multiline strings are unquoted and joined into one line;
- REPL or console prompts are stripped while preserving code lines;
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

- `commands/11-toggle-tag-python.ini`
- `commands/12-toggle-tag-javascript.ini`
- `commands/13-toggle-tag-golang.ini`
- `commands/14-toggle-tag-html.ini`
- `commands/15-toggle-tag-markdown.ini`
- `commands/16-toggle-tag-java.ini`

Built-in item-tags commands that toggle language tags on selected items. They
are disabled in this export, but they preserve the tag commands and metadata for
people who want menu-based manual tagging.

The visible tag styles come from `settings/copyq.conf`, especially the
`itemtags\tags` setting.

## Add a Tag

File: `commands/17-add-a-tag.ini`

Built-in CopyQ item-tags command for interactively adding a tag. Disabled in
this export.

## Remove a Tag

File: `commands/18-remove-a-tag.ini`

Built-in CopyQ item-tags command for removing tags from selected items. Disabled
in this export.

## Clear all tags

File: `commands/19-clear-all-tags.ini`

Built-in CopyQ item-tags command for clearing all tags from selected items.
Disabled in this export.
