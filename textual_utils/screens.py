from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Link

from textual_utils.app_metadata import AppMetadata
from textual_utils.i18n import _


class AboutScreen(ModalScreen):
    CSS_PATH = ["screens.tcss", "about_screen.tcss"]

    def __init__(self, app_metadata: AppMetadata) -> None:
        super().__init__()

        self.app_metadata = app_metadata

    def compose(self) -> ComposeResult:
        app_name = (
            f"{self.app_metadata.name} {self.app_metadata.version}"
            f"  {self.app_metadata.codename}"
        )

        self.dialog = Grid(
            Label(Text(app_name, style="bold green")),
            Label(_(self.app_metadata.author)),
            Link(self.app_metadata.email, url=f"mailto:{self.app_metadata.email}"),
            Button("Ok", variant="primary", id="ok"),
            id="about_dialog",
        )

        yield self.dialog

    def on_mount(self) -> None:
        self.dialog.border_title = _("About")
        self.dialog.border_subtitle = self.app_metadata.name

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ok":
            self.app.pop_screen()
