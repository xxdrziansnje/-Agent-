import os
import hashlib
from utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader

#给一个文件路径，返回它的 MD5 字符串，防止文件重复上传 / 重复解析
def get_file_md5_hex(filepath: str):     # 获取文件的md5的十六进制字符串

    if not os.path.exists(filepath):#
        logger.error(f"[md5计算]文件{filepath}不存在")
        return

    if not os.path.isfile(filepath):
        logger.error(f"[md5计算]路径{filepath}不是文件")
        return

    #创建一个 MD5 计算器
    md5_obj = hashlib.md5()

    chunk_size = 4096       # 4KB分片，避免文件过大爆内存
    try:
        with open(filepath, "rb") as f:     # 打开文件   必须二进制读取
            while chunk := f.read(chunk_size): #读文件
                md5_obj.update(chunk)#计算md5

            """
            chunk = f.read(chunk_size)
            while chunk:
                
                md5_obj.update(chunk)
                chunk = f.read(chunk_size)
            """
            md5_hex = md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"计算文件{filepath}md5失败，{str(e)}")
        return None

#从一个文件夹里，只挑出你指定类型的文件，返回它们的完整路径
#去指定的文件夹里翻箱倒柜，把里面所有文件的后缀名看一遍，
# 只把符合你要求的（比如只要 .pdf 和 .txt）文件的完整绝对路径挑出来，装进一个元组（Tuple）里返回。
def listdir_with_allowed_type(path: str, allowed_types: tuple[str]):        # 返回文件夹内的文件列表（允许的文件后缀）
    files = []#准备一个空列表，用来装一会儿挑出来的合格文件

    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]{path}不是文件夹")
        return allowed_types

    for f in os.listdir(path):
        if f.endswith(allowed_types): #去掉/data/external
            files.append(os.path.join(path, f))

    return tuple(files)
    #   return的结果
    # (
    #     'data\\扫地机器人100问.pdf',
    #     'data\\扫地机器人100问2.txt',
    #     'data\\扫拖一体机器人100问.txt',
    #     'data\\故障排除.txt',
    #     'data\\维护保养.txt',
    #     'data\\选购指南.txt'
    # )

    #它执行完后，程序明确知道了有 6 个有用文件，并拿到了它们的路径




#把本地的 PDF 和 TXT 文件
# 翻译成大语言模型（LLM）后续可以进行分析、搜索或问答的数据
def pdf_loader(filepath: str, passwd=None) -> list[Document]:
    return PyPDFLoader(filepath, passwd).load()


def txt_loader(filepath: str) -> list[Document]:
    return TextLoader(filepath, encoding="utf-8").load()
#把那 6 个路径依次倒进你写的 pdf_loader 和 txt_loader 里面，
# 就能顺利把所有文本都变成 Document 对象了。