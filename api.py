from flask import Flask, render_template

app = Flask()

@app.route("/", methods=["get"])
def home():
    render_template("index.html")


if __name__ == "__main__":
    app.run(port=3000)