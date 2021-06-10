from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import random
from wtforms import Form, StringField
from wtforms.fields import TextField
from wtforms.validators import DataRequired, Length
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class ScoreBoard(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ign = db.Column(db.String(10), nullable=False)
	sc = db.Column(db.Integer, nullable=False, default=0)

	def __repr__(self):
		return 'ScoreBoard' + str(self.id)

class NameForm(Form):
	n1 = TextField('Enter your Gamer Tag:', [DataRequired(message="Enter Your Name Please"), Length(min=3, max=5)])

class GuessForm(Form):
	g1 = TextField('Guess:', [DataRequired(message="Enter Your Guess Please"), Length(min=4, max=4)])


def set_vars():
	session['set_guess'] = random.choice(['fall', 'fell'])
	i = 0
	ar = ["None", "None", "None", "None"]
	
	while i < 4:
		sg = session['set_guess'][i]
		ar[i] = random.choice([sg, '_'])
		i += 1

	session['set_blank'] = ''
	for ch in ar:
		session['set_blank'] += ch
	if session.get('set_score') == None or session.get('set_success') == 3 or session.get('set_state') == 0 :
		session['set_score'] = 0
		session['set_success'] = 1
	


# def gmix(post_guess):
# 	if session.get('set_guess') == None:
# 		set_vars()
# 		return render_template('aa.html')

def win():
	session['set_score'] = session['set_score'] + 1
	session['set_success'] = 1
	set_vars()

def lose():
	session['set_success'] = 2
	post_ign = session['set_ign']
	post_score = session['set_score']
	new_post = ScoreBoard(ign=post_ign, sc=post_score)
	db.session.add(new_post)
	db.session.commit()
	session.pop('set_guess', None)
	session.pop('set_blank', None)
	session.pop('set_score', None)
	session['set_state'] = 3
	return render_template('aa.html')


@app.route('/', methods=['GET', 'POST'])
def main_view():
	form = NameForm(request.form)
	gform = GuessForm(request.form)
	if request.method == 'POST' and session['set_state'] == 0 and form.validate():
		session['set_ign'] = request.form['n1']
		session['set_state'] = 1
		return render_template('aa.html', gform=gform)
	elif request.method == 'POST' and session['set_state'] == 1 and gform.validate():
		if request.form['g1'] == session['set_guess']:
			if win() == None:
				return render_template('aa.html', gform=gform)
		else:
			return lose()
	else:
		if session.get('set_guess') == None or session.get('set_state') == None:
			session['set_state'] = 0
			if set_vars() == None:
				return render_template('aa.html', form=form, gform=gform)
		else:
			# session['set_state'] = 0
			# set_vars()
			return render_template('aa.html', form=form, gform=gform)

@app.route('/scoreboard', methods=['GET'])
def score_view():
	all_scores = ScoreBoard.query.order_by(desc(ScoreBoard.sc)).limit(10)
	return render_template('ss.html', scores=all_scores)