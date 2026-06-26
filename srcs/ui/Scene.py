from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from pygame import Event, Surface

if TYPE_CHECKING:
    from .Engine import Engine


class Scene(ABC):
    def __init__(self, engine: Engine):
        self.engine: Engine = engine

    @abstractmethod
    def handle_event(self, event: Event):
        pass

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def draw(self, screen: Surface):
        pass
