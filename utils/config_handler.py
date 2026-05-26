import yaml #一种专门用来写“配置文件”的文本格式
from utils.path_tool import get_abs_path

def load_rag_config(config_path: str=get_abs_path("config/rag.yml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)



def load_chroma_config(config_path: str=get_abs_path("config/chroma.yml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)



def load_prompts_config(config_path: str=get_abs_path("config/prompts.yml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)



def load_agent_config(config_path: str=get_abs_path("config/agent.yml"), encoding: str="utf-8"):
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


#程序一启动，就把所有配置读到内存里，后面随便用。
rag_conf = load_rag_config()
chroma_conf = load_chroma_config()
prompts_conf = load_prompts_config()
#它会去你的 config/ 目录下，找到你在屏幕上看到的那个 prompts.yml 纯文本文件，并用代码将它打开。
#load_prompts_config() 这个函数内部利用了 YAML 解析器（比如 yaml.safe_load()），把这堆文字活化，自动转换成了 Python 里的字典（Dict）结构。
#把这个转换好的字典赋值给变量 prompts_conf
# prompts_conf = {
#     "main_prompt_path": "prompts/main_prompt.txt",
#     "rag_summarize_prompt_path": "prompts/rag_summarize.txt",
#     "report_prompt_path": "prompts/report_prompt.txt"
# }
agent_conf = load_agent_config()