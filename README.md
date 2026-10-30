# Open in Obsidian

A Sublime Text 4 package that opens Markdown files in [Obsidian](https://obsidian.md) 1.14 or newer, which edits files outside a vault in place.

## Usage

| Where | Action |
| --- | --- |
| Command Palette | `Open in Obsidian: Current File` |
| Keyboard | Optional; see [Key bindings](#key-bindings) |
| Editor and tab context menus | `Open in Obsidian` |
| Sidebar | Right-click one or more Markdown files and choose `Open in Obsidian` |

Modified files are saved before Obsidian opens them.

## Platform support

| Platform | Launch command |
| --- | --- |
| macOS | `open -a Obsidian <file>` |
| Windows | `%LOCALAPPDATA%\Programs\Obsidian\Obsidian.exe <file>`, then `%ProgramFiles%`, then `PATH` |
| Linux | `obsidian <file>` from `PATH` (deb, AppImage symlink, snap), then Flatpak `md.obsidian.Obsidian` |

## Settings

`Preferences > Package Settings > OpenInObsidian > Settings`

| Key | Default | Purpose |
| --- | --- | --- |
| `extensions` | `[".md", ".markdown", ".mdown", ".mdx"]` | Extensions treated as Markdown |
| `show_in_context_menus` | `true` | Show the entry in the editor, tab and sidebar context menus |
| `save_before_open` | `true` | Save modified files before opening |
| `obsidian_command` | `null` | Launch command (string or list) with the file path appended, for example `["/opt/Obsidian.AppImage"]` |

## Key bindings

`Example.sublime-keymap` lists a binding per platform. Copy the one you want to `Preferences > Package Settings > OpenInObsidian > Key Bindings`:

```json
{
    "keys": ["super+shift+o"],
    "command": "open_in_obsidian",
    "context": [{ "key": "selector", "operator": "equal", "operand": "text.html.markdown" }]
}
```

Use `ctrl+alt+o` on Windows and Linux.

## Installation

Install `OpenInObsidian` through Package Control, or clone this repository into the Sublime Text `Packages` directory under the name `OpenInObsidian`:

```sh
cd "<Sublime Text Packages dir>"
git clone https://github.com/thedanheller/sublime-text-open-in-obsidian OpenInObsidian
```

Open the directory with `Preferences > Browse Packages…`.
