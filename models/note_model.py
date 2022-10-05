from pydantic import BaseModel


class Vec3(BaseModel):
    x: float
    y: float
    z: float


class Transform(BaseModel):
    position: Vec3
    rotation: Vec3
    scale: Vec3


class Note(BaseModel):
    identifier: str = None
    description: str
    info: Transform
    description_index: tuple[int, int] = (
        -1,
        -1,
    )  # begin and end positions of descriptions in text
