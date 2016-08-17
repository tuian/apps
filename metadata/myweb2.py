from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello ....Ragha"

@app.route('/tuna')
def tuna():
    return "<H2>Hello tuna</H2>"

if __name__ == "__main__":
    app.run()
