# 🚀 Resume LangChain Agent

一个基于 LangChain + Ollama + Streamlit 的本地简历优化 Agent，  
用于自动化完成岗位分析、简历优化、面试准备及多岗位投递支持。

---

## ✨ 项目亮点

- 基于本地大模型（Ollama），支持离线运行
- 多工具协同（岗位分析 / 简历优化 / 面试准备）
- 自定义任务路由（自动识别用户意图）
- 多步骤自动执行（完整求职流程）
- 支持多岗位批量生成简历版本
- 内置对话记忆（memory.json）
- 提供可视化界面（Streamlit）

---

## 📌 核心功能

- 岗位分析：提取岗位核心能力
- 匹配分析：评估简历与岗位匹配度
- 简历优化：生成可投递版本
- 面试准备：生成面试问答
- 批量生成：多岗位简历版本
- 最终导出：投递版简历

---

## 🧠 技术架构

- Python
- LangChain（工具调用 + 路由）
- Ollama（本地模型）
- Streamlit（Web界面）

---

## ⚙️ 运行方式

### 1. 安装依赖pip install -r requirements.txt


### 2. 安装 Ollama 并下载模型

下载：https://ollama.com


ollama pull qwen3


### 3. 启动项目


streamlit run resume_agent.py


---

## 📁 项目结构


resume-langchain-agent/
├── resume_agent.py
├── resume.txt
├── jd.txt
├── jds/
├── outputs/
├── requirements.txt
├── run.bat
└── README.md


---

## 💡 项目说明

解决求职中的问题：

- 不清楚岗位要求
- 简历匹配度低
- 面试准备不足
- 投递效率低

自动流程：

岗位分析 → 匹配分析 → 简历优化 → 面试准备 → 批量生成

---

## 🚀 后续优化方向

- 支持 PDF / Word 简历上传
- 接入在线模型（OpenAI / DeepSeek）
- 多用户支持
- 在线部署
