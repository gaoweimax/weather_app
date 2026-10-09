from flask import Flask, render_template
from routes.weather_routes import weather_bp
from models.database import init_db

# 暂时先注释掉AI，等我们把天气部分跑通，再打开它
from routes.ai_routes import ai_bp

app = Flask(__name__)

# 把天气路由挂载进来
app.register_blueprint(weather_bp)
app.register_blueprint(ai_bp)

@app.route("/")
def home():
    return render_template("index.html")
init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5000)