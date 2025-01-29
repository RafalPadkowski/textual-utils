from textual.events import Click
from textual.widgets._header import HeaderIcon

from textual_utils import AboutScreen, AppMetadata


class AboutHeaderIcon(HeaderIcon):
    def __init__(self, icon: str, app_metadata: AppMetadata) -> None:
        super().__init__()

        self.icon = icon
        self.app_metadata = app_metadata

    async def on_click(self, _event: Click) -> None:
        self.app.push_screen(AboutScreen(self.app_metadata))
