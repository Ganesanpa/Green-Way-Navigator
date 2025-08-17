from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from routes import get_route_data
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'API_Key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eco_routes.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    routes = db.relationship('Route', backref='user', lazy=True)

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(150))
    destination = db.Column(db.String(150))
    mode = db.Column(db.String(50))
    distance = db.Column(db.Float)
    duration = db.Column(db.Float)
    emission = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class RouteHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    origin = db.Column(db.String(200))
    destination = db.Column(db.String(200))
    distance = db.Column(db.Float)
    emission = db.Column(db.Float)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Trying login: {username=} {password=}")
        user = User.query.filter_by(username=username).first()
        print(f"Found user: {user}")
        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="Username already exists")

        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        mode = request.form['mode']

        route_info = get_route_data(start, end, mode)

        if route_info['map_file'] is None:
            flash("Could not find location. Please try different inputs.")
            return redirect(url_for('index'))

        new_route = Route(
            start=start,
            end=end,
            mode=mode,
            distance=route_info['distance'],
            duration=route_info['duration'],
            emission=route_info['emission'],
            user_id=current_user.id
        )
        db.session.add(new_route)
        db.session.commit()

        return render_template('result.html', info=route_info, map_file=route_info['map_file'])

    return render_template('index.html')



@app.route('/eco_route', methods=['GET', 'POST'])
def eco_route():
    if request.method == 'POST':
        origin = request.form.get('origin')
        destination = request.form.get('destination')
        mode = request.form.get('mode')

        if not origin or not destination or not mode:
            flash("Missing input fields.")
            return redirect(url_for('eco_route'))

        route_data = get_route_data(origin, destination, mode)
        distance = route_data['distance']
        emission = route_data['emission']

        if 'username' in session:
            new_route = RouteHistory(
                username=session['username'],
                origin=origin,
                destination=destination,
                distance=distance,
                emission=emission
            )
            db.session.add(new_route)
            db.session.commit()

        return render_template('result.html', route=route_data)
    
    return render_template('eco_route.html')

@app.route('/my_routes')
def my_routes():
    if 'username' in session:
        routes = RouteHistory.query.filter_by(username=session['username']).all()
        return render_template('my_routes.html', routes=routes)
    return redirect(url_for('login'))



@app.route('/protected')
@login_required
def protected():
    return f"Hello, {current_user.username}! You are logged in."
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        origin = request.form['origin']
        destination = request.form['destination']
        mode = request.form['mode']

        try:
            route_data = get_route_data(origin,destination, mode)
            return render_template('dashboard.html',
                                   map_file=route_data['map_file'],
                                   distance=route_data['distance'],
                                   duration=route_data['duration'],
                                   emission=route_data['emission'])
        except Exception as e:
            print("Error calculating route:", e)
            flash("Failed to calculate route. Please try again.")
            return redirect(url_for('dashboard'))

    return render_template('dashboard.html')  

@app.route('/history')
def history():
    if 'username' not in session:
        return redirect('/login')
    routes = RouteHistory.query.filter_by(username=session['username']).all()
    return render_template('history.html', routes=routes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
