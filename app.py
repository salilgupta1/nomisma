from flask import Flask, session, redirect, url_for, render_template, request
from controllers.UserAuthController import UserAuthController
from controllers.AnalyticsController import AnalyticsController
import os, pprint

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTING'])

userAuth = UserAuthController()
analytics = AnalyticsController()
# home page
@app.route('/')
def index():
	if 'logged_in' in session and session['logged_in'] == True:
		return redirect(url_for('dashboard'))
	else:
		return render_template('index.html',client_id=os.environ['client_id'])

#### Analytics pages
@app.route('/dashboard', methods=['GET'])
def dashboard():
	return render_template('dashboard.html')

@app.route('/setup', methods=['GET'])
def setup():
	if 'logged_in' in session and session['logged_in'] == True:
		analytics.setUsername(session['username'])

		pullError = analytics.pullData(True)
		if pullError == True:
			refineError= analytics.refineData()
			if refineError == True:
				insertError = analytics.insertData()
				if insertError == True:
					print "Complete!"

	else:
		return redirect(url_for('index'))
	return redirect(url_for('dashboard'))

# user pages
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
			session['logged_in'] = True
			session['username'] = username

			# do the first data retrieval from venmo
			return redirect(url_for('setup'))
		else:
			return result
	else:
		# authenticate a user with venmo
		v_username = userAuth.authorizeWithVenmo(request.args.get('code'))
		
		return render_template('auth/registerUser.html',username = v_username)

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
			# go to user dashboard
			return redirect(url_for('dashboard'))
		else:
			error = is_authenticated
	return render_template('auth/login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	session.pop('username', None)

	return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
