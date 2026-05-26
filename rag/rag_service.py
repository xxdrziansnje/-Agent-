#给一个总结概括
# 向量检索 ：从向量数据库中检索与用户查询相关的文档片段
# 内容总结 ：将检索到的相关文档内容进行整合和概括
# 上下文构建 ：将检索到的信息与用户问题结合，形成完整的上下文

from dotenv import load_dotenv

load_dotenv()

from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_prompts
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

class RagSummarizeService(object):
    def __init__(self):
        self.vector_store=VectorStoreService()
        self.retriever=self.vector_store.get_retriever()
        self.prompt_text = load_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model=chat_model
        self.chain=self._init_chain()

    #开始的chain
    def _init_chain(self):
        chain = self.prompt_template | self.model | StrOutputParser()
        return chain

    #检索参考资料
    def retriever_docs(self,query:str)->list[Document]:
        return self.retriever.invoke(query)

    #给chian的总结
    def rag_summarize(self,query:str)->str:
        context_docs=self.retriever_docs(query)
        #此时还是list[Document]

        context=""
        counter=0  #参考资料序号
        for doc in context_docs:
            counter+=1
            context+=f"【参考资料{counter}】:参考资料：{doc.page_content}|参考元数据：{doc.metadata}\n"

        return self.chain.invoke(
            {
                "input":query,
                "context":context,
            }
        )

if __name__ == '__main__':
    rag = RagSummarizeService()

    print(rag.rag_summarize("小户型适合哪些扫地机器人"))