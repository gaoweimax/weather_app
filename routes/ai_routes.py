# ============================================================
# AI 路由层：定义 /api/deduce 接口，接收前端请求
# ============================================================
from models.database import save_record
from flask import Blueprint, request, jsonify
from services.ai_service import deduce_activity

# 创建蓝图
ai_bp = Blueprint('ai', __name__)

@ai_bp.route("/api/deduce")
def deduce():
    # 接收前端传来的城市和活动
    city = request.args.get("city", "guangzhou")
    activity = request.args.get("activity", "跑步")

    # 调用 AI 大脑进行推演
    result_text = deduce_activity(city, activity)
    save_record(city=city, temp="", desc="", activity=activity, ai_result=result_text)

    # 返回 JSON 给前端
    return jsonify({"result": result_text})