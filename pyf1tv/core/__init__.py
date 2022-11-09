import typing as t
from abc import ABC, abstractmethod
from dataclasses import dataclass

from .image_prossesor import Image, ImageProcessorBase


T = t.TypeVar('T')
U = t.TypeVar('U')


@dataclass(frozen=True)
class Images:

    raw: Image
    preprocessed: Image


@dataclass(frozen=True)
class DataGetterBase(t.Generic[T, U], ABC):

    @abstractmethod
    def get_data_from_image(self, image: T) -> U:
        pass


@dataclass(frozen=True)
class ImageOperatorBase(ABC):

    image_processor: ImageProcessorBase
