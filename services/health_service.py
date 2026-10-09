# ============================================================
# 健康业务逻辑层：根据气象数据，结合用户体质，生成健康预警
# ============================================================

def check_health(pressure, humidity, temp, feels):
    """
    接收气压、湿度、温度、体感温度，返回健康预警列表
    现在是硬编码规则，以后你可以随意增加
    """
    warnings = []

    # 转成数字方便比较
    pressure = int(pressure)
    humidity = int(humidity)
    temp = int(temp)

    # 规则1：气压过低 -> 关节痛
    if pressure < 1005:
        warnings.append("🦴 气压较低，关节敏感人群请注意保暖防潮。")

    # 规则2：空气干燥 -> 鼻炎/呼吸道
    if humidity < 30:
        warnings.append("👃 空气干燥，鼻炎或呼吸道敏感人群建议多喝水，使用加湿器。")

    # 规则3：空气闷湿 -> 体感不适
    if humidity > 80 and temp > 25:
        warnings.append("💦 空气闷热潮湿，心血管敏感人群请避免剧烈户外运动。")

    # 规则4：高温 -> 中暑风险
    if temp >= 35:
        warnings.append("🔥 高温预警，注意防暑降温，避免长时间暴晒。")

    # 如果没有任何警告
    if not warnings:
        warnings.append("✅ 今日气象条件平稳，身体状况良好。")

    return warnings