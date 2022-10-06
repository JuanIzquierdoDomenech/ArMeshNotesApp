from pydantic import BaseModel

from enum import Enum

from .note_model import Vec3


class AreaSelection(BaseModel):
    begin: Vec3
    end: Vec3
    tolerance: float
    normalDir: str


class NormalDir(Enum):
    NONE = 0
    POSITIVE_X = 1
    POSITIVE_Y = 2
    POSITIVE_Z = 3
    NEGATIVE_X = 4
    NEGATIVE_Y = 5
    NEGATIVE_Z = 6


def getPlaneFromString(val: str) -> NormalDir:
    if val == "PositiveX":
        return NormalDir.POSITIVE_X
    elif val == "PositiveY":
        return NormalDir.POSITIVE_Y
    elif val == "PositiveZ":
        return NormalDir.POSITIVE_Z
    elif val == "NegativeX":
        return NormalDir.NEGATIVE_X
    elif val == "NegativeY":
        return NormalDir.NEGATIVE_Y
    elif val == "NegativeZ":
        return NormalDir.NEGATIVE_Z
