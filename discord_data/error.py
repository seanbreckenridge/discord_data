from typing import TypeVar, Union

T = TypeVar("T")
E = TypeVar("E", bound=Exception)

ResT = Union[T, E]

Res = ResT[T, Exception]
