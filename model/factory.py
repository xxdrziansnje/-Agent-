#不管后面是什么模型，都必须听从 BaseModelFactory 这个“总指挥”的调遣。
from abc import ABC, abstractmethod
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_community.chat_models.tongyi import BaseChatModel
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models.tongyi import ChatTongyi
from utils.config_handler import rag_conf



# - 定义了所有工厂类必须实现的接口
# - 使用抽象方法强制子类实现 generator() 方法
# - 返回类型是 Embeddings 或 BaseChatModel 的联合类型
class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass


class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return ChatTongyi(model=rag_conf["chat_model_name"])


class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(model=rag_conf["embedding_model_name"])

#实例化
chat_model = ChatModelFactory().generator()
embed_model = EmbeddingsFactory().generator()