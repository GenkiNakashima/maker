from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ana1')
def ana1():
    return render_template('anaume1.html')

@app.route('/ana2')
def ana2():
    return render_template('anaume2.html')

if __name__ == "__main__":
    app.run(debug=True)