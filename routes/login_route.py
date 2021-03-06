from flask import render_template, session, redirect, request
from travelbug import app
import pyrebase
from login_form import LoginForm

config = {
    "apiKey": "AIzaSyBNT4gDmMljV3Oko-E5WLMnNvW9mBfQ5FE",
    "authDomain": "travel-bugg.firebaseapp.com",
    "databaseURL": "https://travel-bugg.firebaseio.com",
   	"storageBucket": "travel-bugg.appspot.com",
   	"serviceAccount": "serviceAccount"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()


#login
@app.route("/login", methods=['GET', 'POST'])
def login():
	title = "Login"
	template_vars = {
		"title" : title
	}

	form = LoginForm()

	if form.validate_on_submit():
		
		auth = firebase.auth()
		
		try: 
			user_data = auth.sign_in_with_email_and_password(request.form["email"], request.form["password"])		
		except:
			return render_template("login.html",vars = template_vars, form=form, is_error=True)

		ev_bool = db.child('User').child(user_data['localId']).child('UserDetails').child('emailVerified').get().val()

		if(ev_bool == "true"):
			session['uid'] = user_data['localId']
			session['logged_in'] = True
			return redirect('/trips')
		else:
			return render_template("login.html",vars = template_vars, form=form, not_verified=True)


	return render_template("login.html",vars = template_vars, form=form)