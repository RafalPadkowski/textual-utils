from math import ceil
from typing import Any

from i18n import tr
from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Link, Select

from textual_utils.app_metadata import AppMetadata
from textual_utils.setting_row import SettingRow


class AboutScreen(ModalScreen[Any]):
    CSS_PATH = ["screens.tcss", "about_screen.tcss"]

    def __init__(self, current_app: App[Any], app_metadata: AppMetadata) -> None:
        super().__init__()

        self.current_app = current_app
        self.app_metadata = app_metadata

    def compose(self) -> ComposeResult:
        app_name = (
            f"{self.app_metadata.name} {self.app_metadata.version}"
            f"  {self.app_metadata.codename}"
        )

        self.dialog = Grid(
            Label(Text(app_name, style="bold green")),
            Label(tr(self.app_metadata.author)),
            Link(self.app_metadata.email, url=f"mailto:{self.app_metadata.email}"),
            Button("Ok", variant="primary", id="ok"),
            id="about_dialog",
        )

        yield self.dialog

    def on_mount(self) -> None:
        self.dialog.border_title = tr("About")
        self.dialog.border_subtitle = self.app_metadata.name

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ok":
            self.current_app.pop_screen()


class ConfirmScreen(ModalScreen[bool]):
    CSS_PATH = ["screens.tcss", "confirm_screen.tcss"]

    def __init__(self, dialog_title: str, dialog_subtitle: str, question: str) -> None:
        super().__init__()

        self.dialog_title = tr(dialog_title)
        self.dialog_subtitle = tr(dialog_subtitle)
        self.question = tr(question)

    def compose(self) -> ComposeResult:
        self.dialog = Grid(
            Label(self.question, id="question"),
            Button(tr("Yes"), variant="primary", id="yes"),
            Button(tr("No"), variant="error", id="no"),
            id="confirm_dialog",
        )

        yield self.dialog

    def on_mount(self) -> None:
        self.dialog.border_title = self.dialog_title
        self.dialog.border_subtitle = self.dialog_subtitle

        self.dialog.styles.grid_columns = str(ceil((len(self.question) - 2) / 2))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "yes":
            self.dismiss(True)
        else:
            self.dismiss(False)


class SettingsScreen(ModalScreen[dict[str, Any] | None]):
    CSS_PATH = ["screens.tcss", "settings_screen.tcss"]

    def __init__(
        self,
        dialog_title: str,
        dialog_subtitle: str,
        setting_rows: dict[str, SettingRow],
        dialog_width: int | None = None,
    ) -> None:
        super().__init__()

        self.dialog_title = tr(dialog_title)
        self.dialog_subtitle = tr(dialog_subtitle)

        self.setting_rows = setting_rows

        self.dialog_width = dialog_width

    def compose(self) -> ComposeResult:
        self.dialog = Grid(id="settings_dialog")

        with self.dialog:
            for setting_row in self.setting_rows.values():
                yield Label(_(setting_row.label))
                yield setting_row.widget

            yield Button(_("Save"), variant="primary", id="save")
            yield Button(_("Cancel"), variant="error", id="cancel")

    def on_mount(self) -> None:
        self.dialog.border_title = self.dialog_title
        self.dialog.border_subtitle = self.dialog_subtitle

        if self.dialog_width is not None:
            self.dialog.styles.width = self.dialog_width
        else:
            max_label_length = max(
                len(tr(setting_row.label)) for setting_row in self.setting_rows.values()
            )

            max_option_length = max(
                len(str(option[0]))
                for setting_row in self.setting_rows.values()
                if isinstance(setting_row.widget, Select)
                for option in setting_row.widget._options
            )

            max_length = max(max_label_length, max_option_length + 8)

            self.dialog.styles.width = 2 * max_length + 9

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            settings_dict: dict[str, Any] = {
                setting_key: self.setting_rows[setting_key].widget.value
                for setting_key in self.setting_rows.keys()
            }
            self.dismiss(settings_dict)
        else:
            self.dismiss(None)
