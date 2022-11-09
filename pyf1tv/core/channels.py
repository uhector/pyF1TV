import typing as t
from abc import ABC
from dataclasses import dataclass

from . import DataGetterBase, Image
from .graphics import GraphicsBase, DataChannelGraphicsBase


T = t.TypeVar('T')


@dataclass(frozen=True)
class ChannelContextBase(DataGetterBase[Image, T], ABC):

    graphics: GraphicsBase[T]

    def get_data_from_image(self, image: Image) -> T:
        return self.graphics.get_data_from_image(image)


@dataclass(frozen=True)
class DataChannelContext(ChannelContextBase[t.Dict[str, t.Any]]):

    graphics: DataChannelGraphicsBase[t.Dict[str, t.Any]]
