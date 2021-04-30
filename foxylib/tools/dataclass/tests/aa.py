from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, List

from dacite import from_dict, Config

if TYPE_CHECKING:
    from foxylib.tools.dataclass.tests.bb import BB


@dataclass
class AA:
    bb_list: List[BB]

    @classmethod
    def shared_function(cls):
        return "X"

    @classmethod
    def config(cls, h_aa):
        from .bb import BB

        config = Config(forward_references={"BB":BB, })
        aa: AA = from_dict(cls, h_aa, config=config)
        return aa

