# ============================================================
# AI 业务逻辑层：用 requests 直接调用 DeepSeek 接口
# 不需要 openai 库，只依赖你早就装好的 requests
# ============================================================

import requests
import json

# ⚠️ 唯一需要修改的地方：把下面引号里的内容，换成你真实的 sk-xxx 密钥
MY_API_KEY = "sk-b07080d2c768472bb3090d54564e2060"


def deduce_activity(city, activity):
    """调用 DeepSeek 接口，生成行动推演"""

    # 组装给 AI 的提示词
    prompt = f"用户在{city}，计划进行{activity}。请结合天气影响，用一段话（80字以内）给出是否适合、主要风险、以及备选建议。"

    # 请求头：把密钥和内容类型告诉服务器
    headers = {
        "Authorization": f"Bearer {MY_API_KEY}",
        "Content-Type": "application/json"
    }

    # 请求体：消息内容
    body = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        # 向 DeepSeek 的接口发 POST 请求
        r = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers=headers,
            json=body,
            timeout=30
        )
        r.raise_for_status()

        # 从返回的 JSON 里提取 AI 回复的文字
        data = r.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"AI推演失败: {str(e)}"