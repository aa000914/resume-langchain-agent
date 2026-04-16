# 🚀 Resume LangChain Agent

一个基于 **LangChain + Ollama + Streamlit** 的本地简历优化 Agent，  
支持岗位分析、简历优化、面试准备以及多岗位批量生成。

---

## ✨ 项目亮点

- 🔹 基于本地大模型（Ollama），无需调用外部API
- 🔹 多工具调用（岗位分析 / 简历优化 / 面试准备）
- 🔹 自定义任务路由（自动判断用户意图）
- 🔹 支持多步骤自动执行（完整求职流程）
- 🔹 支持多岗位批量生成简历版本
- 🔹 内置对话记忆（memory.json）
- 🔹 提供可视化界面（Streamlit）

---

## 📌 核心功能

- 📊 岗位分析：提取岗位核心能力要求
- 📈 匹配分析：评估简历与岗位匹配度
- ✍️ 简历优化：生成可投递版本简历
- 🎯 面试准备：生成高频问题+参考回答
- 📂 批量生成：针对多个岗位生成不同版本简历
- 📄 最终导出：生成最终投递版简历

---

## 🧠 技术架构

- Python
- LangChain（工具调用 + 路由）
- Ollama（本地大模型）
- Streamlit（前端界面）

---

## ⚙️ 运行方式

```bash
pip install -r requirements.txt
streamlit run resume_agent.py
