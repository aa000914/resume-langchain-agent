@echo off
echo 正在安装依赖...
pip install -r requirements.txt

echo 启动项目...
streamlit run resume_agent.py

pause
