import hashlib
import os
from utils.logger_handler import logger

from langchain_chroma import Chroma
from utils.path_tool import get_abs_path
from utils.config_handler import  chroma_conf
from model.factory import embed_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.file_handler import pdf_loader, txt_loader, listdir_with_allowed_type,get_file_md5_hex
from langchain_core.documents import Document

#文本向量化与向量存储模块
#用来专门存放向量的特殊数据库
class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embed_model,
            persist_directory=chroma_conf["persist_directory"],
        )

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
            length_function=len,
        )

    #拿一个检索器             去向量数据库捞资料
    #as_retriever 返回一个Runnable子类实例对象
    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})

    def load_document(self):
        #从数据文件夹读书数据文件，转为向量存入向量库
        #先计算md5后去重

        def check_md5_hex(md5_for_check:str):#md5_for_check是想检查的文件的MD5值
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                #chroma_conf["md5_hex_store"]=md5.text  是相对路径
                #程序是第一次运行，还没记录过任何 MD5
                #文件不存在则创建文件关闭
                open(get_abs_path(chroma_conf["md5_hex_store"]), "w",encoding="utf-8").close()
                return False
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "r",encoding="utf-8") as f:
                for line in f.readlines():
                    line=line.strip()
                    if line==md5_for_check:
                        return True

                return False

        def save_md5_hex(md5_for_check:str):
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_for_check+"\n")

        def get_file_documents(read_path:str):  #返回的是list[documents]
            if read_path.endswith("txt"):
                return txt_loader(read_path)
            if read_path.endswith("pdf"):
                return pdf_loader(read_path)
            return []

        allowed_files_path=listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),
            tuple(chroma_conf["allow_knowledge_file_type"]),
        )

        for path in allowed_files_path:
            #获取文件的MD5
            md5_hex=get_file_md5_hex(path)

            if check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]{path}内容已经存在知识库内，跳过")
                continue

            try:
                documents:list[Document]=get_file_documents(path)

                if not documents:
                    logger.warning(f"[加载知识库]{path}内没有有效文本内容，跳过")
                    continue
                split_document=self.spliter.split_documents(documents)

                if not split_document:
                    logger.warning(f"[加载知识库]{path}内没有有效文本内容，跳过")
                    continue

                #将内容存入向量库
                self.vector_store.add_documents(split_document)

                save_md5_hex(md5_hex)

                logger.info(f"[加载知识库]{path}内容加载成功")

            except Exception as e:
                logger.error(f"[加载知识库]{path}加载失败：{str(e)}",exc_info=True)


if __name__ == '__main__':
    vs = VectorStoreService()

    vs.load_document()

    retriever = vs.get_retriever()

    res = retriever.invoke("迷路")
    for r in res:
        print(r.page_content)
        print("-"*20)
