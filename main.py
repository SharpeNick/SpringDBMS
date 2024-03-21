from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/graphs')
def graphs():
    return render_template('graphs.html')

@app.route('/pay')
def pay():
    return render_template('pay.html')

@app.route('/appt')
def appt():
    return render_template('appt.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)