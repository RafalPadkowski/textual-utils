from dataclasses import replace

from textual.app import App
from textual.binding import Binding
from textual.screen import Screen
from tilsit_i18n import tr

from .about_header_icon import AboutHeaderIcon


def translate_about_header_icon(app: App) -> None:
    about_header_icon: AboutHeaderIcon = app.query_one(AboutHeaderIcon)
    about_header_icon.tooltip = tr("About")


def translate_bindings(
    screen: App | Screen,
    bindings: list[Binding | tuple[str, str] | tuple[str, str, str]],
) -> None:
    for binding in bindings:
        if isinstance(binding, Binding):
            key = binding.key
            current_binding: Binding = screen._bindings.key_to_bindings[key][0]
            screen._bindings.key_to_bindings[key] = [
                replace(current_binding, description=tr(binding.description))
            ]
