from flask import Flask, render_template

app = Flask(__name__, template_folder="./")


@app.route('/')
def index():
    return render_template("index.html")


app.run(port=4000, host='0.0.0.0')
