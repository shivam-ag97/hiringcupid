import os
from flask import Flask, jsonify, request, render_template, g, url_for, session, redirect, send_file, flash, abort, \
    jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)
app.secret_key = 'qweasb@#12344'

client = MongoClient('mongodb+srv://shivam:shivam@cluster0-07rfo.mongodb.net/test?retryWrites=true&w=majority')
db = client.get_database('HiringCupid')


@app.route("/index")
def index():
	return render_template("home_page.html")

@app.route('/register_as_interviewer')
def register_as_interviewer():
	return render_template("register_as_interviewer.html")


@app.route("/create_interviewee_profile" , methods=["POST","GET"])
def create_interviewee_profile():
	if request.method=="POST":
		interviewers=db.interviewers
		interviewers.insert({"iid":request.form['iid'], "pw":request.form['pw'],"fname": request.form['fname'],"lname":request.form['lname'],
						"cur_comp":request.form['cur_company'] , "exp":request.form['exp'],
						"past" : request.form.getlist('past_comp')})
		return "profile successfully created"


@app.route("/login_interviewer",methods=["POST"])
def login_interviewer():
	if request.method == "POST":
		interviewers=db.interviewers
		# print(request.form['iid'])
		login_interviewer=interviewers.find_one({"iid":request.form['iid']})
		if login_interviewer:
			pw = request.form['pw']
			if pw == login_interviewer['pw']:
				return render_template("interviewer_page.html")
			return "Invalid userID or password"
		return "Invalid Credentials"
	return render_template('home_page.html')



@app.route("/register_as_candidate")
def register_as_candidate():
	return render_template("register_as_candidate.html")

@app.route("/create_candidate_profile" , methods=["POST","GET"])
def create_candidate_profile():
	if request.method=="POST":
		candidates=db.candidate
		candidates.insert({"cid":request.form['cid'], "pw":request.form['pw'],"fname": request.form['fname'],"lname":request.form['lname'],
						"dc":request.form['dc'] , "exp":request.form['exp'],
						"past" : request.form.getlist('past_comp')})
		return "profile successfully created"


@app.route("/login_candidate",methods=["POST"])
def login_candidate():
	if request.method == "POST":
		candidates=db.candidate
		login_candidate=candidates.find_one({"cid":request.form['cid']})
		if login_candidate:
			pw = request.form['pw']
			if pw == login_candidate['pw']:
				return render_template("candidate_page.html")
			return "Invalid userID or password"
		return "Invalid Credentials"
	return render_template('home_page.html')





