from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, List

if TYPE_CHECKING:
    from client import Client


@dataclass
class MenuHandler:
    name: str
    handler: Callable[[], None]


class Menu(ABC):
    def __init__(self, client: "Client") -> None:
        super().__init__()
        self.client = client
        self.menu_items = []

    def render(self):
        for i, menu_item in enumerate(self.menu_items):
            print(f"{i}. {menu_item.name}")

        try:
            selected_menu = int(input())
            if 0 <= selected_menu < len(self.menu_items):
                self.menu_items[selected_menu].handler()
        except:
            print("Invalid Input")

    def get_input(self, input_name: str) -> str:
        print(f"please enter {input_name}: ")
        return input()
