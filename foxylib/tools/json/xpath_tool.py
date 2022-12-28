from typing import Union, List, Tuple


class XpathTool:
    @classmethod
    def jpath2xpath(cls, jpath: Union[List, Tuple]) -> str:
        return '.'.join(jpath)
