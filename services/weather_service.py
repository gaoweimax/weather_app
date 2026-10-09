# ============================================================
# 天气业务逻辑层：负责翻译天气、生成出行建议
# 这个文件不负责接收请求，也不负责返回数据
# 只负责"纯计算"和"纯逻辑"
# ============================================================

# ---------- 1. 天气英文转中文对照表 ----------
WEATHER_CN = {
    "Sunny": "晴", "Clear": "晴",
    "Partly cloudy": "多云", "Cloudy": "多云",
    "Overcast": "阴", "Mist": "薄雾", "Fog": "雾",
    "Light rain": "小雨", "Rain": "雨", "Heavy rain": "大雨",
    "Snow": "雪", "Thunderstorm": "雷雨",
}


# ---------- 2. 生成建议和推荐地点的函数 ----------
def make_tip_and_recommend(temp, humidity, desc_en):
    """根据温度、湿度、天气，生成出行建议和推荐地点"""
    d = desc_en.lower()
    tip = ""
    recommend = ""

    # 天气原因优先判断
    if "rain" in d or "thunder" in d:
        tip = "记得带伞，出门注意防滑，尽量选择室内活动。"
        recommend = "博物馆、商场、咖啡馆、室内展览馆"
    elif "snow" in d:
        tip = "有雪，注意保暖，路面可能结冰，出行请穿防滑鞋。"
        recommend = "温泉、室内滑雪场、温暖的书店"
    elif temp >= 30:
        tip = f"天气炎热（{temp}°C），注意防晒补水，避免长时间户外活动。"
        recommend = "水上乐园、室内游泳馆、大型商场（蹭空调）"
    elif temp >= 22:
        tip = f"温度舒适（{temp}°C），非常适合户外出行。"
        recommend = "公园、湖边、步行街、风景区"
    elif temp >= 12:
        tip = f"微凉（{temp}°C），建议加件薄外套再出门。"
        recommend = "Citywalk、特色书店、艺术街区"
    else:
        tip = f"较冷（{temp}°C），穿厚一点再出门，注意防寒。"
        recommend = "室内展览、温泉、火锅店、电影院"

    # 湿度补充建议
    if int(humidity) > 80 and "rain" not in d:
        tip += " 湿度较高，体感可能有些闷热。"
    elif int(humidity) < 30:
        tip += " 空气干燥，记得多喝水，注意保湿。"

    return tip, recommend