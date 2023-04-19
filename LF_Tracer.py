import sys
import inspect
from typing import Any, Optional, Callable, Dict, List, Type, TextIO, cast
from types import FrameType, TracebackType

class LFTracer():
    def __init__(self, target_func: str = None, list_func: bool = False, file: TextIO = sys.stdout) -> None:
        self.target_func = target_func
        self.list_func = list_func
        self.file = file
        self.stats = {}

    def __enter__(self) -> Any:
        def tracer(frame:FrameType, event:str, arg:Any):
            if event != 'line':
                return tracer
            co = frame.f_code
            filename = co.co_filename
            lineno = frame.f_lineno
            key = (filename, lineno)
            if key in self.stats:
                self.stats[key] += 1
            else:
                self.stats[key] = 1
            return tracer

        for target in self.target_func:
            module, func = target.rsplit('.', 1)
            mod = __import__(module, globals(), locals(), [func])
            func_obj = getattr(mod, func)
            setattr(func_obj, '__tracer__', tracer)

        return self


    def __exit__(self, exc_tp: Type, exc_value: BaseException, exc_traceback: TracebackType) -> Optional[bool]:
        return None

    def getLFMap(self):
        return self.stats
