import pyrebase #importing the pyrebase library
from flask import * #importing the flask library
from datetime import datetime #importing the datetime library
import requests #importing the requests library

firebaseConfig = { 
  'apiKey': "AIzaSyAdwG8DptqyooEO6bddDpy3u-VQVAyFfO0",
  'authDomain': "e-learn-937b1.firebaseapp.com",
  'projectId': "e-learn-937b1",
  'storageBucket': "e-learn-937b1.appspot.com",
  'messagingSenderId': "1062121952623",
  'appId': "1:1062121952623:web:fb2a17b941d5f0fa9b449a",
  'measurementId': "G-9QH6CSJC3H",
  'databaseURL': "https://e-learn-937b1-default-rtdb.firebaseio.com/"
  } #configuring the firebase cloud database

firebase=pyrebase.initialize_app(firebaseConfig) #initializing firebase
auth=firebase.auth() #initializing authentication
db=firebase.database() #initializing database
now = datetime.now() 
dt = now.strftime("%d/%m/%Y %H:%M:%S") #setting the time format

app = Flask(__name__) #intalizing flask
app.config["SECRET_KEY"] = "OCML3BRatWEUeqxcuBHLpw" #the secret key is used to encrypt the cookie

@app.route('/') #hosting the index page
def index():
    return render_template('index.html') #rendering the web page 

@app.route('/Javascript') #hosting the Javascript page
def Javascript(): #preventing the user from accessing the page without signing in
  must = "You must be logged in to access the course." #setting error message
  if "email" in session: # making sure that the user is signed in
    user = session["email"] #collecting the email from the cookie
    return render_template('Javascript.html', username = user) #rendering the web page and displaying the username
  else:
    return render_template('signin.html', m=must) #rendering the web page and displaying the error

@app.route('/Html_and_Css') #This block of code is almost identical to the previous one however it projects a diffrent web page
def Html_and_Css(): 
  must = "You must be logged in to access the course." 
  if "email" in session: 
    user = session["email"] 
    return render_template('Html_and_Css.html', username = user) 
  else:
    return render_template('signin.html', m=must) 

@app.route('/C++') #This block of code is almost identical to the previous one however it projects a diffrent web page
def C():
  must = "You must be logged in to access the course." 
  if "email" in session:
    user = session["email"] 
    return render_template('C++.html', username = user)
  else:
    return render_template('signin.html', m=must)

@app.route('/Python')  #This block of code is almost identical to the previous one however it projects a diffrent web page
def Python():
  must = "You must be logged in to access the course." 
  if "email" in session:
    user = session["email"] 
    return render_template('Python.html', username = user)
  else:
    return render_template('signin.html', m=must)

@app.route('/signup', methods=['GET', 'POST']) #hosting the signup page while allowing the "POST" and "GET" methods
def signup():
  fail = "Something went wrong" #setting error message
  success = "Sign up successful." #setting error message
  passes = "The two passwords do not match." #setting error message
  if request.method =='POST': #initiating the code in the case of submitting the data
    email = request.form['email'] #obtaining data from the web app
    password = request.form['pass'] #obtaining data from the web app
    password2 = request.form['pass2'] #obtaining data from the web app
    if len(password) < 8 : #validating the password to be at least 8 characters
      fail = "The password must be at least 8 characters." #validating the password to be at least 8 characters
      return render_template('signup.html', f=fail)
    if len(password) > 20 : #validating the password to be at least 8 characters
      fail = "The password must not be more than 20 characters." #overwriting the error message
      return render_template('signup.html', f=fail) #rendering the web page and displaying the error
    if not any(char.isdigit() for char in password): #validating the password to be at least 8 characters
      fail = "Password must have at least one number."
      return render_template('signup.html', f=fail)
    if not any(char.isupper() for char in password): #validating the password to be at least 1 uppercase letter
      fail = "Password must have at least one uppercase letter."
      return render_template('signup.html', f=fail)
    if not any(char.islower() for char in password): #validating the password to be at least 1 lowercase letter
      fail = "Password must have at least one lowercase letter."
      return render_template('signup.html', f=fail)
    if not any(char.isalpha() for char in password): #validating the password to have at least 1 characters
      fail = "Password must have at least one character."
      return render_template('signup.html', f=fail)
    if password == password2:
      try:
        n_user=auth.create_user_with_email_and_password(email,password) #creating a new email and password using the parameters that were collected from the web page
        auth.send_email_verification(n_user['idToken']) #sending a verification email to verify new users using firebase function
        return render_template('signup.html', s=success)
      except:
        return render_template('signup.html', f=fail)
    return render_template('signup.html', p = passes)  
  return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST']) #hosting the signin page while allowing the "POST" and "GET" methods
def signin():
  fail = "Please check your credentials." #setting error message
  success = "Login successful." #setting error message
  ver = "Please verify your email,before trying to sign in." #setting error message
  if request.method =='POST': #initiating the code in the case of submitting the data
    email = request.form['email'] #obtaining data from the web app
    password = request.form['pass'] #obtaining data from the web app
    try:
      auth.sign_in_with_email_and_password(email,password) #signing in with the email and password that were inputted via web page
      user_info = auth.sign_in_with_email_and_password(email,password) 
      account_info = auth.get_account_info(user_info['idToken']) #collecting info on the account
      if account_info['users'][0]['emailVerified'] == True: #if the account is verified the if function is initiated
        session["email"] = email #adding the email to the cookie
        return render_template('signin.html', s=success) 
      return render_template ('signin.html', v = ver)
    except:
      return render_template('signin.html', f=fail)
  return render_template('signin.html')

@app.route('/profile', methods=['GET', 'POST']) #hosting the profile page while allowing the "POST" and "GET" methods
def profile():
  must = "You must be logged in to access the profile page." #setting error message
  if "email" in session: #validating if the user is signed in
    user = session["email"] #getting the email from cookie
    return render_template('profile.html', username = user)
  else:
    return render_template('signin.html', m=must)

@app.route('/logout', methods=['GET', 'POST']) 
def logout():
  if request.method =='POST': #initiating the if statment if the logout button is clicked
    session.pop("email", None) #deleting the cookie
  return redirect(url_for('index'))

@app.route('/r_pass', methods=['GET', 'POST']) #hosting the reset password page while allowing the "POST" and "GET" methods
def r_pass():
  sent = "The reset password mail have been sent to the selected email." #setting error message 
  n_sent = "This email is not in our database, make sure you have the right email or sign up." #setting error message
  if request.method =='POST': #initiating the if statment if the logout button is clicked
    email = request.form['user_email'] #obtaining data from the web app
    try:
      auth.send_password_reset_email(email) #sending a password reset email to the requested user
      return render_template('r_pass.html', s = sent)
    except requests.HTTPError as e: #error handling: in case the email is not in the database
      error_json = e.args[1]
      error = json.loads(error_json)['error']['message']
      if error == "EMAIL_NOT_FOUND":
        return render_template('r_pass.html', n = n_sent)
  return render_template('r_pass.html')

@app.route('/comment', methods=['GET', 'POST']) #hosting the comment section in the Javascript page while allowing the "POST" and "GET" methods
def comment():
  empty = "The comment can't be empty." #setting error message
  if request.method =='POST':
    comment = request.form['Comment'] #obtaining data from the web app
    if len(comment) < 1: #validating against empty
      return render_template('Javascript.html', e = empty)
    elif comment.isspace(): #validating against comments with only space
      return render_template('Javascript.html', e = empty)
    else:
      email = session["email"] #obtaining the email from the cookie
      x = '@'
      p = email.rfind(x)
      user = email[0:p] #cutting a part of the email
      dt = now.strftime("%d/%m/%Y %H:%M:%S") #obtaining the current time
      data=[comment,dt,user] #putting the data in a list
      db.child("Comments").child("Javascript Comments").push(data) #sending the data in to the database
      comm = db.child("Comments").child("Javascript Comments").get() #pulling the data from the database
      get = comm.val()
      return render_template('Javascript.html', get = get.values()) #rendring the web page with all the comments
  return render_template('Javascript.html')

@app.route('/comment2', methods=['GET', 'POST']) #This block of code is almost identical to the previous one however it projects a diffrent web page
def comment2():
  empty = "The comment can't be empty." 
  if request.method =='POST':
    comment = request.form['Comment'] 
    if len(comment) < 1:
      return render_template('Html_and_Css.html', e = empty)
    elif comment.isspace():
      return render_template('Html_and_Css.html', e = empty)
    else:
      email = session["email"]
      x = '@'
      p = email.rfind(x)
      user = email[0:p]
      dt = now.strftime("%d/%m/%Y %H:%M:%S")
      data=[comment,dt,user]
      db.child("Comments").child("Html_and_Css Comments").push(data)
      comm = db.child("Comments").child("Html_and_Css Comments").get()
      get = comm.val()
      return render_template('Html_and_Css.html', get = get.values())
  return render_template('Html_and_Css.html')

@app.route('/comment3', methods=['GET', 'POST']) #This block of code is almost identical to the previous one however it projects a diffrent web page
def comment3():
  empty = "The comment can't be empty." 
  if request.method =='POST':
    comment = request.form['Comment'] 
    if len(comment) < 1:
      return render_template('C++.html', e = empty)
    elif comment.isspace():
      return render_template('C++.html', e = empty)
    else: 
      email = session["email"]
      x = '@'
      p = email.rfind(x)
      user = email[0:p]
      dt = now.strftime("%d/%m/%Y %H:%M:%S")
      data=[comment,dt,user]
      db.child("Comments").child("C++ Comments").push(data)
      comm = db.child("Comments").child("C++ Comments").get()
      get = comm.val()
      return render_template('C++.html', get = get.values())
  return render_template('C++.html')

@app.route('/comment4', methods=['GET', 'POST']) #This block of code is almost identical to the previous one however it projects a diffrent web page
def comment4():
  empty = "The comment can't be empty." 
  if request.method =='POST':
    comment = request.form['Comment'] 
    if len(comment) < 1: 
      return render_template('Python.html', e = empty)
    elif comment.isspace():
      return render_template('Python.html', e = empty)
    else: 
      email = session["email"]
      x = '@'
      p = email.rfind(x)
      user = email[0:p]
      dt = now.strftime("%d/%m/%Y %H:%M:%S")
      data=[comment,dt,user]
      db.child("Comments").child("Python Comments").push(data)
      comm = db.child("Comments").child("Python Comments").get()
      get = comm.val()
      return render_template('Python.html', get = get.values())
  return render_template('Python.html')

@app.route('/show', methods=['GET', 'POST']) #hosting the show function in the Javascript page while allowing the "POST" and "GET" methods
def show():
  if request.method =='POST':
    comm = db.child("Comments").child("Javascript Comments").get() #pulling all the comments from the database
    get = comm.val()
    return render_template('Javascript.html', get = get.values()) #rendring the web page with all the comments
  return render_template('Javascript.html')

@app.route('/show2', methods=['GET', 'POST'])  #This block of code is almost identical to the previous one however it projects a diffrent web page
def show2():
  if request.method =='POST':
    comm = db.child("Comments").child("Html_and_Css Comments").get()
    get = comm.val()
    return render_template('Html_and_Css.html', get = get.values())
  return render_template('Html_and_Css.html')

@app.route('/show3', methods=['GET', 'POST'])  #This block of code is almost identical to the previous one however it projects a diffrent web page
def show3():
  if request.method =='POST':
    comm = db.child("Comments").child("C++ Comments").get()
    get = comm.val()
    return render_template('C++.html', get = get.values())
  return render_template('C++.html')

@app.route('/show4', methods=['GET', 'POST'])  #This block of code is almost identical to the previous one however it projects a diffrent web page
def show4():
  if request.method =='POST':
    comm = db.child("Comments").child("Python Comments").get()
    get = comm.val()
    return render_template('Python.html', get = get.values())
  return render_template('Python.html')

if __name__ == '__main__': 
  app.run() 