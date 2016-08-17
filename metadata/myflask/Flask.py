#http://courses.pgbovine.net/csc201/week13-code.txt

from flask import Flask, render_template,jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World, Ragha'


@app.route('/user')
def user():
    return 'Hello World, User !'

@app.route('/user/<name>')
def user_name(name):
    myobject = data()
    return render_template('Home.html',name=myobject)
    #return 'Hello World, '+name+ '!'


@app.route('/data')
def data():
    people_data = {"Email":"Ranjith.Kumar@gmail.com","DOB":"23-12-1955","Name":"Ranjith"}
    return people_data
    #return jsonify(people_data)


if __name__ == '__main__':
    app.run(debug=True)
