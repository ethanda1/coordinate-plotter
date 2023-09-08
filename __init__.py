from flask import Flask, render_template, request, session, flash
from matplotlib import pyplot as plt

app = Flask(__name__)

coordinates = []


@app.route("/")
def index():
    return render_template("index.html", coordinates=coordinates)


@app.route("/add-coordinate", methods=["POST"])
def add_coordinate():
    x = float(request.form["x"])
    y = float(request.form["y"])
    coordinates.append((x, y))
    return render_template("index.html", coordinates=coordinates)


@app.route("/reset", methods=["POST"])
def reset():
    global coordinates
    coordinates = []
    session.clear()
    return render_template("index.html", coordinates=coordinates)


@app.route("/plot", methods=["POST"])
def plot():
    if len(coordinates) > 0:
        plt.figure(figsize=(8, 6))
        plt.scatter(*zip(*coordinates), marker="o", label="Coordinates")
        plt.xlabel("X-coordinate")
        plt.ylabel("Y-coordinate")
        plt.title("Coordinate Plot")
        plt.legend()
        plt.grid(True)
        plt.savefig("static/plot.png")
        return render_template(
            "index.html", plot_url="static/plot.png", coordinates=coordinates, plot=True
        )
    else:
        return render_template(
            "index.html", plot_url="static/plot.png", coordinates=coordinates, plot=True
        )


if __name__ == "__main__":
    app.secret_key = "your_secret_key_here"
    app.run()
