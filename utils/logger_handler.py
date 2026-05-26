import logging
from utils.path_tool  import get_abs_path
import os
from datetime import datetime




# 1. 日志目录创建
LOG_ROOT = get_abs_path("logs")
os.makedirs(LOG_ROOT, exist_ok=True) #创建 logs 文件夹，如果已经存在就不报错，直接跳过。

#定义日志的输出格式
DEFAULT_LOG_FORMAT = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)
#DEBUG < INFO < WARNING < ERROR < CRITICAL


# 1.创建一个 文件处理器（FileHandler）
#告诉日志要往哪个文件里写

def get_logger(
        name: str = "agent",
        console_level: int = logging.INFO,#控制台打印的日志级别
        file_level: int = logging.DEBUG,#写入文件的日志级别
        log_file = None,#日志文件路径，不传就自动生成
) -> logging.Logger:
    logger = logging.getLogger(name)#创建 / 获取 一个叫 agent 的日志器
    logger.setLevel(logging.DEBUG)

    #如果这个 logger 已经有输出通道了，就直接返回它，不要再重复加通道
    if logger.handlers:
        return logger

    console_handler = logging.StreamHandler()#创建一个 “控制台输出通道”, 专门往控制台打印日志
    console_handler.setLevel(console_level)#设置控制台要显示什么级别的日志
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)#给控制台日志套上你定义的格式

    logger.addHandler(console_handler)


    #如果用户没指定日志文件，就自动生成一个规范的日志文件路径
    if not log_file:  # 日志文件的存放路径
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")

    file_handler = logging.FileHandler(log_file, encoding='utf-8')#创建一个“写文件”的通道
    file_handler.setLevel(file_level)#设置写文件的日志级别
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)#设置日志格式

    logger.addHandler(file_handler)#把“写文件通道”安装到 logger 上

    return logger




#  创建 logger 对象，把处理器加进去
# 作用：真正能用的日志工具
logger = get_logger()