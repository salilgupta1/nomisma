from flask import Flask, session, redirect, url_for, render_template, request
from controllers.UserAuth import UserAuth
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTING'])

userAuth = UserAuth()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/auth/registerUser', methods=['GET','POST'])
def registerUser():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		result = userAuth.completeRegistration(username,password)

		if result == True:
			# clear out sessions
			session.pop('logged_in', None)
			session.pop('username', None)
			# go to the users dashboard
			return render_template('dashboard.html')
		else:
			return result
	else:
		# authenticate a user with venmo
		v_username = userAuth.authorizeWithVenmo(request.args.get('code'))
		
		return render_template('registerUser.html',username = v_username)

@app.route('/login' , methods=['GET','POST'])
def login():
	error = None
	if request.method =='POST':
		username = request.form['username']
		password = request.form['password']

		is_authenticated = userAuth.authenticateUser(username,password)

		if is_authenticated == True:
			session['logged_in'] = True
			session['username'] = username
			return render_template('dashboard.html')
		else:
			error = is_authenticated
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	session.pop('username', None)

	return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
