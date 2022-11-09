import inspect
import itertools
import typing as t
from abc import ABC
from dataclasses import dataclass

from . import DataGetterBase, Images, ocr

T = t.TypeVar('T')
U = t.TypeVar('U')


@dataclass(frozen=True)
class Position:

    x: int
    y: int


@dataclass(frozen=True)
class Dimentions:

    width: int
    height: int


@dataclass(frozen=True)
class ElementBase(DataGetterBase[Images, U], ABC):

    position: Position
    dimentions: Dimentions

    def _get_image_section(self, images: Images) -> Images:
        height = self.position.y + self.dimentions.height
        width = self.position.x + self.dimentions.width
        # Raw image section
        raw = images.raw[self.position.y:height,
                        self.position.x:width]
        # Preprocessed image section
        preprocessed = images.preprocessed[self.position.y:height,
                                        self.position.x:width]
        return Images(raw, preprocessed)


@dataclass(frozen=True)
class TextElement(ElementBase[str]):

    type: ocr.RecogTargetType
    filters: t.List[str] | None

    def _apply_filters(self, text: str) -> str:
        if self.filters:
            for filter in self.filters:
                text = text.__getattribute__(filter)()
        return text
    
    def get_data_from_image(self, image: Images) -> str:
        sections = self._get_image_section(image)
        text = ocr.image_to_string(sections.preprocessed, self.type)
        return self._apply_filters(text)


@dataclass(frozen=True)
class ContainerElement(ElementBase[t.Dict[str, t.Any]]):

    content: t.Dict[str, ElementBase[t.Any]]

    def get_data_from_image(self, image: Images) -> t.Dict[str, t.Any]:
        sections = self._get_image_section(image)
        data: t.Dict[str, t.Any] = {}
        for key, value in self.content.items():
            data[key] = value.get_data_from_image(sections)
        return data


@dataclass(frozen=True)
class DynamicElementBase(ElementBase[U], ABC):

    repeat: int
    mutable_axis: t.Literal['x'] | t.Literal['y']
    offset: int | t.List[int]

    def _filter_attributes(
        self,
        class_: t.Callable[..., ElementBase[t.Any]],
        attributes: t.Dict[str, t.Any]
    ) -> t.Dict[str, t.Any]:
        """Filters dict to do them match with target class constructor parameters"""
        fields: t.List[t.Any] = [field for field in inspect.signature(class_).parameters]

        filtered: t.Dict[str, t.Any] = {}
        for key, value in attributes.items():
            if key in fields:
                filtered[key] = value
        return filtered

    def _generate_element(
        self,
        class_: t.Callable[..., ElementBase[t.Any]],
        attributes: t.Dict[str, t.Any]
    ) -> t.Any:
        return class_(**self._filter_attributes(class_, attributes))

    def generate_elements(
        self,
        class_: t.Callable[..., ElementBase[t.Any]]
    ) -> t.Iterator[ElementBase[t.Any]]:
        mutable_offset = self.offset
        if isinstance(mutable_offset, int):
            mutable_offset = [mutable_offset]
        
        offset_cyrcle = itertools.cycle(mutable_offset)
        attributes = vars(self).copy()
        for _ in range(self.repeat):
            yield self._generate_element(class_, attributes)
            if self.mutable_axis == 'x':
                attributes['position'] = Position(
                    attributes['position'].x + next(offset_cyrcle),
                    attributes['position'].y)
            elif self.mutable_axis == 'y':
                attributes['position'] = Position(
                    attributes['position'].x,
                    attributes['position'].y + next(offset_cyrcle))


@dataclass(frozen=True)
class DynamicTextElement(DynamicElementBase[t.List[str]], TextElement):  # type: ignore[override]
    
    def get_data_from_image(self, image: Images) -> t.List[str]:  # type: ignore[override]
        data: t.List[str] = []
        iterable = t.cast(
            t.Iterable[TextElement], self.generate_elements(TextElement))
        for element in iterable:
            data.append(element.get_data_from_image(image))
        return data


@dataclass(frozen=True)
class DynamicContainerElement(DynamicElementBase[t.List[t.Dict[str, t.Any]]],  # type: ignore[override]
                            ContainerElement):

    def get_data_from_image(self, image: Images) -> t.List[t.Dict[str, t.Any]]:  # type: ignore[override]
        data: t.List[t.Dict[str, t.Any]] = []
        iterable = t.cast(
            t.Iterable[ContainerElement], self.generate_elements(ContainerElement))
        for element in iterable:
            data.append(element.get_data_from_image(image))
        return data
