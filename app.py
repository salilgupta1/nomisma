from flask import Flask, session, redirect, url_for, render_template, request, jsonify
from controllers.UserAuthController import UserAuthController
from controllers.AnalyticsController import AnalyticsController
import os, string, random, simplejson

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
	if 'logged_in' in session and session['logged_in'] == True:
		if analytics.getUsername() == None:
			analytics.setUsername(session['username']) 
		analytics.updateAnalytics()
		return render_template('dashboard.html')
	else:
		return redirect(url_for('index'))

@app.route('/retrieveCharts',methods=['GET'])
def getCharts():
	if session['csrf_token'] != request.args.get('csrf_token'):
		return redirect(url_for('logout'))
	
	data = analytics.getCharts()
	return jsonify(data)

@app.route('/retrieveStandAlones', methods=['GET'])
def getStandAlones():
	if session['csrf_token'] != request.args.get('csrf_token'):
		return redirect(url_for('logout'))

	data = analytics.getStandAlones()
	return jsonify(data)

#### User pages
@app.route('/auth/registerUser', methods=['GET','POST'])
def registerUser():
	if request.method == 'POST':
		# complete user reg
		username = request.form['username']
		password = request.form['password']
		userAuth.completeRegistration(username,password)

		# add the user data to session
		session['logged_in'] = True
		session['username'] = username
		return redirect(url_for('dashboard'))
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
	session.pop('__csrf_token',None)

	return redirect(url_for('index'))

def generate_csrf_token():
	try:
		if 'csrf_token' not in session or session['csrf_token'] is None:
			session['csrf_token'] = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
		return session['csrf_token']
	except:
		raise

# give jinja ability to store and create a csrf token
app.jinja_env.globals['csrf_token'] = generate_csrf_token

if __name__ == '__main__':

	app.run()
