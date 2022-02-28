from typing import TypedDict


class Movie(TypedDict):
    id: str
    name: str
    addedDate: int
    watched: bool
