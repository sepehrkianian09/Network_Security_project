from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, List

if TYPE_CHECKING:
    from client import Client


@dataclass
class MenuHandler:
    name: str
    handler: Callable[[], "Menu"]


class Menu(ABC):
    def __init__(self, client: "Client") -> None:
        super().__init__()
        self.client = client

    @property
    @abstractmethod
    def menu_items(self) -> List[MenuHandler]:
        pass

    def render(self) -> "Menu":
        for i, menu_item in enumerate(self.menu_items):
            print(f"{i}. {menu_item.name}")

        try:
            selected_menu = int(input())
            if 0 <= selected_menu < len(self.menu_items):
                return self.menu_items[selected_menu].handler()
        except:
            print("Invalid Input")

        return self
