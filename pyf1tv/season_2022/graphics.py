import typing as t
from dataclasses import dataclass

from pyf1tv.core.elements import Position, Dimentions, TextElement
from pyf1tv.core.graphics import DataChannelGraphicsBase
from .elements import (
    SessionTypeElement,
    TimeLeftElement,
    ClasificationBase,
    QualyClasification,
    RaceClasification
)


T = t.TypeVar('T')


@dataclass(frozen=True)
class Graphics2022Base(DataChannelGraphicsBase[t.Dict[str, t.Any]]):

    gp_name: TextElement = TextElement(
        Position(230, 50), Dimentions(1140, 64), 'LINE', ['upper'])
    session_type: SessionTypeElement = SessionTypeElement(
        Position(1382, 45), Dimentions(220, 70), 'LINE', None)


@dataclass(frozen=True)
class QualyGraphics2022(Graphics2022Base):
    
    time_left: TextElement = TimeLeftElement(
        Position(1382, 45), Dimentions(220, 70), 'LINE')
    classification: ClasificationBase = QualyClasification(
        Position(41, 175), Dimentions(1823, 32))


@dataclass(frozen=True)
class RaceGraphics2022(Graphics2022Base):

    classification: ClasificationBase = RaceClasification(
        Position(41, 175), Dimentions(1823, 32))
