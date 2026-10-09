# ============================================================
# 天气路由层：负责定义网址、接收请求、返回响应
# ============================================================

from flask import Blueprint, request, jsonify
import requests
from models.database import save_record, get_history
from services.weather_service import WEATHER_CN, make_tip_and_recommend
from services.health_service import check_health

weather_bp = Blueprint('weather', __name__)


@weather_bp.route("/api/weather")
def weather():
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "请输入城市名"})

    url = f"https://wttr.in/{city}?format=j1"
    headers = {"User-Agent": "curl/7.68.0"}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()

        current = data["current_condition"][0]
        pressure = current["pressure"]
        wind_dir = current["winddir16Point"]
        wind_speed = current["windspeedKmph"]
        visibility = current["visibility"]
        precip = current["precipMM"]
        temp = int(current["temp_C"])
        feels = current["FeelsLikeC"]
        humidity = current["humidity"]
        desc_en = current["weatherDesc"][0]["value"].strip()
        desc = WEATHER_CN.get(desc_en, desc_en)

        all_days = data["weather"]
        forecast_7d = []
        for day in all_days:
            day_data = {
                "date": day["date"],
                "maxtemp": day["maxtempC"],
                "mintemp": day["mintempC"],
                "hourly": []
            }
            for hour_data in day["hourly"]:
                t = hour_data["time"].zfill(4)
                day_data["hourly"].append({
                    "time": t[:2] + ":" + t[2:],
                    "temp": hour_data["tempC"],
                    "rain_chance": hour_data["chanceofrain"]
                })
            forecast_7d.append(day_data)

        tip, recommend = make_tip_and_recommend(temp, humidity, desc_en)
        health_warnings = check_health(pressure, humidity, temp, feels)
        save_record(city=city, temp=temp, desc=desc)

        return jsonify({
            "temp": temp,
            "feels": feels,
            "humidity": humidity,
            "desc": desc,
            "pressure": pressure,
            "wind_dir": wind_dir,
            "wind_speed": wind_speed,
            "visibility": visibility,
            "precip": precip,
            "tip": tip,
            "recommend": recommend,
            "forecast_7d": forecast_7d,
            "health_warnings": health_warnings
        })

    except requests.exceptions.Timeout:
        return jsonify({"error": "请求超时，请稍后重试"})
    except requests.exceptions.HTTPError:
        return jsonify({"error": f"找不到城市「{city}」，请检查拼音拼写"})
    except Exception as e:
        return jsonify({"error": "查询失败：" + str(e)})


# ============================================================
# 历史记录接口（注意：这里必须顶格写，不能缩进）
# ============================================================
@weather_bp.route("/api/history")
def history():
    records = get_history(10)
    return jsonify(records)