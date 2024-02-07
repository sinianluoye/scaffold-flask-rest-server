import sys
import os
__project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, __project_path)

from config import *
import logging
from logging import FileHandler
import sys
import functools
from utils.time import datetime_utcnow
import contextlib

basicFormatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(process)d][%(threadName)s][%(filename)s:%(lineno)d][%(funcName)s] %(message)s')

class LoggerWarpper:

    def __init__(self):
        self._logger = logging.getLogger("ShowMyFiles")
        self._logger.propagate = False
    
    def add_handler(self, handler):
        self._logger.addHandler(handler)
    
    def set_level(self, level):
        self._logger.setLevel(level)
    
    def __format_log_message(self, **kwargs):
        return " | ".join([f"{key}={value}" for key, value in kwargs.items()])
    
    def __log(self, loglevel, stacklevel=0, **kwargs):
        message = self.__format_log_message(**kwargs)
        stacklevel = 3 + stacklevel # 3 is the stack level of debug-> __log -> log

        if loglevel == LOG_LEVEL_DEBUG:
            self._logger.log(logging.DEBUG, message, stacklevel=stacklevel)
        elif loglevel == LOG_LEVEL_INFO:
            self._logger.log(logging.INFO, message, stacklevel=stacklevel)
        elif loglevel == LOG_LEVEL_WARNING:
            self._logger.log(logging.WARNING, message, stacklevel=stacklevel)
        elif loglevel == LOG_LEVEL_ERROR:
            self._logger.log(logging.ERROR, message, stacklevel=stacklevel)

    def debug(self, **kwargs):
        self.__log(LOG_LEVEL_DEBUG, **kwargs)
    
    def info(self, **kwargs):
        self.__log(LOG_LEVEL_INFO, **kwargs)
    
    def warning(self, **kwargs):
        self.__log(LOG_LEVEL_WARNING, **kwargs)
    
    def error(self, **kwargs):
        self.__log(LOG_LEVEL_ERROR, **kwargs)

    def exception(self, *args, **kwargs):
        self._logger.exception(*args, **kwargs, stacklevel=2)
    
    LOG_AOP_STAGE_START = "start"
    LOG_AOP_STAGE_SUCCESS = "success"
    LOG_AOP_STAGE_FAILED = "failed"

    @contextlib.contextmanager
    def log_session(self, func=None, level=LOG_LEVEL_INFO,*,
                increase_stack_level=0,
                failed_log_level=LOG_LEVEL_ERROR, 
                error_process=None,
                show_error_trace_stack=False,
                raise_processed_error=True,
                performance_trace=False,
                performance_trace_field="time_cost",
                **trace_kwargs):
        if func is not None:
            trace_kwargs['function'] = f"{func.__module__}.{func.__name__}"
        stack_level = increase_stack_level + 1
        if performance_trace:
            start_time = datetime_utcnow()
        try:
            self.__log(level, stacklevel=stack_level, stage=self.LOG_AOP_STAGE_START, **trace_kwargs)
            yield
            if performance_trace:
                end_time = datetime_utcnow()
                trace_kwargs[performance_trace_field] = (end_time - start_time).total_seconds() 
            self.__log(level, stacklevel=stack_level, stage=self.LOG_AOP_STAGE_SUCCESS, **trace_kwargs)
        except Exception as e:
            if performance_trace:
                end_time = datetime_utcnow()
                trace_kwargs[performance_trace_field] = (end_time - start_time).total_seconds()
            self.__log(failed_log_level, stacklevel=stack_level, stage=self.LOG_AOP_STAGE_FAILED, **trace_kwargs)
            if show_error_trace_stack:
                self.exception(e)
            if error_process is not None:
                error_process(e)
            if raise_processed_error:
                raise
        

    def log_aop(self, level=LOG_LEVEL_INFO,*, 
                failed_log_level=LOG_LEVEL_ERROR, 
                error_process=None,
                show_error_trace_stack=False,
                raise_processed_error=True,
                performance_trace=False,
                performance_trace_field="time_cost",
                traced_args=None, 
                **trace_kwargs):
        """log aop

        Args:
            level (str, optional): log level. Defaults to LOG_LEVEL_DEBUG.
            failed_log_level (str, optional): log level when failed. Defaults to LOG_LEVEL_ERROR.
            error_process (function, optinal): a function accept the exception, 
                the result will be replace with the function's result instead of raise the exception,
                the trace stack will be log if it is not None, so don't write trace stack again in the function.
                default is None, which means raise the exception (and will not write trace stack). Defaults to None.
            perform_trace (bool, optional): whether trace performance_trace. Defaults to False.
            performance_trace_field (str, optional): the field name of performance_trace. Defaults to "time_cost".
            traced_args (dict, optional): a dict of name of args to trace -> function of how to get the arg. Defaults to None.
                for example: {"file_path": lambda *arg, **kwargs: kwargs["file_path"]}
            trace_kwargs (dict): another items to trace. 
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if traced_args is not None:
                    for arg in traced_args:
                        trace_kwargs[arg] = traced_args[arg](*args, **kwargs)
                with self.log_session(
                    func, 
                    increase_stack_level=1,
                    level=level,
                    failed_log_level=failed_log_level, 
                    error_process=error_process,
                    show_error_trace_stack=show_error_trace_stack,
                    raise_processed_error=raise_processed_error,
                    performance_trace=performance_trace, 
                    performance_trace_field=performance_trace_field, 
                    **trace_kwargs
                    ):
                    return func(*args, **kwargs)
            return wrapper
        return decorator


    def log_range(self, iterable, *, 
                    func=None,
                    log_every=1, 
                    log_level=LOG_LEVEL_INFO, 
                    increase_stack_level=0,
                    failed_log_level=LOG_LEVEL_ERROR, 
                    error_process=None,
                    show_error_trace_stack=False,
                    raise_processed_error=True,
                    performance_trace=False,
                    performance_trace_field="time_cost",
                    **trace_kwargs):
        with self.log_session(func=func, 
                              level=log_level, 
                              increase_stack_level=increase_stack_level, 
                              failed_log_level=failed_log_level,
                              error_process=error_process,
                              show_error_trace_stack=show_error_trace_stack,
                              raise_processed_error=raise_processed_error, 
                              performance_trace=performance_trace, 
                              performance_trace_field=performance_trace_field, 
                              **trace_kwargs):
            total = 0
            start_time = datetime_utcnow()
            for i, item in enumerate(iterable):
                yield i, item
                if (i+1) % log_every == 0:
                    speed = (datetime_utcnow() - start_time).total_seconds()/(i+1)
                    trace_kwargs["processed_items"] = i + 1
                    trace_kwargs["stage"] = "processing"
                    trace_kwargs["speed"] = f"{speed:.3f}s/item" if speed > 1 else f"{1.0/speed:.3f}items/s"
                    if hasattr(iterable, "__len__"):
                        remaining = (len(iterable) - i - 1) * speed
                        total = len(iterable)
                        progress = (i+1)/len(iterable) * 100.0
                        trace_kwargs["progress"] = f"{progress:.2f}%"
                        trace_kwargs["remaining"] = f"{remaining:.3f}s"
                        trace_kwargs["total"] = total
                   
                    self.__log(log_level, 
                               stacklevel=1+increase_stack_level, 
                               function=f"{func.__module__}.{func.__name__}", 
                               **trace_kwargs)


logger = LoggerWarpper()

if LOG_ENABLE:
    class __ColorfulHandler(logging.StreamHandler):

        __RED = "\033[1;31m"  
        __YELLOW = "\033[1;33m"
        __RESET = "\033[0m"

        def emit(self, record):
            if record.levelno >= logging.ERROR:
                self.stream.write(self.__RED)
            elif record.levelno >= logging.WARNING:
                self.stream.write(self.__YELLOW)
            else:
                self.stream.write(self.__RESET) 
            super().emit(record)
            self.stream.write(self.__RESET)

    def __add_console_handler(logger):
        consoleHandler = __ColorfulHandler()
        consoleHandler.setLevel(logging.DEBUG)
        consoleHandler.setStream(sys.stderr)
        consoleHandler.setFormatter(basicFormatter)
        logger.add_handler(consoleHandler)


    def __add_file_handler(logger):
        _fileHandlerEncoding = "utf-8"
        if os.path.exists(LOG_FILE_PATH) == False:
            os.makedirs(LOG_FILE_PATH)

        for loglevel in LOG_LEVEL_ALL:
            # NOTICE: Don't use TimedRotatingFileHandler, it is not multi-process safe
            _fileHandler = FileHandler(LOG_FILE_PATH + loglevel.lower() + ".log")
            _fileHandler.encoding = _fileHandlerEncoding
            _fileHandler.setLevel(loglevel)
            _fileHandler.setFormatter(basicFormatter)
            logger.add_handler(_fileHandler)

    logger.set_level(LOG_LEVEL)
    __add_console_handler(logger)
    __add_file_handler(logger)
