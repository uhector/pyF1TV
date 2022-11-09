import typing as t
from abc import ABC
from dataclasses import dataclass

from . import Images, DataGetterBase, ImageOperatorBase
from .image_prossesor import Image, ImageProcessorBase, OpenCV


T = t.TypeVar('T')


@dataclass(frozen=True)
class GraphicsBase(DataGetterBase[Image, T], ImageOperatorBase, ABC):

    image_processor: ImageProcessorBase = OpenCV()

    def _preprocess_image(self, image: Image) -> Images:
        preprocessed = self.image_processor.invert(
            self.image_processor.bgr_to_grayscale(image))
        return Images(image, preprocessed)

    def get_data_from_image(self, image: Image) -> T:
        images = self._preprocess_image(image)

        data: t.Dict[str, t.Any] = {}
        for key, value in self.__dict__.items():
            if issubclass(type(value), DataGetterBase):
                data[key] = value.get_data_from_image(images)
        return data  # type: ignore


@dataclass(frozen=True)
class DataChannelGraphicsBase(GraphicsBase[T]):
    ...
