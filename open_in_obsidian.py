import os
import shlex
import shutil
import subprocess
import sys

import sublime
import sublime_plugin

SETTINGS_FILE = "OpenInObsidian.sublime-settings"
FLATPAK_APP_ID = "md.obsidian.Obsidian"


def get_settings():
    return sublime.load_settings(SETTINGS_FILE)


def is_markdown(path, settings):
    extensions = tuple(e.lower() for e in settings.get("extensions", [".md"]))
    return bool(path) and os.path.isfile(path) and path.lower().endswith(extensions)


def find_launcher(settings):
    """Return the argv prefix that launches Obsidian on the current platform."""
    custom = settings.get("obsidian_command")
    if custom:
        return shlex.split(custom) if isinstance(custom, str) else list(custom)

    if sys.platform == "darwin":
        return ["open", "-a", "Obsidian"]

    if sys.platform == "win32":
        candidates = [
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Obsidian", "Obsidian.exe"),
            os.path.join(os.environ.get("ProgramFiles", ""), "Obsidian", "Obsidian.exe"),
        ]
        for candidate in candidates:
            if os.path.isfile(candidate):
                return [candidate]
        found = shutil.which("Obsidian")
        if found:
            return [found]
        raise LookupError("Obsidian.exe was not found.")

    found = shutil.which("obsidian")
    if found:
        return [found]
    flatpak_dirs = [
        "/var/lib/flatpak/app",
        os.path.expanduser("~/.local/share/flatpak/app"),
    ]
    if shutil.which("flatpak") and any(
        os.path.isdir(os.path.join(d, FLATPAK_APP_ID)) for d in flatpak_dirs
    ):
        return ["flatpak", "run", FLATPAK_APP_ID]
    raise LookupError("The obsidian executable was not found in PATH.")


def launch(path, settings):
    argv = find_launcher(settings) + [path]
    options = {
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
    }
    if sys.platform == "win32":
        # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
        options["creationflags"] = 0x00000008 | 0x00000200
    else:
        options["start_new_session"] = True
    subprocess.Popen(argv, **options)


class OpenInObsidianCommand(sublime_plugin.WindowCommand):
    """Open Markdown files in Obsidian.

    Without arguments the active view is used. The sidebar passes `paths`;
    the tab context menu passes `group` and `index`.
    """

    def run(self, paths=None, group=-1, index=-1):
        settings = get_settings()
        targets = self.targets(paths, group, index, settings)
        if not targets:
            sublime.status_message("Open in Obsidian: no Markdown file selected")
            return

        for view in self.dirty_views(paths, group, index):
            if settings.get("save_before_open", True):
                view.run_command("save")

        try:
            for path in targets:
                launch(path, settings)
        except (LookupError, OSError) as error:
            sublime.error_message(
                "Open in Obsidian\n\n{}\n\n"
                "Install Obsidian 1.14 or newer, or set \"obsidian_command\" in "
                "Preferences > Package Settings > Open in Obsidian.".format(error)
            )

    def is_enabled(self, paths=None, group=-1, index=-1):
        return bool(self.targets(paths, group, index, get_settings()))

    def is_visible(self, paths=None, group=-1, index=-1):
        return self.is_enabled(paths, group, index)

    def view_for(self, group, index):
        if group >= 0 and index >= 0:
            views = self.window.views_in_group(group)
            return views[index] if index < len(views) else None
        return self.window.active_view()

    def dirty_views(self, paths, group, index):
        if paths:
            return []
        view = self.view_for(group, index)
        return [view] if view and view.file_name() and view.is_dirty() else []

    def targets(self, paths, group, index, settings):
        if paths:
            candidates = paths
        else:
            view = self.view_for(group, index)
            candidates = [view.file_name()] if view else []
        return [p for p in candidates if is_markdown(p, settings)]


class OpenInObsidianMenuCommand(OpenInObsidianCommand):
    """Menu entry variant, hidden when `show_in_context_menus` is false."""

    def is_visible(self, paths=None, group=-1, index=-1):
        return bool(get_settings().get("show_in_context_menus", True)) and super().is_visible(
            paths, group, index
        )
