cd %~dp0
python -m venv exec_env
exec_env\Scripts\activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple