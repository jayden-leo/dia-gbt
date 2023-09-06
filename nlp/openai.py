import openai
import os
from disambiguator.status import status_info, Status

# key = os.getenv('OPENAI_API_KEY')
# print(str(key))
openai.api_key = "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"


def get_completion(prompt_text, temperature=0, model="gpt-3.5-turbo"):
    """
    :param prompt_text: your command
    :param temperature: stability of llm replies
    :param model: default:"gpt-3.5-turbo". you can use "gpt-4" if you have qualification
    :return: result from llm
    """
    messages = [{"role": "user", "content": prompt_text}]
    try:
        responses = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,  # 模型输出的温度系数，控制输出的随机程度
            timeout=10
        )
        responses = responses.choices[0].message["content"]
    except Exception as e:
        responses = status_info[Status.ERROR_LLM] + str(e)
    # 调用 OpenAI 的 ChatCompletion 接口
    return responses
