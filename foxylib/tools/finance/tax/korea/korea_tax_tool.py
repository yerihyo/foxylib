from decimal import Decimal


class KoreaTaxTool:
    class Value:
        VAT_RATIO = Decimal("0.10")
    V = Value

    @classmethod
    def charged2vat_removed(cls, v):
        return v/(1+cls.V.VAT_RATIO)

    @classmethod
    def price2vat_added(cls, v):
        return (v * (1 + cls.V.VAT_RATIO)).normalize()
