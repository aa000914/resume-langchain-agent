import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import streamlit as st
from langchain_ollama import ChatOllama

# =========================
# 基础配置
# =========================
MODEL_NAME = "qwen3"
APP_DIR = Path(__file__).parent
RESUME_FILE = APP_DIR / "resume.txt"
JD_FILE = APP_DIR / "jd.txt"
JDS_DIR = APP_DIR / "jds"
OUTPUT_DIR = APP_DIR / "outputs"
MEMORY_FILE = OUTPUT_DIR / "memory.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
JDS_DIR.mkdir(parents=True, exist_ok=True)

llm = ChatOllama(model=MODEL_NAME)

BASE_RULE = """
严禁编造不存在的经历、技能、项目、证书、工具、成果或量化数据。
如果原始简历里没有明确写出某项技能或工具，不能擅自添加。
只能基于已有信息做更专业的表达。
如果能力不足，只能写“基础了解”“接触过”“具备基础能力”，
不能写成“精通”“熟练掌握”“独立负责复杂项目”。
输出要简洁直接，格式稳定，不要长篇大论。
"""


# =========================
# 文件与记忆
# =========================
def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def save_result(subdir: str, prefix: str, content: str) -> str:
    target_dir = OUTPUT_DIR / subdir
    target_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = target_dir / f"{prefix}_{timestamp}.txt"
    file_path.write_text(content, encoding="utf-8")
    return str(file_path)


def load_memory() -> Dict:
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {"history": [], "summary": ""}
    return {"history": [], "summary": ""}


def save_memory(memory: Dict) -> None:
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    MEMORY_FILE.write_text(json.dumps(memory, ensure_ascii=False, indent=2), encoding="utf-8")


def add_memory(user_input: str, result: str) -> None:
    memory = load_memory()
    memory.setdefault("history", [])
    memory["history"].append(
        {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": user_input,
            "assistant": result[:1200],
        }
    )
    memory["history"] = memory["history"][-12:]

    summary_prompt = f"""
你是求职对话记忆整理器。
请基于以下历史对话，提炼一个简短记忆摘要，供后续回答使用。
要求：
- 只保留对后续求职有帮助的信息
- 100字以内
- 中文输出

历史：
{json.dumps(memory['history'], ensure_ascii=False, indent=2)}
"""
    try:
        memory["summary"] = llm.invoke(summary_prompt).content.strip()
    except Exception:
        pass

    save_memory(memory)


# =========================
# 核心能力函数
# =========================
def analyze_job(jd: str) -> str:
    prompt = f"""
你是招聘专家。

请提取这个岗位最重要的能力，最多5条。

要求：
- 每条一句话
- 简洁直接
- 不要长篇分析
- 不要废话
- 不要写“精通”这种夸张词，除非岗位原文明确要求

【岗位描述】
{jd}
"""
    return llm.invoke(prompt).content


def match_resume(resume: str, jd: str, memory_summary: str = "") -> str:
    prompt = f"""
你是HR顾问。
{BASE_RULE}

请分析这份简历与岗位的匹配度。

要求：
- 用5条以内总结
- 输出包含：
  1. 匹配度（0-100）
  2. 2个优势
  3. 2个短板
  4. 2条建议
- 简洁直接

【记忆摘要】
{memory_summary}

【岗位描述】
{jd}

【简历】
{resume}
"""
    return llm.invoke(prompt).content


def optimize_resume(resume: str, jd: str, memory_summary: str = "") -> str:
    prompt = f"""
你是简历优化专家。
{BASE_RULE}

请把这份简历优化成【初级数据分析师】可投递版本。

特别要求：
- 只能改写表达，不能补充新技能
- 不要出现“精通”“熟练掌握”“独立完成复杂分析”这类超出原文的信息
- 如果原文没写 SQL / Power BI / Tableau / Pandas 项目，就绝对不要添加
- 语言专业但真实
- 输出结构固定为：
【个人优势总结】
【核心技能】
【工作经历】
【教育背景】

【记忆摘要】
{memory_summary}

【岗位描述】
{jd}

【简历】
{resume}
"""
    return llm.invoke(prompt).content


def interview_prep(resume: str, jd: str, memory_summary: str = "") -> str:
    prompt = f"""
你是一位面试官。
{BASE_RULE}

请根据岗位和简历，生成面试准备内容。

要求：
- 输出5个高频面试问题
- 每题给一个简短参考回答
- 回答只能基于现有简历信息
- 如果简历里没有相关经验，就写“可从相近经历迁移回答”
- 最后补充3个最容易被追问的风险点
- 简洁直接，不要写成长文

【记忆摘要】
{memory_summary}

【岗位描述】
{jd}

【简历】
{resume}
"""
    return llm.invoke(prompt).content


def answer_other_question(resume: str, jd: str, user_question: str, memory_summary: str = "") -> str:
    prompt = f"""
你是求职顾问。
{BASE_RULE}

请回答用户的问题。

要求：
- 结合岗位和简历
- 用5条以内说明
- 简洁直接
- 不要长篇解释

【记忆摘要】
{memory_summary}

【岗位描述】
{jd}

【简历】
{resume}

【用户问题】
{user_question}
"""
    return llm.invoke(prompt).content


def export_final_resume(resume: str, jd: str, memory_summary: str = "") -> str:
    prompt = f"""
你是资深求职顾问。
{BASE_RULE}

请基于当前岗位描述，把简历整理成一版“最终投递版”。

要求：
- 语言自然、正式
- 适合直接复制到招聘网站或Word简历
- 不要多余解释
- 输出结构固定为：
【个人优势总结】
【核心技能】
【工作经历】
【教育背景】

【记忆摘要】
{memory_summary}

【岗位描述】
{jd}

【原始简历】
{resume}
"""
    return llm.invoke(prompt).content


def batch_generate_resumes(resume: str) -> str:
    jd_files = list(JDS_DIR.glob("*.txt"))
    if not jd_files:
        return f"未在 {JDS_DIR} 中找到 .txt 岗位文件。"

    summary = []
    for file in jd_files:
        target_jd = file.read_text(encoding="utf-8").strip()
        result = optimize_resume(resume, target_jd)
        save_path = save_result("final_resumes", f"resume_{file.stem}", result)
        summary.append(f"{file.stem} -> {save_path}")
    return "批量生成完成：\n" + "\n".join(summary)


# =========================
# 路由与多步执行
# =========================
def route_task(user_input: str) -> str:
    prompt = f"""
你是任务分类器。

请判断用户输入最符合哪一种需求，只能返回一个数字：
1 = 匹配分析（问简历和岗位匹不匹配、行不行、适不适合、短板）
2 = 优化简历（问修改简历、润色简历、重写简历）
3 = 岗位分析（问岗位最重要的能力、关键词、要求、看重什么）
4 = 面试准备（问面试问题、模拟面试、怎么回答）
5 = 其他求职问题（上面都不明显符合时选5）
6 = 批量生成多个岗位版本简历
7 = 导出最终投递版简历
8 = 自动完整求职流程（岗位分析+匹配分析+优化简历+面试准备）

规则：
- 只返回一个数字
- 不要解释
- 不要输出别的内容

用户输入：
{user_input}
"""
    result = llm.invoke(prompt).content.strip()
    if result not in [str(i) for i in range(1, 9)]:
        return "5"
    return result


def full_workflow(resume: str, jd: str, memory_summary: str = "") -> str:
    step1 = analyze_job(jd)
    step2 = match_resume(resume, jd, memory_summary)
    step3 = optimize_resume(resume, jd, memory_summary)
    step4 = interview_prep(resume, jd, memory_summary)

    return (
        "【步骤1：岗位分析】\n" + step1 + "\n\n"
        + "【步骤2：匹配分析】\n" + step2 + "\n\n"
        + "【步骤3：优化简历】\n" + step3 + "\n\n"
        + "【步骤4：面试准备】\n" + step4
    )


def execute_task(choice: str, user_input: str, resume: str, jd: str, memory_summary: str = "") -> Tuple[str, str]:
    if choice == "1":
        return "match_resume", match_resume(resume, jd, memory_summary)
    if choice == "2":
        return "optimize_resume", optimize_resume(resume, jd, memory_summary)
    if choice == "3":
        return "analyze_job", analyze_job(jd)
    if choice == "4":
        return "interview_prep", interview_prep(resume, jd, memory_summary)
    if choice == "5":
        return "other_question", answer_other_question(resume, jd, user_input, memory_summary)
    if choice == "6":
        return "batch_generate", batch_generate_resumes(resume)
    if choice == "7":
        return "final_resume", export_final_resume(resume, jd, memory_summary)
    if choice == "8":
        return "full_workflow", full_workflow(resume, jd, memory_summary)
    return "unknown", "无法识别任务。"


# =========================
# Streamlit UI
# =========================
st.set_page_config(page_title="简历 Agent V6", layout="wide")
st.title("简历 Agent V6")
st.caption("已补上：记忆、多步自动执行、网页界面、稳定输出")

if "resume_text" not in st.session_state:
    st.session_state.resume_text = read_text(RESUME_FILE)
if "jd_text" not in st.session_state:
    st.session_state.jd_text = read_text(JD_FILE)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.subheader("基础设置")
    model_name = st.text_input("模型名", value=MODEL_NAME)
    st.caption("默认使用 qwen3，本地 Ollama 需已可用")

    st.subheader("记忆")
    memory = load_memory()
    st.text_area("当前记忆摘要", value=memory.get("summary", ""), height=120)
    if st.button("清空记忆"):
        save_memory({"history": [], "summary": ""})
        st.success("已清空 memory.json")

    st.subheader("批量岗位文件夹")
    st.write(str(JDS_DIR))
    st.caption("把多个 JD 的 .txt 文件放进 jds 文件夹")

col1, col2 = st.columns(2)
with col1:
    st.subheader("原始简历")
    resume_text = st.text_area("编辑 resume.txt", value=st.session_state.resume_text, height=320)
    if st.button("保存简历"):
        write_text(RESUME_FILE, resume_text)
        st.session_state.resume_text = resume_text
        st.success("resume.txt 已保存")

with col2:
    st.subheader("当前岗位 JD")
    jd_text = st.text_area("编辑 jd.txt", value=st.session_state.jd_text, height=320)
    if st.button("保存 JD"):
        write_text(JD_FILE, jd_text)
        st.session_state.jd_text = jd_text
        st.success("jd.txt 已保存")

st.subheader("快捷功能")
btn1, btn2, btn3, btn4, btn5 = st.columns(5)
action = None
with btn1:
    if st.button("岗位分析"):
        action = "3"
with btn2:
    if st.button("匹配分析"):
        action = "1"
with btn3:
    if st.button("优化简历"):
        action = "2"
with btn4:
    if st.button("面试准备"):
        action = "4"
with btn5:
    if st.button("完整流程"):
        action = "8"

user_input = st.text_input("直接输入你的问题", placeholder="例如：我最大的短板是什么 / 帮我导出最终投递版简历")

col_run1, col_run2, col_run3 = st.columns(3)
with col_run1:
    run_free = st.button("运行问题")
with col_run2:
    run_batch = st.button("批量生成多个岗位版本")
with col_run3:
    export_final = st.button("导出最终投递版")

if run_batch:
    action = "6"
    user_input = "帮我批量生成多个岗位版本简历"

if export_final:
    action = "7"
    user_input = "帮我导出最终投递版简历"

if run_free and not action:
    action = route_task(user_input or "")

if action:
    current_resume = read_text(RESUME_FILE)
    current_jd = read_text(JD_FILE)
    memory_summary = load_memory().get("summary", "")

    with st.spinner("AI 正在处理..."):
        task_name, result = execute_task(action, user_input, current_resume, current_jd, memory_summary)

    st.subheader("结果")
    st.text_area("输出", value=result, height=420)

    if task_name == "batch_generate":
        st.success("批量简历已保存到 outputs/final_resumes")
    else:
        save_path = save_result("ui_results", task_name, result)
        st.success(f"已保存到：{save_path}")

    add_memory(user_input or f"快捷功能 {action}", result)
    st.session_state.chat_history.append(
        {
            "question": user_input or f"快捷功能 {action}",
            "task": task_name,
            "result": result,
        }
    )

st.subheader("最近记录")
for item in st.session_state.chat_history[-6:][::-1]:
    with st.expander(f"{item['task']} | {item['question'][:40]}"):
        st.write(item["result"])

st.markdown("---")
st.caption("运行方式：streamlit run resume_agent.py")
