import logging
import ctypes
# output "logging" messages to DbgView via OutputDebugString (Windows only!)
OutputDebugString = ctypes.windll.kernel32.OutputDebugStringW

class LogOutputType:
    STDOUT = 0
    FILE = 1
    WINDOWS_DEBUG_VIEW = 2

class LogLevel:
    DEBUG = 0
    INFO = 1
    WARN = 2
    FATAL = 3

class DbgViewHandler(logging.Handler):
    def emit(self, record):
        OutputDebugString(self.format(record))


class MyLogger():

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):         # 클래스 객체에 _instance 속성이 없다면
            # print("__new__ is called\n")
            cls._instance = super().__new__(cls)  # 클래스의 객체를 생성하고 Foo._instance로 바인딩
        return cls._instance                      # Foo._instance를 리턴

    def __init__(self,log_level, log_handler_type=[LogOutputType.STDOUT]):
        fmt = logging.Formatter(
            fmt='%(asctime)s.%(msecs)03d [%(thread)5s] %(levelname)-8s %(funcName)-20s %(lineno)d %(message)s',
            datefmt='%Y:%m:%d %H:%M:%S')

        self.log_output_type = LogOutputType.STDOUT
        self.log_level = log_level
        self.logger = logging.getLogger("MyLogger")

        logging.basicConfig(level=log_level)
        self.logger.propagate = False

        if LogOutputType.WINDOWS_DEBUG_VIEW in log_handler_type:
            d_logHandler = DbgViewHandler()
            d_logHandler.setFormatter(fmt)
            self.logger.addHandler(d_logHandler)

        if LogOutputType.STDOUT in log_handler_type:
            c_logHandler = logging.StreamHandler()
            c_logHandler.setFormatter(fmt)
            self.logger.addHandler(c_logHandler)

        if LogOutputType.FILE in log_handler_type:
            f_logHandler = logging.FileHandler("DUMMY.LOG")
            f_logHandler.setFormatter(fmt)
            self.logger.addHandler(f_logHandler)

    def emit(self, record):
        if self.log_output_type == LogOutputType.WINDOWS_DEBUG_VIEW:
            OutputDebugString(self.format(record))
        elif self.log_output_type == LogOutputType.FILE:
            self.record_log_to_file(record)
        else:
            print(record)

    def set_logging_output(self, log_output_type=LogOutputType.STDOUT):
        self.log_output_type = log_output_type

    def set_logging_level(self, log_level=LogLevel.DEBUG):
        self.log_level = log_level

    def log_debug_msg(self, msg):
        self.logger.debug(msg)

    def log_info_msg(self, msg):
        self.logger.info(msg)

    def log_warn_msg(self, msg):
        self.logger.warning(msg)

    def log_fatal_msg(self, msg):
        self.logger.fatal(msg)



#logger = MyLogger(logging.DEBUG, [LogOutputType.WINDOWS_DEBUG_VIEW, LogOutputType.STDOUT])
logger = MyLogger(logging.DEBUG, [LogOutputType.FILE, LogOutputType.STDOUT])
logger.log_debug_msg('test a debug message')
logger.log_info_msg('test a info message')
logger.log_warn_msg('test a warning message')
logger.log_fatal_msg('test a fatal message')