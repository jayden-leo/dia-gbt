import spacy
import os
import subprocess

os.environ['http_proxy'] = "http://localhost:7890"
os.environ['https_proxy'] = "https://localhost:7890"

model_name = "en_core_web_sm"
spacy.cli.download(model_name)

# command = "ls -l"  # 替换为您想要运行的 shell 命令
#
# try:
#     # 使用subprocess模块运行 shell 命令，并捕获输出
#     result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
#     # 输出命令的标准输出
#     print("标准输出:")
#     print(result.stdout)
#     # 输出命令的标准错误
#     print("标准错误:")
#     print(result.stderr)
#     print("命令运行成功。")
# except subprocess.CalledProcessError as e:
#     print("命令运行时出现错误:", e)
