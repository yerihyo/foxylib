import logging
import sys

from foxylib.native.class_tools import ClassToolkit
from foxylib.native.func_tools import FuncToolkit


class LoggerToolkit:
    @classmethod
    def func2logger(cls, f, level=None,):
        l = []
        
        clazz = FuncToolkit.func2cls(f)
        if clazz: l.append( ClassToolkit.cls2name(clazz) )
        l.append( FuncToolkit.func2name(f) )
        
        name = ".".join(l)
        logger = cls.name2logger(name)
        if level: logger.setLevel(level)
        return logger
    f_class2logger = func2logger
    
#     @classmethod
#     def func2log(cls, f, msg, level=None,):
#         logger = LoggerToolkit.f_class2logger(cls.data2s_BODY,)
#         logger.debug(msg, level=level,)
    

    @classmethod
    def name2logger(cls, name):
        logger = logging.getLogger(name)
        
        # required only during debugging?

        if not logger.handlers:
            handler = logging.StreamHandler(stream=sys.stderr)
            handler.setLevel(logging.INFO)
            handler.setFormatter(logging.Formatter('%(asctime)s [%(name)s] %(levelname)s - %(message)s', "%Y.%m.%d %H:%M:%S"))
            logger.addHandler(handler)
        
        return logger
    
