from flask import Flask, render_template, request, session, send_file
from matplotlib import pyplot as plt
from flask_session.__init__ import Session

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
coordinates = []
xlabel = "x-axis"
ylabel = "y-axis"
title = "Coordinate Title"


@app.route("/")
def index():
    return render_template("index.html", coordinates=coordinates)


@app.route("/add-coordinate", methods=["POST"])
def add_coordinate():
    x = float(request.form["x"])
    y = float(request.form["y"])
    if len(coordinates) == 0:
        global title
        title = request.form["coord-name"]
        global xlabel
        xlabel = request.form["x-label"]
        global ylabel
        ylabel = request.form["y-label"]
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
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
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


@app.route("/download-plot", methods=["GET"])
def download_plot():
    image_path = "static/plot.png"
    filename = "plot.png"
    return send_file(image_path, as_attachment=True, download_name=filename)


if __name__ == "__main__":
    app.secret_key = "somethingseeecret"
    app.run()
