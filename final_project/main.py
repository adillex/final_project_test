from flask import Flask, render_template, url_for, request, redirect, Blueprint, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = "ADIL"
db = SQLAlchemy()
db.init_app(app)
print(db.session)


class Support:
    @staticmethod
    def hashPassword(password):
        return hash(password)


# class Session:
#     def __init__(self, id=None, is_session=False):
#         self.id = id
#         self.is_session = is_session
#
#
# session = Session()

class Request_to_ans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productId = db.Column(db.Integer, nullable=False)
    studentName = db.Column(db.String(100), nullable=False)
    studentId = db.Column(db.Integer, nullable=False)
    masterName = db.Column(db.String(100), nullable=False)
    masterId = db.Column(db.Integer, nullable=False)
    masterCard = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(250), nullable=False)
    status = db.Column(db.Integer, nullable=False)  # bool true=1 false=0

    def __repr__(self):
        return '<Request_to_ans %r>' % self.id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    userName = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    text = db.Column(db.Text, nullable=False)
    card = db.Column(db.String(100), unique=True, nullable=False)
    phoneNumber = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.Text, nullable=False)
    password = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.id


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(100), nullable=False)
    masterId = db.Column(db.String(100), nullable=False)
    masterUserName = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    intro = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    class_name = db.Column(db.Text, nullable=False)
    lector = db.Column(db.Text, nullable=False)
    photo = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Product %r>' % self.id


with app.app_context():
    db.create_all()


@app.route('/')
@app.route('/home')
def main():
    products = Product.query.order_by(Product.date.desc()).all()
    # return render_template('wall.html')
    return render_template('wall.html', products=products)


@app.route('/profile')
def go_to_profile():
    return redirect('/profile/' + str(session['id']))


@app.route('/user_profile')
def go_to_user_profile():
    return redirect('/user_profile/' + str(session['id']))


@app.route('/profile/<int:id>')
def user_profile(id):
    user = User.query.get(id)
    return render_template('userProfile.html', user=user, session=session)


@app.route('/productProfile/<int:id>')
def productProfile(id):
    product = Product.query.get(id)
    return render_template('productProfile.html', product=product, session=session)


@app.route('/profile/<int:id>/delete')
def profile_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/logout')


@app.route('/productProfile/<int:id>/delete')
def product_delete(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect('/main')


@app.route('/productProfile/<int:id>/redact', methods=["POST", "GET"])
def product_redact(id):
    product = Product.query.get(id)
    if request.method == "POST":
        product.productName = request.form['productName']
        product.photo = request.form['photo']
        product.text = request.form['text']
        product.price = request.form['price']
        # try:
        db.session.add(product)
        db.session.commit()
        return redirect('/')

        # except:
        #     return "при добавлении статьи произошла ошибка"

    else:
        return render_template("productRedact.html", product=product)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/registration', methods=["POST", "GET"])
def registration():
    if request.method == "POST":
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        userName = request.form['username']
        email = request.form['email']
        Phone_Number = request.form['Phone_Number']
        card = request.form['card']
        photo = request.form['photo']
        text = request.form['text']
        password = request.form['password']

        user = User(firstName=firstName,
                    lastName=lastName,
                    userName=userName,
                    email=email,
                    phoneNumber=Phone_Number,
                    card=card,
                    photo=photo,
                    text=text,
                    password=password)

        # try:
        db.session.add(user)
        db.session.commit()
        session['authenticated'] = True
        session['username'] = user.userName
        session['id'] = user.id
        return redirect('/')
        # except:
        #     return "при добавлении статьи произошла ошибка"

    else:
        return render_template("registration.html")


@app.route('/productRegistration', methods=["POST", "GET"])
def product_registration():
    if request.method == "POST":

        productName = request.form['productName']
        masterId = session['id']
        masterUserName = session['username']
        url = request.form['url']
        intro = request.form['intro']
        class_name = request.form['class_name']
        lector = request.form['lector']
        photo = request.form['photo']
        text = request.form['text']
        price = request.form['price']

        product = Product(productName=productName,
                          masterId=masterId,
                          masterUserName=masterUserName,
                          url=url,
                          intro=intro,
                          class_name=class_name,
                          lector=lector,
                          photo=photo,
                          price=price,
                          text=text)

        # try:
        db.session.add(product)
        db.session.commit()
        return redirect('/')
        # except:
        #     return "при добавлении статьи произошла ошибка"

    else:
        return render_template("productRegistration.html")


@app.route('/logout')
def logout():
    session['authenticated'] = False
    session['username'] = None
    session['id'] = None
    return redirect("/")


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = db.session.query(User).filter_by(userName=request.form['username'],
                                                password=request.form['password']).first()
        print(user)
        if user:
            session['authenticated'] = True
            session['id'] = user.id
            session['username'] = user.userName
            return redirect("/")
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")


@app.route('/demand', methods=["POST", "GET"])
def demand():
    demands = db.session.query(Request_to_ans).filter_by(masterId=session['id']).all()
    return render_template("login.html", demands=demands)


class Config(object):
    SECRET_KEY = 'my-secrete-key'


if __name__ == "__main__":
    app.run(debug=True)
