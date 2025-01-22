import os

from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import Session
from flask_wtf import FlaskForm
from .database import SessionLocal  # Import SessionLocal

from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import Session
from . import db
from app.models.user import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo
from . import db
from flask import Blueprint, redirect, render_template, request, jsonify, url_for, session
from app.controllers.es_pull_scroll import es_search
from .controllers.sparql_utils import execute_sparql_query , save_query
from wtforms.validators import DataRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField
from app.database import engine, get_db, Base
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return redirect(url_for('main.login'))


@main.route('/login', methods=['GET', 'POST'])
def login():
    class LoginForm(FlaskForm):
        username = StringField('Username', validators=[DataRequired()])
        password = PasswordField('Password', validators=[DataRequired()])

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check if the user exists and verify the password
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # Login successful, set session
            session['user'] = user.username
            session.permanent = True  # Make session permanent
            flash("Login successful", "success")
            return redirect(url_for('main.dashboard'))

        flash("Invalid username or password", "danger")
        return redirect(url_for('main.login'))

    return render_template('login.html', form=form)


Base.metadata.create_all(bind=engine)
@main.route('/logout')
def logout():
    session.pop('user', None)  # Remove user from session
    flash("You have been logged out.", "info")
    return redirect(url_for('main.login'))


@main.route('/users', methods=['GET'])
def get_users():
    with Session(engine) as session:
        users = session.query(User).all()
        return jsonify([{'id': u.id, 'username': u.username} for u in users])


    

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    class SignupForm(FlaskForm):
        username = StringField('username', validators=[DataRequired(), Length(min=4, max=20)])
        password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=20)])
        
    form = SignupForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check if the username already exists
        with SessionLocal() as session:
            if session.query(User).filter_by(username=username).first():
                flash("Username already exists.", "danger")
                return redirect(url_for('main.signup'))

            # Hash the password and create the new user
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            session.add(new_user)
            session.commit()

        flash("Account created successfully. Please login.", "success")
        return redirect(url_for('main.login'))

    return render_template('signup.html', form=form)


@main.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('main.login'))
    return render_template('index.html')


@main.route('/query', methods=['POST'])
def query():
    query = request.form.get('sparql_query')
    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400
    save_query(query)
    results = execute_sparql_query(query)
    if "error" in results:
        return jsonify({"error": results["error"]}), 400

    return jsonify({"results": results})
@main.route('/previous-queries', methods=['GET'])
def get_previous_queries():
    queries = []
    file_path = os.path.join(os.path.dirname(__file__), 'static', 'sparql_queries.txt')
    with open(file_path, 'r') as f:
        lines = f.readlines()
        start_collecting = False
        for line in lines:
            if '#PERSONALIZED USER Query' in line:
                start_collecting = True
                continue
            if start_collecting and line.strip() and not line.strip().startswith('#'):
                queries.append(line.strip())
    return jsonify(queries)


# Add newline here
@main.route('/test', methods=['GET'])
def test_pipeline():
    """
    Test the pipeline: query Elasticsearch and use the result to query DBpedia.
    """
    try:
        # Step 1: Query Elasticsearch for a search term
        search_term = request.args.get('query', default='Albert Einstein')
        es_results = es_search(search_term)

        if not es_results:
            return jsonify({"message": "No results found in Elasticsearch."}), 404

        # Step 2: Use SPARQL to query DBpedia with the first Elasticsearch result
        sparql_query = es_results[0].get("query")
        dbpedia_results = execute_sparql_query(sparql_query)

        return jsonify({
            "elasticsearch_results": es_results,
            "dbpedia_results": dbpedia_results
        })

    except Exception as e:
        return jsonify({"error": f"Pipeline testing failed: {str(e)}"}), 500

@main.route('/test-db', methods=['GET'])
def test_db():
    try:
        user = User.query.first()
        if user:
            return jsonify({"message": f"First user: {user.username}"})
        else:
            return jsonify({"message": "No users found in the database."})
    except Exception as e:
        return jsonify({"error": f"Database connection failed: {str(e)}"}), 500
