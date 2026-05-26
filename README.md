<div align="center">

# 智扫通 · 智能客服 Agent

**基于 ReAct Agent + RAG + 通义千问 的扫地机器人智能客服系统**

支持知识库问答、多工具自主调用、动态提示词切换和使用报告生成。

<br>

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-LCEL-green?logo=langchain&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?logo=streamlit&logoColor=white)
![Chroma](https://img.shields.io/badge/Chroma-VectorDB-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

---

## 项目简介

智扫通是一个面向**扫地机器人/扫拖一体机器人**场景的智能客服系统。它不仅仅是一个问答机器人，而是一个具备**自主思考能力的 Agent** —— 能够根据用户的问题，自动判断需要调用哪些工具、以什么顺序调用，并整合结果生成专业回答。

**核心亮点：**
- **ReAct 推理框架**：Agent 遵循「思考 → 行动 → 观察」循环，自主决策工具调用
- **RAG 知识库检索**：基于 Chroma 向量数据库，从真实文档中检索参考资料，减少幻觉
- **动态提示词切换**：通过中间件机制，根据上下文自动切换普通问答 / 报告生成模式
- **7 个内置工具**：涵盖知识检索、天气查询、用户数据、报告生成等能力
- **流式打字机效果**：Streamlit 前端支持逐字输出，体验流畅

---

## 架构总览

```
用户输入
   │
   ▼
┌─────────────────────────────────────────────────┐
│              Streamlit 聊天界面                    │
│         (app.py · 流式打字机输出)                   │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│           ReAct Agent (LangGraph)                │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │            中间件层 (Middleware)            │   │
│  │  ┌────────────┐ ┌──────────┐ ┌─────────┐ │   │
│  │  │ monitor_   │ │ log_     │ │ report_ │ │   │
│  │  │ tool       │ │ before_  │ │ prompt_ │ │   │
│  │  │ (工具监控)  │ │ model    │ │ switch  │ │   │
│  │  │            │ │ (日志)    │ │ (提示词) │ │   │
│  │  └────────────┘ └──────────┘ └─────────┘ │   │
│  └──────────────────────────────────────────┘   │
│                      │                           │
│         思考 → 选择工具 → 执行 → 观察 → 回答       │
└──────────────────────┬──────────────────────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
   ┌──────────┐ ┌──────────┐ ┌──────────┐
   │ RAG 检索  │ │ 外部数据  │ │ 模拟服务  │
   │ (Chroma) │ │ (CSV)    │ │ (天气等)  │
   └──────────┘ └──────────┘ └──────────┘
```

---

## 项目结构

```
自研agent黑马/
│
├── app.py                          # Streamlit 主入口
├── config/                         # YAML 配置文件
│   ├── rag.yml                     #   模型名称 (qwen3-max, text-embedding-v4)
│   ├── chroma.yml                  #   向量数据库参数 (chunk_size, k, 路径等)
│   ├── prompts.yml                 #   提示词文件路径映射
│   └── agent.yml                   #   外部数据路径
│
├── prompts/                        # 提示词模板
│   ├── main_prompt.txt             #   普通客服模式 (ReAct 系统提示)
│   ├── report_prompt.txt           #   报告生成模式 (强制工具链)
│   └── rag_summarize.txt           #   RAG 摘要提示词
│
├── agent/                          # Agent 核心
│   ├── react_agent.py              #   ReactAgent 类 (创建 + 流式执行)
│   └── tools/
│       ├── agent_tools.py          #   7 个 @tool 工具定义
│       └── middleware.py           #   3 个中间件 (监控/日志/提示切换)
│
├── rag/                            # RAG 模块
│   ├── rag_service.py              #   检索 + LCEL 摘要链
│   ├── vector_store.py             #   Chroma 管理 + 文档 ETL
│   └── chroma_db/                  #   向量数据库持久化存储
│
├── model/
│   └── factory.py                  #   模型工厂 (ChatTongyi + DashScopeEmbeddings)
│
├── utils/                          # 工具模块
│   ├── config_handler.py           #   YAML 配置加载器 (模块级单例)
│   ├── prompt_loader.py            #   提示词文件加载
│   ├── file_handler.py             #   MD5 去重 + PDF/TXT 加载器
│   ├── logger_handler.py           #   控制台 + 文件双通道日志
│   └── path_tool.py                #   相对路径 → 绝对路径转换
│
├── data/                           # 知识库文档
│   ├── *.txt, *.pdf                #   扫地机器人 FAQ / 故障 / 保养 / 选购
│   └── external/
│       └── records.csv             #   模拟用户使用记录 (10用户×12月)
│
├── md5.text                        # 已入库文档的 MD5 注册表
├── logs/                           # 运行日志
├── requirements.txt                # Python 依赖
├── .env.example                    # 环境变量模板
└── .gitignore
```

---

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/xxdrziansnje/-Agent-.git
cd -Agent-
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

> **为什么要用虚拟环境？** 避免不同项目的依赖版本冲突。每个项目有自己独立的 Python 包环境，互不干扰。

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

> **依赖说明：**
>
> | 包名 | 作用 |
> |------|------|
> | `langchain` | LLM 应用开发框架，提供 Agent、Chain、Tool 等核心抽象 |
> | `langgraph` | LangChain 的图执行引擎，支持 ReAct 循环和中间件 |
> | `langchain-chroma` | Chroma 向量数据库的 LangChain 集成 |
> | `langchain-community` | 社区集成（通义千问 ChatTongyi、DashScopeEmbeddings） |
> | `dashscope` | 阿里云 DashScope SDK，通义千问模型的底层调用接口 |
> | `streamlit` | Web UI 框架，快速搭建聊天界面 |
> | `pypdf` | PDF 文件解析器 |
> | `pyyaml` | YAML 配置文件解析 |

### 4. 配置 API Key

#### 4.1 为什么需要 API Key？

本项目使用阿里云的**通义千问 (qwen3-max)** 大模型和 **text-embedding-v4** 向量模型。调用这些模型需要通过阿里云的 DashScope 平台进行身份验证。

简单来说：
- **API Key = 你的身份凭证**，阿里云用它来识别「谁在调用模型」
- **每次调用会消耗 Token**，API Key 决定了从哪个账号扣费
- **没有 API Key 就无法调用模型**，程序会报错

#### 4.2 获取 API Key

1. 打开 [阿里云 DashScope 控制台](https://dashscope.console.aliyun.com/)
2. 用你的阿里云账号登录（没有就注册一个，免费）
3. 左侧菜单找到 **「API-KEY 管理」**
4. 点击 **「创建新的 API-KEY」**
5. 复制生成的 Key（格式类似 `sk-xxxxxxxxxxxxxxxxxxxxxxxx`）

#### 4.3 写入配置文件

在项目根目录创建 `.env` 文件：

```bash
# Windows PowerShell
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```

然后编辑 `.env`，把你的 Key 填进去：

```env
DASHSCOPE_API_KEY=sk-你的实际Key填在这里
```

> **安全提醒：** `.env` 文件已在 `.gitignore` 中，不会被提交到 GitHub。**千万不要把 API Key 直接写在代码里或提交到公开仓库。**

#### 4.4 关于 Base_URL

本项目使用阿里云官方 SDK，**默认连接 DashScope 官方接口**，不需要配置 base_url。

如果你使用的是**第三方兼容接口**（比如公司内部代理、OpenAI 兼容网关），需要修改 `model/factory.py`，将 `ChatTongyi` 替换为 `ChatOpenAI` 并指定 `base_url`：

```python
# model/factory.py 中替换为：
from langchain_openai import ChatOpenAI

class ChatModelFactory(BaseModelFactory):
    def generator(self):
        return ChatOpenAI(
            model="qwen3-max",
            api_key="your-key",
            base_url="https://your-proxy-url/v1",  # 第三方服务地址
        )
```

> **大多数人不需要改这个。** 直接用阿里云官方接口即可。

### 5. 初始化知识库

首次运行前，需要将文档向量化并存入 Chroma：

```bash
python rag/vector_store.py
```

> **这一步做了什么？**
> 1. 扫描 `data/` 目录下的所有 `.txt` 和 `.pdf` 文件
> 2. 对每个文件计算 MD5，跳过已入库的（防止重复）
> 3. 将文本按 200 字符切块，重叠 20 字符（保证上下文连贯）
> 4. 使用 `text-embedding-v4` 模型将文本转为向量
> 5. 存入本地 Chroma 向量数据库

### 6. 启动应用

```bash
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`，即可开始对话。

---

## 两种运行模式

### 普通问答模式

直接输入问题，Agent 会调用 RAG 检索知识库回答：

```
你：小户型适合哪些扫地机器人？
AI：根据参考资料，小户型推荐选择...
```

### 报告生成模式

输入包含「报告」「使用记录」等关键词时，Agent 会自动切换到报告模式：

```
你：帮我生成我的使用报告
AI：[自动调用 get_user_id → get_current_month → fill_context_for_report
     → fetch_external_data，然后生成 Markdown 格式的使用报告]
```

> **提示词切换机制：** `fill_context_for_report` 工具本身没有业务逻辑，它的作用是触发 `monitor_tool` 中间件，将上下文标记为 `report=True`，随后 `report_prompt_switch` 中间件会读取这个标记，自动切换到报告专用提示词。这是一个**解耦设计** —— 工具只负责触发，提示词切换由中间件负责。

---

## 7 个内置工具

| 工具 | 类型 | 说明 |
|------|------|------|
| `rag_summarize` | 真实 RAG | 从 Chroma 向量库检索相关文档，经 LLM 摘要后返回 |
| `get_weather` | 模拟 | 返回指定城市的天气信息 |
| `get_user_location` | 模拟 | 返回用户所在城市 |
| `get_user_id` | 模拟 | 返回当前用户 ID |
| `get_current_month` | 模拟 | 返回当前月份 |
| `fetch_external_data` | 真实文件 | 从 CSV 查询指定用户指定月份的使用记录 |
| `fill_context_for_report` | 触发器 | 无业务逻辑，触发中间件切换报告模式 |

> 其中 `get_weather`、`get_user_location` 等为模拟数据，实际项目中可替换为真实 API 调用。

---

## 核心设计解析

### 中间件架构

项目使用了 3 个中间件，在 Agent 执行过程中插入拦截逻辑：

```
Agent 执行流程：

工具调用前 ──→ monitor_tool (记录日志 + 捕获报告触发器)
模型调用前 ──→ log_before_model (记录消息数量和状态)
生成提示词时 ──→ report_prompt_switch (条件选择提示词文件)
```

### RAG 检索链路

```
用户提问
   │
   ▼
text-embedding-v4 向量化
   │
   ▼
Chroma similarity_search (k=3)
   │
   ▼
格式化为【参考资料1】【参考资料2】...
   │
   ▼
PromptTemplate + qwen3-max → 摘要回答
```

### 文档 ETL 流程

```
data/ 目录扫描
   │
   ▼
过滤 .txt / .pdf
   │
   ▼
MD5 去重 (md5.text)
   │
   ▼
TextLoader / PyPDFLoader
   │
   ▼
RecursiveCharacterTextSplitter (chunk=200, overlap=20)
   │
   ▼
DashScopeEmbeddings → Chroma.add_documents()
   │
   ▼
注册 MD5，跳过下次重复处理
```

---

## 配置项说明

所有配置集中在 `config/` 目录下的 YAML 文件中：

**config/rag.yml** — 模型配置
```yaml
chat_model_name: qwen3-max          # 聊天大模型
embedding_model_name: text-embedding-v4  # 向量嵌入模型
```

**config/chroma.yml** — 向量数据库配置
```yaml
collection_name: agent       # Chroma 集合名
persist_directory: chroma_db # 持久化目录
k: 3                         # 检索返回的 Top-K 文档数
chunk_size: 200              # 文本分块大小
chunk_overlap: 20            # 分块重叠长度
```

**config/prompts.yml** — 提示词路径
```yaml
main_prompt_path: prompts/main_prompt.txt
rag_summarize_prompt_path: prompts/rag_summarize.txt
report_prompt_path: prompts/report_prompt.txt
```

---

## 常见问题

**Q: 报错 `DASHSCOPE_API_KEY` 相关错误？**
A: 检查 `.env` 文件是否存在且 Key 是否正确。注意 Key 前缀是 `sk-`，不要有多余的空格或引号。

**Q: 知识库初始化报错？**
A: 确保 `data/` 目录下有 `.txt` 或 `.pdf` 文件，且已正确安装 `pypdf`。

**Q: Chroma 数据库报错？**
A: 删除 `chroma_db/` 目录后重新运行 `python rag/vector_store.py`。

**Q: 模型响应很慢？**
A: 通义千问 qwen3-max 是较大的模型，首次调用可能较慢。可以换用 `qwen-plus` 或 `qwen-turbo`（修改 `config/rag.yml` 中的 `chat_model_name`）。

---

## License

MIT
