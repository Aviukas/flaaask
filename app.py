from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from models import User, Group, Bill
from forms import RegistrationForm, LoginForm, GroupForm, BillForm


if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
@login_required
def home():
    group_form = GroupForm()
    if group_form.validate_on_submit():
        group = Group(name=group_form.name.data)
        group.users.append(current_user)
        db.session.add(group)
        db.session.commit()
        flash('Group created!')
        return redirect(url_for('home'))
    return render_template('home.html', group_form=group_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your username and/or password.')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/group/<int:group_id>', methods=['GET', 'POST'])
@login_required
def group(group_id):
    group = Group.query.get_or_404(group_id)
    if current_user not in group.users:
        flash("You don't have access to this group.")
        return redirect(url_for('home'))
    bill_form = BillForm()
    if bill_form.validate_on_submit():
        bill = Bill(description=bill_form.description.data, amount=bill_form.amount.data, payer_id=bill_form.payer_id.data, group_id=group_id)
        db.session.add(bill)
        db.session.commit()
        flash('Bill added!')
        return redirect(url_for('group', group_id=group_id))
    return render_template('group.html', group=group, bill_form=bill_form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# if __name__ == '__main__':
#     app.run(debug=True)