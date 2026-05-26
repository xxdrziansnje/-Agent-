<div align="center">

<img src="https://img.shields.io/badge/智扫通-ZhiSaoTong-blue?style=for-the-badge&logo=robot&logoColor=white" alt="智扫通"/>

# 智扫通 · 智能客服 Agent

### 基于 ReAct Agent + RAG + 通义千问 的扫地机器人智能客服系统

<br/>

**具备自主思考能力的 AI Agent —— 能自动判断调用哪些工具、以什么顺序调用，整合结果生成专业回答。**

<br/>

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/LangChain-LCEL-1C3C3C?style=flat-square&logo=langchain&logoColor=white" alt="LangChain"/>
<img src="https://img.shields.io/badge/LangGraph-Agent-1C3C3C?style=flat-square&logo=datachain&logoColor=white" alt="LangGraph"/>
<img src="https://img.shields.io/badge/通义千问-qwen3--max-615EFE?style=flat-square&logo=alibabacloud&logoColor=white" alt="Qwen"/>
<img src="https://img.shields.io/badge/Chroma-VectorDB-E87722?style=flat-square&logo=chroma&logoColor=white" alt="Chroma"/>
<img src="https://img.shields.io/badge/Streamlit-App-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit"/>
<img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="MIT"/>

<br/>

<img src="https://img.shields.io/badge/状态-已测试通过-brightgreen?style=flat-square" alt="Tested"/>
<img src="https://img.shields.io/badge/Python-依赖-11+?style=flat-square&logo=pypi&logoColor=white" alt="Deps"/>
<img src="https://img.shields.io/badge/工具数-7个-orange?style=flat-square" alt="Tools"/>

</div>

<br/>

---

## 目录

- [项目简介](#项目简介)
- [效果展示](#效果展示)
- [技术架构](#技术架构)
- [项目结构](#项目结构)
- [环境要求](#环境要求)
- [快速开始（6步跑通）](#快速开始6步跑通)
- [配置详解](#配置详解)
- [两种运行模式](#两种运行模式)
- [7个内置工具](#7个内置工具)
- [核心设计解析](#核心设计解析)
- [完整依赖清单](#完整依赖清单)
- [常见问题排查](#常见问题排查)
- [二次开发指南](#二次开发指南)
- [License](#license)

---

## 项目简介

智扫通是一个面向**扫地机器人 / 扫拖一体机器人**场景的智能客服系统。

它不是简单的问答机器人，而是一个具备 **ReAct 推理能力的 Agent** —— 面对用户问题，它会自主完成「思考 → 行动 → 观察 → 再思考」的循环，判断需要调用哪些工具、以什么顺序调用，最终整合所有信息生成专业回答。

### 核心特性

<table>
<tr>
<td width="50%">

**ReAct 推理框架**
Agent 遵循「思考 → 行动 → 观察」循环，面对复杂问题能自主拆解、分步执行，而非一步到位。

</td>
<td width="50%">

**RAG 知识库检索**
基于 Chroma 向量数据库的语义检索，从真实文档中获取参考资料，让大模型「言之有据」，减少幻觉。

</td>
</tr>
<tr>
<td>

**动态提示词切换**
通过中间件机制，根据运行时上下文自动切换「普通问答」和「报告生成」两种模式，无需重启。

</td>
<td>

**7 个内置工具**
涵盖知识检索 (RAG)、天气查询、用户数据、外部 CSV 查询、报告生成触发器等能力。

</td>
</tr>
<tr>
<td>

**流式打字机效果**
Streamlit 前端逐字输出 AI 回答，体验流畅自然。

</td>
<td>

**工厂模式 + 单例**
模型创建使用工厂模式，配置加载使用模块级单例，保证全局唯一实例，避免重复初始化。

</td>
</tr>
</table>

---

## 效果展示

### 普通问答

```
你：小户型适合哪些扫地机器人？

AI：根据参考资料，小户型建议选择以下类型的扫地机器人：
    1. 机身高度低于8cm的机型，可以轻松进入沙发和床底
    2. 支持LDS激光导航的机型，建图更精准
    3. 尘盒容量0.3L以上即可，不需要太大...
```

### 报告生成

```
你：帮我生成我的使用报告

AI：# 黑马程序员扫地机器人使用情况报告与保养建议

    ## 一、基本信息
    - 用户ID：1003
    - 报告月份：2025-06

    ## 二、使用情况分析
    - 清洁效率：92%
    - 耗材状态：边刷寿命剩余 60%
    ...

    ## 三、保养建议
    ...
```

---

## 技术架构

```
用户输入
   │
   ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Streamlit 聊天界面                           │
│                   (app.py · 流式打字机输出)                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                 ReAct Agent (LangGraph)                          │
│                                                                  │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │                   中间件层 (Middleware)                    │  │
│   │                                                          │  │
│   │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│   │   │ monitor_tool │  │log_before_   │  │report_prompt │  │  │
│   │   │  工具执行监控  │  │model 模型日志│  │_switch 提示词│  │  │
│   │   │              │  │              │  │   动态切换    │  │  │
│   │   └──────────────┘  └──────────────┘  └──────────────┘  │  │
│   └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│           思考 → 选择工具 → 执行 → 观察 → 再思考 → 回答             │
└────────────────────────────┬────────────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
     ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
     │   RAG 检索    │ │   外部数据    │ │   模拟服务    │
     │   (Chroma)   │ │   (CSV)      │ │   (天气等)    │
     │  向量语义检索  │ │  用户使用记录  │ │  可替换为真实  │
     └──────────────┘ └──────────────┘ └──────────────┘
```

### 技术栈

| 层级 | 技术 | 作用 |
|------|------|------|
| **大语言模型** | 阿里云通义千问 `qwen3-max` | 核心推理与自然语言生成 |
| **向量模型** | 阿里云 `text-embedding-v4` | 将文本转为 1024 维向量 |
| **Agent 框架** | LangGraph + ReAct | 图执行引擎，支持循环推理和中间件 |
| **编排框架** | LangChain (LCEL) | Chain、Tool、Prompt 的标准抽象 |
| **向量数据库** | Chroma | 本地持久化向量存储 |
| **前端界面** | Streamlit | 快速搭建聊天 Web UI |
| **模型 SDK** | DashScope | 阿里云模型调用底层接口 |

---

## 项目结构

```
.
├── app.py                              # Streamlit 主入口
│
├── config/                             # 配置文件（全部为 YAML）
│   ├── rag.yml                         #   模型名称配置
│   ├── chroma.yml                      #   向量数据库参数
│   ├── prompts.yml                     #   提示词文件路径映射
│   └── agent.yml                       #   Agent 外部数据路径
│
├── prompts/                            # 提示词模板（纯文本 .txt）
│   ├── main_prompt.txt                 #   普通客服 ReAct 系统提示词
│   ├── report_prompt.txt               #   报告生成专用提示词
│   └── rag_summarize.txt               #   RAG 摘要提示词
│
├── agent/                              # Agent 核心模块
│   ├── react_agent.py                  #     ReactAgent 类（创建 + 流式执行）
│   └── tools/
│       ├── agent_tools.py              #       7 个 @tool 工具定义
│       └── middleware.py               #       3 个中间件实现
│
├── rag/                                # RAG 检索模块
│   ├── rag_service.py                  #     检索 + LCEL 摘要链
│   └── vector_store.py                 #     Chroma 管理 + 文档 ETL
│
├── model/
│   └── factory.py                      # 模型工厂（ChatTongyi + DashScopeEmbeddings）
│
├── utils/                              # 工具模块
│   ├── config_handler.py               #   YAML 配置加载器（模块级单例）
│   ├── prompt_loader.py                #   提示词文件加载器
│   ├── file_handler.py                 #   MD5 去重 + PDF/TXT 加载器
│   ├── logger_handler.py               #   控制台 + 文件双通道日志
│   └── path_tool.py                    #   相对路径 → 绝对路径转换
│
├── data/                               # 知识库文档
│   ├── 扫地机器人100问.pdf              #   扫地机器人常见问题
│   ├── 扫地机器人100问2.txt             #   扫地机器人常见问题（补充）
│   ├── 扫拖一体机器人100问.txt          #   扫拖一体机器人 FAQ
│   ├── 故障排除.txt                     #   故障排查指南
│   ├── 维护保养.txt                     #   日常维护保养
│   ├── 选购指南.txt                     #   选购建议
│   └── external/
│       └── records.csv                 #   模拟用户使用记录（10用户×12月）
│
├── md5.text                            # 已入库文档的 MD5 注册表
├── logs/                               # 运行日志（自动生成）
├── chroma_db/                          # 向量数据库持久化（自动生成）
│
├── requirements.txt                    # Python 依赖清单
├── .env.example                        # 环境变量模板
├── .gitignore                          # Git 忽略规则
└── README.md                           # 项目说明（本文件）
```

---

## 环境要求

| 项目 | 要求 | 说明 |
|------|------|------|
| **Python** | 3.10 及以上 | 推荐 3.11 或 3.12 |
| **操作系统** | Windows / macOS / Linux | 均已测试通过 |
| **网络** | 需要能访问阿里云 API | 首次知识库初始化和每次对话都需要 |
| **磁盘** | 约 200MB | 依赖包 + 向量数据库 |
| **阿里云账号** | 需要 | 用于获取 DashScope API Key（免费注册） |

---

## 快速开始（6步跑通）

> **重要：** 后续所有命令都在项目根目录下执行，不要进入子目录。

### 第 1 步：克隆项目

```bash
git clone https://github.com/xxdrziansnje/-Agent-.git
cd -Agent-
```

### 第 2 步：创建虚拟环境

```bash
python -m venv venv
```

激活虚拟环境：

```bash
# Windows CMD
venv\Scripts\activate.bat

# Windows PowerShell
venv\Scripts\Activate.ps1

# macOS / Linux
source venv/bin/activate
```

激活后命令行前面会出现 `(venv)` 前缀，表示虚拟环境已生效。

> **为什么用虚拟环境？**
> 不同项目可能依赖同一个包的不同版本。虚拟环境为每个项目创建独立的 Python 环境，
> 避免 A 项目需要 `langchain==0.3.0` 而 B 项目需要 `langchain==0.2.0` 的冲突。

### 第 3 步：安装依赖

```bash
pip install -r requirements.txt
```

安装过程大约需要 1-3 分钟，取决于网络速度。看到 `Successfully installed ...` 就是成功了。

> **如果下载很慢**，可以使用国内镜像源：
> ```bash
> pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
> ```

### 第 4 步：配置 API Key

#### 4.1 为什么需要 API Key？

本项目使用阿里云的 **通义千问 (qwen3-max)** 大模型和 **text-embedding-v4** 向量模型。
调用这些模型需要通过阿里云的 DashScope 平台进行身份验证。

简单来说：
- **API Key = 你的身份凭证**，阿里云用它来识别「谁在调用模型」
- **每次调用会消耗 Token**（按量计费），API Key 决定了从哪个账号扣费
- **没有 API Key 就无法调用模型**，程序启动就会报错

#### 4.2 获取 API Key（约 2 分钟）

1. 打开 [阿里云 DashScope 控制台](https://dashscope.console.aliyun.com/)
2. 用你的阿里云账号登录（没有就注册一个，**免费**）
3. 首次使用需要**开通 DashScope 服务**（免费开通，按量计费）
4. 左侧菜单找到 **「API-KEY 管理」**
5. 点击 **「创建新的 API-KEY」**
6. 复制生成的 Key（格式类似 `sk-xxxxxxxxxxxxxxxxxxxxxxxx`）

> **注意：** 请妥善保管你的 API Key，不要泄露给他人或提交到公开仓库。

#### 4.3 写入配置文件

**方式一：命令行（推荐）**

```bash
# Windows PowerShell
Copy-Item .env.example .env

# Windows CMD
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

**方式二：手动操作**

在项目根目录找到 `.env.example` 文件，复制一份并重命名为 `.env`。

然后用记事本或任意编辑器打开 `.env`，将你的 Key 填入：

```env
DASHSCOPE_API_KEY=sk-你的实际Key填在这里
```

**完整的 `.env` 文件内容应该长这样：**

```env
# 唯一需要填写的配置
DASHSCOPE_API_KEY=sk-5a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p
```

> **安全提醒：**
> - `.env` 文件已在 `.gitignore` 中，**不会被提交到 GitHub**
> - **千万不要**把 API Key 直接写在代码里或提交到公开仓库
> - 如果 Key 不慎泄露，去 DashScope 控制台删除并重新创建即可

#### 4.4 关于 Base_URL

本项目使用阿里云官方 SDK，**默认连接 DashScope 官方接口**，**不需要配置 base_url**。

如果你使用的是**第三方兼容接口**（比如公司内部代理、OpenAI 兼容网关），需要修改 `model/factory.py`：

```python
# 将 ChatTongyi 替换为 ChatOpenAI
from langchain_openai import ChatOpenAI

class ChatModelFactory(BaseModelFactory):
    def generator(self):
        return ChatOpenAI(
            model="qwen3-max",
            api_key="your-key",
            base_url="https://your-proxy-url/v1",  # 第三方服务地址
        )
```

同时修改 `EmbeddingsFactory` 也类似处理。**大多数人不需要改这个。**

### 第 5 步：初始化知识库

```bash
python -m rag.vector_store
```

首次运行输出类似：

```
INFO - [加载知识库] data\扫地机器人100问.pdf 内容加载成功
INFO - [加载知识库] data\扫拖一体机器人100问.txt 内容加载成功
...
```

> **为什么用 `python -m` 而不是 `python rag/vector_store.py`？**
> 项目内部使用了相对导入（如 `from utils.xxx import ...`），
> 直接运行 `.py` 文件会报 `ModuleNotFoundError`。
> `python -m` 会把项目根目录加入 Python 搜索路径，确保所有模块都能正确导入。

> **这一步做了什么？**
>
> | 步骤 | 操作 | 说明 |
> |------|------|------|
> | 1 | 扫描 `data/` 目录 | 找到所有 `.txt` 和 `.pdf` 文件 |
> | 2 | MD5 去重 | 对每个文件计算 MD5，跳过已入库的 |
> | 3 | 文本分块 | 按 200 字符切块，重叠 20 字符 |
> | 4 | 向量化 | 调用 `text-embedding-v4` 转为向量 |
> | 5 | 存入 Chroma | 写入本地向量数据库 |
>
> 首次运行需要调用阿里云的向量模型 API，会消耗少量 Token。
> 后续运行如果文档没变化会自动跳过（MD5 相同）。

### 第 6 步：启动应用

```bash
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`，即可开始对话。

> **启动后看到以下输出说明一切正常：**
> ```
> You can now view your Streamlit app in your browser.
> Local URL: http://localhost:8501
> ```

---

## 配置详解

所有运行时配置集中在 `config/` 目录下的 YAML 文件中，**无需修改 Python 代码**。

### config/rag.yml — 模型配置

```yaml
chat_model_name: qwen3-max              # 聊天大模型
embedding_model_name: text-embedding-v4  # 向量嵌入模型
```

可选模型（按速度排序）：

| 模型 | 速度 | 质量 | 适用场景 |
|------|------|------|---------|
| `qwen-turbo` | 最快 | 一般 | 简单问答、测试 |
| `qwen-plus` | 中等 | 较好 | 日常使用 |
| `qwen3-max` | 较慢 | 最强 | 复杂推理、报告生成 |

### config/chroma.yml — 向量数据库配置

```yaml
collection_name: agent           # Chroma 集合名
persist_directory: chroma_db     # 持久化目录
k: 3                             # 检索返回的 Top-K 文档数
data_path: data                  # 知识库文档目录
md5_hex_store: md5.text          # MD5 去重记录文件
allow_knowledge_file_type:       # 允许的文件类型
  - "txt"
  - "pdf"

chunk_size: 200                  # 文本分块大小（字符数）
chunk_overlap: 20                # 分块重叠长度
separators:                      # 分隔符优先级（从高到低）
  - "\n\n"
  - "\n"
  - "."
  - "!"
  - "?"
  - "。"
  - "！"
  - "？"
  - " "
  - ""
```

> **chunk_size 怎么选？**
> - 太小（<100）：语义被切断，检索效果差
> - 太大（>500）：包含太多无关信息，模型容易「迷路」
> - 推荐 200-500，本项目用 200 是因为知识库文档较短

### config/prompts.yml — 提示词路径

```yaml
main_prompt_path: prompts/main_prompt.txt           # 普通客服提示词
rag_summarize_prompt_path: prompts/rag_summarize.txt # RAG 摘要提示词
report_prompt_path: prompts/report_prompt.txt        # 报告生成提示词
```

### config/agent.yml — Agent 配置

```yaml
external_data_path: data/external/records.csv  # 外部用户数据路径
```

---

## 两种运行模式

### 普通问答模式

直接输入问题，Agent 走标准 ReAct 流程：

```
你：小户型适合哪些扫地机器人？

Agent 思考：用户在问选购建议，需要调用 rag_summarize 检索知识库
Agent 行动：调用 rag_summarize("小户型 扫地机器人 推荐")
Agent 观察：检索到 3 条参考资料
Agent 回答：根据参考资料，小户型建议选择...
```

### 报告生成模式

输入包含「报告」「使用记录」等关键词时，Agent 自动切换模式：

```
你：帮我生成我的使用报告

Agent 思考：用户要生成报告，需要按固定流程执行
Agent 行动：调用 get_user_id() → 获取 "1003"
Agent 行动：调用 get_current_month() → 获取 "2025-06"
Agent 行动：调用 fill_context_for_report() → 触发中间件切换提示词
Agent 行动：调用 fetch_external_data("1003", "2025-06") → 获取使用数据
Agent 回答：# 黑马程序员扫地机器人使用情况报告...
```

> **提示词切换机制（关键设计）：**
>
> `fill_context_for_report` 工具本身没有业务逻辑，它的唯一作用是：
> 1. 被 `monitor_tool` 中间件捕获
> 2. 中间件将运行时上下文标记为 `report=True`
> 3. `report_prompt_switch` 中间件读取该标记
> 4. 自动切换到报告专用提示词文件
>
> 这是一个**解耦设计** —— 工具只负责「触发信号」，提示词切换由中间件负责，
> 两者互不依赖，便于独立扩展。

---

## 7个内置工具

| # | 工具名 | 类型 | 说明 | 入参 |
|---|--------|------|------|------|
| 1 | `rag_summarize` | 真实 RAG | 从 Chroma 检索文档 → LLM 摘要 | `query: str` |
| 2 | `get_weather` | 模拟 | 返回指定城市天气 | `city: str` |
| 3 | `get_user_location` | 模拟 | 返回用户所在城市 | 无 |
| 4 | `get_user_id` | 模拟 | 返回用户 ID | 无 |
| 5 | `get_current_month` | 模拟 | 返回当前月份 (YYYY-MM) | 无 |
| 6 | `fetch_external_data` | 真实文件 | 从 CSV 查询用户使用记录 | `user_id: str, month: str` |
| 7 | `fill_context_for_report` | 触发器 | 触发中间件切换报告模式 | 无 |

> **关于「模拟」工具：**
> `get_weather`、`get_user_location` 等返回的是模拟数据。
> 在实际项目中，只需替换函数体为真实 API 调用即可，Agent 层无需任何改动。
> 这体现了工具与 Agent 的**解耦性**。

---

## 核心设计解析

### 中间件架构

项目使用 3 个中间件，在 Agent 执行的不同时机插入拦截逻辑：

```
Agent 执行时间线
─────────────────────────────────────────────────────────────►

  工具调用前        模型调用前        生成提示词时
      │                │                │
      ▼                ▼                ▼
┌───────────┐   ┌───────────┐   ┌───────────┐
│monitor_   │   │log_before │   │report_    │
│tool       │   │_model     │   │prompt_    │
│           │   │           │   │switch     │
│• 记录日志  │   │• 记录消息数│   │• 读取标记  │
│• 捕获报告 │   │• 记录状态  │   │• 切换提示词│
│  触发器   │   │           │   │  文件     │
└───────────┘   └───────────┘   └───────────┘
```

### RAG 检索链路

```
用户提问: "小户型适合哪些扫地机器人？"
         │
         ▼
  text-embedding-v4 向量化
  (文本 → 1024维向量)
         │
         ▼
  Chroma similarity_search (k=3)
  (在向量空间中找最相似的3个文档片段)
         │
         ▼
  格式化为: 【参考资料1】xxx 【参考资料2】xxx ...
         │
         ▼
  PromptTemplate + qwen3-max
  (将参考资料和用户问题一起发给大模型)
         │
         ▼
  返回专业摘要回答
```

### 文档 ETL 流程

```
data/ 目录扫描
  ├─ 扫地机器人100问.pdf  ✓
  ├─ 扫拖一体机器人100问.txt  ✓
  ├─ 故障排除.txt  ✓
  └─ ...共6个文件
         │
         ▼
  过滤: 只保留 .txt 和 .pdf
         │
         ▼
  MD5 去重 (比对 md5.text)
  ├─ 已存在 → 跳过
  └─ 新文件 → 继续处理
         │
         ▼
  文本加载 (TextLoader / PyPDFLoader)
         │
         ▼
  文本分块 (RecursiveCharacterTextSplitter)
  ├─ chunk_size = 200 字符
  ├─ chunk_overlap = 20 字符
  └─ 保留语义完整性
         │
         ▼
  向量化 (DashScopeEmbeddings)
  └─ text-embedding-v4 → 1024维向量
         │
         ▼
  存入 Chroma (本地持久化)
  └─ 记录 MD5，下次跳过
```

---

## 完整依赖清单

`requirements.txt` 中的所有依赖及其用途：

| 包名 | 版本 | 用途 |
|------|------|------|
| `langchain` | - | LLM 应用开发框架，提供 Agent、Chain、Tool 等核心抽象 |
| `langchain-core` | - | LangChain 核心组件（LCEL、消息类型、Prompt 等） |
| `langchain-community` | - | 社区集成包（通义千问 ChatTongyi、DashScopeEmbeddings） |
| `langchain-chroma` | - | Chroma 向量数据库的 LangChain 集成 |
| `langchain-text-splitters` | - | 文本分块器（RecursiveCharacterTextSplitter） |
| `langgraph` | - | LangChain 的图执行引擎，支持 ReAct 循环和中间件 |
| `dashscope` | - | 阿里云 DashScope SDK，通义千问模型的底层调用接口 |
| `streamlit` | - | Web UI 框架，快速搭建聊天界面 |
| `pypdf` | - | PDF 文件解析器 |
| `pyyaml` | - | YAML 配置文件解析 |
| `python-dotenv` | - | 从 `.env` 文件加载环境变量 |

> **安装命令：**
> ```bash
> pip install -r requirements.txt
> ```
>
> **如果下载慢，使用清华镜像源：**
> ```bash
> pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
> ```
>
> **如果某个包安装失败，尝试单独安装：**
> ```bash
> pip install langgraph --upgrade
> ```

---

## 常见问题排查

### 启动类问题

<details>
<summary><b>Q: 报错 ModuleNotFoundError: No module named 'xxx'？</b></summary>

确保你在 **项目根目录** 下运行命令，且使用 `python -m` 方式执行模块：

```bash
# 正确
python -m rag.vector_store

# 错误
python rag/vector_store.py
```

</details>

<details>
<summary><b>Q: 报错 ModuleNotFoundError: No module named 'langchain'？</b></summary>

依赖没装完，重新执行：

```bash
pip install -r requirements.txt
```

</details>

### API Key 类问题

<details>
<summary><b>Q: 报错 DashScope API Key 相关错误？</b></summary>

检查以下几点：

1. `.env` 文件是否存在于项目根目录（不是子目录）
2. 文件名是否正确（不要写成 `.env.txt`）
3. Key 是否正确（前缀是 `sk-`，不要有多余的空格或引号）
4. `.env` 文件内容格式：`DASHSCOPE_API_KEY=sk-xxxxx`（等号两边不要有空格）
5. 如果刚创建 `.env`，重启一下终端再试

**快速验证 Key 是否生效：**

```bash
python -c "from dotenv import load_dotenv; load_dotenv(); from model.factory import chat_model; print(chat_model.invoke('你好').content)"
```

如果返回正常回答，说明配置成功。

</details>

<details>
<summary><b>Q: 如何确认 API Key 已正确加载？</b></summary>

```bash
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('Key:', os.environ.get('DASHSCOPE_API_KEY', 'NOT SET')[:10] + '...')"
```

应该输出 `Key: sk-xxxxxxx...`，如果输出 `Key: NOT SET...` 说明 `.env` 没读到。

</details>

### 知识库类问题

<details>
<summary><b>Q: 知识库初始化报错？</b></summary>

1. 确保 `data/` 目录下有 `.txt` 或 `.pdf` 文件
2. 确保已安装 `pypdf`：`pip install pypdf`
3. 确保使用 `python -m rag.vector_store` 命令

</details>

<details>
<summary><b>Q: Chroma 数据库报错？</b></summary>

删除向量数据库后重新初始化：

```bash
# Windows
rmdir /s /q chroma_db

# macOS / Linux
rm -rf chroma_db

# 重新初始化
python -m rag.vector_store
```

</details>

### 性能类问题

<details>
<summary><b>Q: 模型响应很慢？</b></summary>

通义千问 `qwen3-max` 是较大的模型，首次调用可能需要几秒到十几秒。

可以换用更快的模型，修改 `config/rag.yml` 中的 `chat_model_name`：

```yaml
chat_model_name: qwen-turbo   # 最快
# chat_model_name: qwen-plus  # 平衡
# chat_model_name: qwen3-max  # 最强（默认）
```

</details>

<details>
<summary><b>Q: 首次启动很慢？</b></summary>

首次启动需要：
1. 加载 sentence-transformers 模型（首次会下载，约 500MB）
2. 创建 Chroma 向量数据库连接

后续启动会快很多。如果实在太慢，可以检查网络连接。

</details>

---

## 二次开发指南

### 添加新工具

在 `agent/tools/agent_tools.py` 中添加：

```python
@tool(description="工具描述，Agent 根据此判断何时调用")
def my_new_tool(param: str) -> str:
    """工具的 docstring 也会被 Agent 读取"""
    # 你的逻辑
    return "结果"
```

然后在 `agent/react_agent.py` 的工具列表中注册：

```python
tools=[rag_summarize, get_weather, ..., my_new_tool]  # 添加到这里
```

最后在 `prompts/main_prompt.txt` 中补充新工具的使用说明。

### 添加新中间件

在 `agent/tools/middleware.py` 中添加：

```python
@wrap_tool_call  # 或 @before_model / @dynamic_prompt
def my_middleware(request, handler):
    # 你的拦截逻辑
    return handler(request)
```

然后在 `agent/react_agent.py` 的中间件列表中注册：

```python
middleware=[monitor_tool, log_before_model, report_prompt_switch, my_middleware]
```

### 替换大模型

修改 `config/rag.yml` 中的模型名称即可，无需改代码。

如果要换成非阿里云的模型（如 OpenAI），需要修改 `model/factory.py` 中的工厂类。

---

## License

MIT

---

<div align="center">

**如果这个项目对你有帮助，请给一个 Star 支持一下！**

</div>
