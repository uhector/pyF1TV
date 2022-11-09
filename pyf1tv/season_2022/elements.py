import typing as t
from dataclasses import dataclass, field

from pyf1tv.core import Images
from pyf1tv.core.elements import (
    Position,
    Dimentions,
    ElementBase,
    TextElement,
    ContainerElement,
    DynamicTextElement,
    DynamicContainerElement
)


@dataclass(frozen=True)
class SessionTypeElement(TextElement):

    def get_data_from_image(self, image: Images) -> str:
        result = super().get_data_from_image(image)
        if result.startswith('p'):
            return 'practice'
        elif result.startswith('q'):
            return 'qualy'
        elif result.startswith('l'):
            return 'race'
        return ''


@dataclass(frozen=True)
class TimeLeftElement(TextElement):

    filters: t.List[str] | None = field(default_factory=lambda:['strip'])

    def get_data_from_image(self, image: Images) -> str:
        text = super().get_data_from_image(image)
        try:
            return self._apply_filters(text.split('/')[1])
        except IndexError:
            return ''


@dataclass(frozen=True)
class CurrentElement(ContainerElement):
    
    content: t.Dict[str, t.Any] = field(default_factory=lambda: {
        'tyres': TextElement(Position(24, 0), Dimentions(25, 32), 'CHAR', ['upper']),
        'time': TextElement(Position(48, 0), Dimentions(95, 32), 'TIME', ['upper'])
    })


@dataclass(frozen=True)
class ClasificationBase(DynamicContainerElement):

    repeat: int = 20
    mutable_axis: t.Literal['x'] | t.Literal['y'] = 'y'
    offset: int | t.List[int] = field(default_factory=lambda: [35, 36, 36])


@dataclass(frozen=True)
class QualyClasification(ClasificationBase):

    content: t.Dict[str, ElementBase[t.Any]] = field(default_factory=lambda: {
        'position': TextElement(
            Position(0, 0), Dimentions(40, 32), 'NUMBER', None),
        'name': TextElement(
            Position(85, 0), Dimentions(52, 32), 'WORD', ['upper']),
        'lap_time': TextElement(
            Position(159, 0), Dimentions(118, 32), 'TIME', None),
        'gap': TextElement(
            Position(278, 0), Dimentions(101, 32), 'TIME', ['upper']),
        'current': CurrentElement(
            Position(380, 0), Dimentions(170, 32)),
        'sectors': DynamicTextElement(
            Position(1556, 0), Dimentions(86, 32), 'TIME', None, 3, 'x', 86)
    })


@dataclass(frozen=True)
class RaceClasification(ClasificationBase):

    content: t.Dict[str, ElementBase[t.Any]] = field(default_factory=lambda: {
        'position': TextElement(
            Position(0, 0), Dimentions(40, 32), 'NUMBER', None),
        'name': TextElement(
            Position(85, 0), Dimentions(52, 32), 'WORD', ['upper']),
        'gap': TextElement(
            Position(203, 0), Dimentions(101, 32), 'TIME', ['upper']),
        'interval': TextElement(
            Position(305, 0), Dimentions(103, 32), 'TIME', None),
        'last_lap': TextElement(
            Position(409, 0), Dimentions(115, 32), 'TIME', None),
        'sectors': DynamicTextElement(
            Position(1556, 0), Dimentions(86, 32), 'TIME', None, 3, 'x', 86)
    })
