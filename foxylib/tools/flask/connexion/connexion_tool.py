from future.utils import lfilter


class ConnexionTool:
    @classmethod
    def list2cleaned(cls, array_in):
        if not array_in:
            return array_in

        return lfilter(bool, array_in)
