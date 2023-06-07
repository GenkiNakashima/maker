from flask import Flask, render_template, request
from cotoha1_api import anaume
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ana1', methods=["GET", "POST"])
def ana1():
    if request.method == "GET":
        return render_template('anaume1.html')
    elif request.method == "POST":
        # 追加箇所
        text = request.form["input_text"]
        question=anaume(text)
        return render_template('anaume2.html',question=question)
    

@app.route('/ana2')
def ana2():
    return render_template('anaume2.html')

if __name__ == "__main__":
    app.run(debug=True)