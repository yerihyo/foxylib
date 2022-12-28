from dataclasses import dataclass

from .aa import AA  # would like to keep AA import as global


@dataclass
class BB:
    name: str

    @classmethod
    def shared_function(cls):
        AA.shared_function()  # need to import AA in multiple parts of BB

    @classmethod
    def config(cls, ):
        return {"x":"y"}
