# Open in Obsidian

A Sublime Text 4 package that opens Markdown files in [Obsidian](https://obsidian.md) 1.14 or newer, which edits files outside a vault in place.

## Usage

| Where | Action |
| --- | --- |
| Command Palette | `Open in Obsidian: Current File` |
| Keyboard | `Cmd+Shift+O` (macOS), `Ctrl+Alt+O` (Windows, Linux) in Markdown files |
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

`Preferences > Package Settings > Open in Obsidian > Settings`

| Key | Default | Purpose |
| --- | --- | --- |
| `extensions` | `[".md", ".markdown", ".mdown", ".mdx"]` | Extensions treated as Markdown |
| `save_before_open` | `true` | Save modified files before opening |
| `obsidian_command` | `null` | Launch command (string or list) with the file path appended, for example `["/opt/Obsidian.AppImage"]` |

## Installation

Clone this repository into the Sublime Text `Packages` directory under the name `OpenInObsidian`:

```sh
cd "<Sublime Text Packages dir>"
git clone https://github.com/thedanheller/sublime-text-open-in-obsidian OpenInObsidian
```

Open the directory with `Preferences > Browse Packages…`.
