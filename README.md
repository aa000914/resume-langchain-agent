# 🚀 Resume LangChain Agent

一个基于 **LangChain + Ollama + Streamlit** 的本地简历优化 Agent，  
用于提升求职效率，支持岗位分析、简历优化、面试准备及多岗位批量生成。

---

## ✨ 项目亮点

- 🔹 基于本地大模型（Ollama），无需调用外部API
- 🔹 多工具调用（岗位分析 / 简历优化 / 面试准备）
- 🔹 自定义任务路由（自动识别用户意图）
- 🔹 支持多步骤自动执行（完整求职流程）
- 🔹 支持多岗位批量生成简历版本
- 🔹 内置对话记忆（memory.json）
- 🔹 提供可视化界面（Streamlit）

---

## 📌 核心功能

- 📊 岗位分析：提取岗位核心能力要求  
- 📈 匹配分析：评估简历与岗位匹配度  
- ✍️ 简历优化：生成可投递版本简历  
- 🎯 面试准备：生成高频问题 + 参考回答  
- 📂 批量生成：针对多个岗位生成不同版本简历  
- 📄 最终导出：生成最终投递版简历  

---

## 🧠 技术架构

- Python  
- LangChain（工具调用 + 路由机制）  
- Ollama（本地大模型）  
- Streamlit（Web界面）  

---

## ⚙️ 快速运行

### 1️⃣ 安装依赖

```bash
pip install -r requirements.txt
2️⃣ 安装 Ollama

下载并安装：

👉 https://ollama.com

安装完成后执行：

ollama pull qwen3
3️⃣ 启动项目
streamlit run resume_agent.py
📁 项目结构
resume-langchain-agent/
├── resume_agent.py     # 主程序
├── requirements.txt    # 依赖
├── run.bat             # 一键启动（Windows）
├── resume.txt          # 原始简历（本地使用）
├── jd.txt              # 当前岗位描述
├── jds/                # 多岗位JD文件夹
├── outputs/            # 输出结果
└── README.md
💡 项目价值

该项目用于解决求职过程中的核心问题：

不清楚岗位要求重点
简历与岗位匹配度低
面试准备不足
多岗位投递效率低

通过 Agent 自动完成：

👉 岗位分析 → 简历优化 → 面试准备 → 批量生成
