from foxylib.tools.collections.collections_tool import l_singleton2obj
from foxylib.tools.file.file_tool import FileTool
import xml.etree.ElementTree as ET

class XMLTool:
    @classmethod
    def down(cls, root, tags):
        node = root

        for tag in tags:
            node = node.find(tag)
            if not node: return node

        return node

    @classmethod
    def down2text(cls, root, tags):
        node = root

        for tag in tags:
            node = node.find(tag)
            if not node: return node

        return node.text

    @classmethod
    def down2uniq(cls, root, tags):
        node = root
        for tag in tags:
            children = node.findall(tag)
            if not children:
                return None

            node = l_singleton2obj(children)
        return node

    @classmethod
    def x2text(cls, node): return node.text

    @classmethod
    def filepath2xml(cls, filepath):
        utf8 = FileTool.filepath2utf8(filepath)
        return cls.utf82xml(utf8)

    @classmethod
    def utf82xml(cls, utf8):
        return ET.fromstring(utf8)

    @classmethod
    def xml2j_xml(cls, xml):
        return {node.tag: node.text for node in xml}
