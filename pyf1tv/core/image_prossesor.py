import typing as t
from abc import ABC, abstractmethod

import cv2 as cv


Image: t.TypeAlias = cv.Mat


class ImageProcessorBase(ABC):

    @abstractmethod
    def brg_to_rgb(self, image: Image) -> Image:
        ...

    @abstractmethod
    def bgr_to_grayscale(self, image: Image) -> Image:
        ...

    @abstractmethod
    def rgb_to_grayscale(self, image: Image) -> Image:
        ...

    @abstractmethod
    def invert(self, image: Image) -> Image:
        ...


class OpenCV(ImageProcessorBase):

    def brg_to_rgb(self, image: Image) -> Image:
        return cv.cvtColor(image, cv.COLOR_BGR2RGB)

    def bgr_to_grayscale(self, image: Image) -> Image:
        return cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    def rgb_to_grayscale(self, image: Image) -> Image:
        return cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    
    def invert(self, image: Image) -> Image:
        return cv.bitwise_not(image)
