import os
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB

from app import app, db
from app.forms import LoginForm, AnalyzeForm, RegistrationForm, SubmissionForm, TrainForm
from app.models import User, Submission


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    submissions = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, submissions=submissions)


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    form = AnalyzeForm()
    if form.validate_on_submit():
        sentence = form.sentence.data
        model = joblib.load('./ml_backend/pickled_objects/bernoulli_model.pkl')
        countvectorizer = joblib.load('./ml_backend/pickled_objects/countvectorizer.pkl')
        prediction = model.predict(countvectorizer.transform([sentence]))[0]
        if prediction == 1:
            prediction = "Good"
        elif prediction == 0:
            prediction = "Bad"
        flash('Sentence: {} | Sentiment: {}.'.format(sentence, prediction))
        return redirect(url_for('analyze'))
    return render_template('analyze.html', title='Analyze', form=form)


@app.route('/train', methods=['GET', 'POST'])
@login_required
def train():
    form = TrainForm()
    if form.validate_on_submit():
        sentence_list = []
        is_good_list = []
        submissions = Submission.query.all()
        for submission in submissions:
            sentence_list.append(submission.sentence)
            is_good_list.append(int(submission.is_good))
        # ML Model
        countvectorizer = CountVectorizer(binary='true')
        sentence_list = countvectorizer.fit_transform(sentence_list)
        model = BernoulliNB().fit(sentence_list, is_good_list)
        # Pickle ML model and replace old model
        os.remove("./ml_backend/pickled_objects/countvectorizer.pkl")
        os.remove("./ml_backend/pickled_objects/bernoulli_model.pkl") # FIX 1
        joblib.dump(countvectorizer, "./ml_backend/pickled_objects/countvectorizer.pkl")
        joblib.dump(model, './ml_backend/pickled_objects/bernoulli_model.pkl')
        flash("Thank you for helping the machines! Your work won't go unnoticed in our dystopian future!")
        return redirect(url_for('train'))
    return render_template('train.html', title='Train', form=form)


@app.route('/add_submission', methods=['GET', 'POST'])
@login_required
def add_submission():
    form = SubmissionForm()
    if form.validate_on_submit():
        submission = Submission(sentence=form.sentence.data, is_good=form.is_good.data, author=current_user)
        db.session.add(submission)
        db.session.commit()
        flash('Thank you, add another or train our model!!')
        return redirect(url_for('add_submission'))
    return render_template('add_submission.html', title='Add Submission', form=form)
