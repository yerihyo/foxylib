from typing import Tuple

from foxylib.tools.collections.collections_tool import tmap


class ColorTool:
    @classmethod
    def rgb2tinted(cls, rgb: Tuple[int, int, int], tint_factor: float) -> Tuple[int, int, int]:
        """
        ref: https://stackoverflow.com/a/31325812/1902064
        """
        def value2tinted(value: int):
            return value + int((255 - value) * tint_factor)

        return tmap(value2tinted, rgb)
