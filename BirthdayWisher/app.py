from flask import Flask,render_template,request,redirect,url_for,flash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET','POST'])
def home():
    if request.method=="POST":
        username = request.form.get('username')
        age = request.form.get('age')
        if not username:
            flash("C'mon! At least let us know who we are celebrating...", category='success')
            return redirect(url_for('home',uname=username,age=age))
        if not age:
            flash("Don't shy away from telling your age! We are not storing it anywhere. We are not judging you either :)", category="success")
            return redirect(url_for('home',uname=username,age=age))
        return redirect(url_for('cake',uname=username,age=age))
    return render_template("base.html")

@app.route('/cake', methods=['GET','POST'])
def cake():
    username = request.args.get('uname')
    age = request.args.get('age')
    return render_template("home.html",username=username,age=age)

if __name__ == '__main__':
    app.run(debug=True)