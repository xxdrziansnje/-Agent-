# 扫地机器人智能客服 Agent

> LangGraph ReAct Agent + 通义千问(qwen3-max) + Chroma + Streamlit

## 启动方式
```bash
streamlit run app.py
```

## 目录结构
```
app.py                    # Streamlit 入口
config/
  rag.yml                 # chat_model_name: qwen3-max, embedding: text-embedding-v4
  chroma.yml              # chunk_size:200, overlap:20, k:3
  prompts.yml             # 三个提示词 .txt 路径
  agent.yml               # external_data_path
prompts/
  main_prompt.txt         # 标准客服 ReAct 系统提示
  rag_summarize.txt       # RAG摘要子提示 (含 {input} {context} 模板变量)
  report_prompt.txt       # 报告生成提示 (强制工具调用顺序)
agent/
  react_agent.py          # ReactAgent 类: create_agent() + execute_stream()
  tools/
    agent_tools.py        # 7个 @tool 工具
    middleware.py          # 3个中间件: monitor_tool, log_before_model, report_prompt_switch
model/
  factory.py              # ChatModelFactory + EmbeddingsFactory 单例
rag/
  rag_service.py          # RagSummarizeService: 检索+LCEL摘要链
  vector_store.py         # VectorStoreService: Chroma管理+文档ETL
  chroma_db/              # RAG层 Chroma 持久化存储
data/
  *.txt, *.pdf            # 6个知识库文档 (扫地机器人FAQ/故障/保养/选购)
  external/records.csv    # 10用户×12月模拟使用记录
utils/
  config_handler.py       # YAML配置模块级单例 (rag_conf, chroma_conf, prompts_conf, agent_conf)
  prompt_loader.py        # 从磁盘加载 .txt 提示词
  file_handler.py         # MD5去重, PDF/TXT加载器, 目录遍历
  logger_handler.py       # 控制台+文件双通道日志
  path_tool.py            # get_abs_path() 相对→绝对路径
md5.text                  # 已入库文档MD5注册表
```

## 核心架构

### 两种运行模式（通过运行时上下文切换）
- **普通模式** (context.report=false): 加载 main_prompt.txt, 标准 ReAct 客服问答
- **报告模式** (context.report=true): 加载 report_prompt.txt, 强制工具链生成Markdown报告

### 提示切换机制（关键设计）
```
fill_context_for_report 工具(空触发器)
  → monitor_tool 中间件捕获 → 设置 context["report"] = True
  → report_prompt_switch 中间件(@dynamic_prompt) 读 context → 切换提示词文件
```

### 7个工具
| # | 工具 | 类型 | 说明 |
|---|------|------|------|
| 1 | rag_summarize | 真实RAG | Chroma检索(k=3)→LCEL链→LLM摘要 |
| 2 | get_weather | 模拟 | 固定天气字符串 |
| 3 | get_user_location | 模拟 | 随机城市[深圳,合肥,杭州] |
| 4 | get_user_id | 模拟 | 随机ID 1001-1010 |
| 5 | get_current_month | 模拟 | 随机12个月份 |
| 6 | fetch_external_data | 真实文件 | 查询 records.csv |
| 7 | fill_context_for_report | 触发器 | 无业务逻辑，仅触发提示切换 |

### 3个中间件
| 中间件 | 装饰器 | 作用 |
|--------|--------|------|
| monitor_tool | @wrap_tool_call | 记录工具执行 + 捕获 fill_context_for_report |
| log_before_model | @before_model | 记录LLM调用前状态 |
| report_prompt_switch | @dynamic_prompt | 条件选择提示词文件 |

### 关键单例（导入时创建）
- `model/factory.py` → chat_model (ChatTongyi), embed_model (DashScopeEmbeddings)
- `utils/config_handler.py` → rag_conf, chroma_conf, prompts_conf, agent_conf
- `utils/logger_handler.py` → logger

### RAG 链路
```
用户查询 → retriever.invoke(query)
  → Chroma similarity_search(k=3)
  → 格式化文档为【参考资料N】
  → LCEL链: prompt_template | chat_model | StrOutputParser()
  → 返回AI摘要
```

### 文档ETL
```
data/扫描 → 过滤 .txt/.pdf → MD5去重(md5.text)
  → TextLoader/PyPDFLoader → RecursiveCharacterTextSplitter(chunk=200,overlap=20)
  → DashScopeEmbeddings → Chroma.add_documents() → 注册MD5
```
独立执行: `python rag/vector_store.py`

### Streamlit 流式输出
`execute_stream()` 用 `agent.stream(stream_mode="values")` 获取字符块, capture() 内部函数缓冲 + 10ms字符间延迟实现打字机效果。
