class XMLToolkit:
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
