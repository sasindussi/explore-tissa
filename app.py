from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'explore_tissa_secret_key_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tissa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Attraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    opening_hours = db.Column(db.String(100), nullable=False)
    travel_tips = db.Column(db.Text, nullable=True)
    distance_km = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    best_time = db.Column(db.String(100), nullable=True)
    entry_fee = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), nullable=True)
    warning = db.Column(db.Text, nullable=True)

class SavedPlace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    place_name = db.Column(db.String(150), nullable=False)

def init_db():
    with app.app_context():
        db.create_all()
        # Create default admin if not exists
        if Admin.query.filter_by(username='admin').first() is None:
            admin = Admin(username='admin', password='password123')
            db.session.add(admin)
            db.session.commit()

        if Attraction.query.count() == 0:
            attractions_data = [
                Attraction(
                    name="Tissamaharama Raja Maha Viharaya",
                    category="Religious",
                    description="An ancient Buddhist temple featuring a massive historical stupa.",
                    opening_hours="5:00 AM - 9:00 PM",
                    travel_tips="Remove shoes and hats before entering shrine areas. Maintain silence.",
                    distance_km=1.0,
                    latitude=6.2831,
                    longitude=81.2890,
                    image_url="https://pfxpcemoftcdwrfiipvw.supabase.co/storage/v1/object/public/explore_tissa/tissa_seya.webp",
                    best_time="Early Morning (6:00 AM - 8:00 AM)",
                    entry_fee="Free Entry",
                    status="Open",
                    warning=None
                ),
                Attraction(
                    name="Tissa Wewa",
                    category="Nature",
                    description="A scenic, ancient reservoir built in the 3rd century BC, perfect for evening walks.",
                    opening_hours="Open 24 Hours",
                    travel_tips="Watch out for wild crocodiles and stray dogs near the bund.",
                    distance_km=1.5,
                    latitude=6.2890,
                    longitude=81.2820,
                    image_url="https://pfxpcemoftcdwrfiipvw.supabase.co/storage/v1/object/public/explore_tissa/tissa_lake.webp",
                    best_time="Evening (4:30 PM - 6:30 PM)",
                    entry_fee="Free Entry",
                    status="Open",
                    warning="Watch out for wild crocodiles near the bund."
                ),
                Attraction(
                    name="Yala National Park (Palatupana)",
                    category="Nature",
                    description="Famous wildlife sanctuary known for leopards, elephants, and diverse bird species.",
                    opening_hours="6:00 AM - 6:00 PM",
                    travel_tips="Safari booking required in advance. Wear comfortable outdoor clothing.",
                    distance_km=16.0,
                    latitude=6.3728,
                    longitude=81.5467,
                    image_url="https://pfxpcemoftcdwrfiipvw.supabase.co/storage/v1/object/public/explore_tissa/yala_park.webp",
                    best_time="Early Morning (6:00 AM - 9:00 AM)",
                    entry_fee="Safari Ticket Applicable",
                    status="Open",
                    warning=None
                ),
                Attraction(
                    name="Kataragama Kiri Vehera",
                    category="Religious",
                    description="A sacred ancient stupa steeped in history and religious significance.",
                    opening_hours="5:00 AM - 10:00 PM",
                    travel_tips="Dress respectfully covering shoulders and knees. Remove footwear.",
                    distance_km=18.5,
                    latitude=6.4150,
                    longitude=81.3340,
                    image_url="https://pfxpcemoftcdwrfiipvw.supabase.co/storage/v1/object/public/explore_tissa/kataragama.webp",
                    best_time="Evening (5:00 PM - 7:00 PM)",
                    entry_fee="Free Entry",
                    status="Open",
                    warning=None
                ),
                Attraction(
                    name="Yatala Vehera",
                    category="Historical",
                    description="An ancient dagoba surrounded by a wall of sculpted elephant heads.",
                    opening_hours="6:00 AM - 8:00 PM",
                    travel_tips="Great location for sunset photography. Respect local customs.",
                    distance_km=3.0,
                    latitude=6.2710,
                    longitude=81.2940,
                    image_url="https://pfxpcemoftcdwrfiipvw.supabase.co/storage/v1/object/public/explore_tissa/yatala_seya.webp",
                    best_time="Late Afternoon (4:00 PM - 6:00 PM)",
                    entry_fee="Free Entry",
                    status="Open",
                    warning=None
                ),
                Attraction(
                    name="Sandagiri Stupa",
                    category="Historical",
                    description="An ancient archaeological site and stupa in Tissamaharama.",
                    opening_hours="6:00 AM - 7:00 PM",
                    travel_tips="Wear comfortable walking shoes for the sandy grounds.",
                    distance_km=2.5,
                    latitude=6.2800,
                    longitude=81.2850,
                    image_url="https://pfxpcemoftcdwrfiipvw.supabase.co/storage/v1/object/public/explore_tissa/sandagiri_seya.webp",
                    best_time="Morning",
                    entry_fee="Free Entry",
                    status="Open",
                    warning=None
                ),
                Attraction(
                    name="Debarawewa Menik Viharaya",
                    category="Religious",
                    description="A peaceful temple located close to the Debarawewa wetland.",
                    opening_hours="6:00 AM - 8:00 PM",
                    travel_tips="Quiet environment ideal for meditation and photography.",
                    distance_km=4.0,
                    latitude=6.2950,
                    longitude=81.2750,
                    image_url="https://pfxpcemoftcdwrfiipvw.supabase.co/storage/v1/object/public/explore_tissa/menik_temple.webp",
                    best_time="Morning",
                    entry_fee="Free Entry",
                    status="Open",
                    warning=None
                ),
                Attraction(
                    name="Wirawila Bird Sanctuary",
                    category="Nature",
                    description="A haven for local and migratory bird species around the Wirawila tank.",
                    opening_hours="6:00 AM - 6:00 PM",
                    travel_tips="Bring binoculars and a telephoto lens for bird watching.",
                    distance_km=10.0,
                    latitude=6.2400,
                    longitude=81.2500,
                    image_url="https://pfxpcemoftcdwrfiipvw.supabase.co/storage/v1/object/public/explore_tissa/wirawila_bird.webp",
                    best_time="Early Morning",
                    entry_fee="Nominal Gate Fee",
                    status="Open",
                    warning=None
                ),
                Attraction(
                    name="Kirinda Viharaya",
                    category="Religious",
                    description="Historic temple perched on a rocky cliff overlooking the Indian Ocean.",
                    opening_hours="6:00 AM - 7:00 PM",
                    travel_tips="Very windy at the top. Great panoramic sea views.",
                    distance_km=12.0,
                    latitude=6.2080,
                    longitude=81.3320,
                    image_url="https://pfxpcemoftcdwrfiipvw.supabase.co/storage/v1/object/public/explore_tissa/kirinda_temple.webp",
                    best_time="Sunset",
                    entry_fee="Free Entry",
                    status="Open",
                    warning="Be careful near cliff edges."
                ),
                Attraction(
                    name="Refresh Restaurant",
                    category="Restaurant",
                    description="Popular local spot serving authentic Sri Lankan rice and curry and refreshments.",
                    opening_hours="7:00 AM - 10:00 PM",
                    travel_tips="Try their traditional clay pot rice and fresh fruit juices.",
                    distance_km=1.2,
                    latitude=6.2850,
                    longitude=81.2880,
                    image_url="https://pfxpcemoftcdwrfiipvw.supabase.co/storage/v1/object/public/explore_tissa/refresh_resturant.webp",
                    best_time="Lunch Time",
                    entry_fee="Free Entry",
                    status="Open",
                    warning=None
                )
            ]
            db.session.bulk_save_objects(attractions_data)
            db.session.commit()

# Routes
@app.route('/')
def index():
    attractions = Attraction.query.all()
    return render_template('index.html', attractions=attractions)

@app.route('/attractions')
def attractions():
    selected_category = request.args.get('category')
    if selected_category:
        attractions = Attraction.query.filter_by(category=selected_category).all()
    else:
        attractions = Attraction.query.all()
    categories = [c[0] for c in db.session.query(Attraction.category).distinct().all()]
    return render_template('attractions.html', attractions=attractions, categories=categories, selected_category=selected_category)

@app.route('/attraction/<int:id>')
def attraction_detail(id):
    attraction = Attraction.query.get_or_404(id)
    return render_template('detail.html', attraction=attraction)

@app.route('/planner')
def planner():
    attractions = Attraction.query.all()
    return render_template('planner.html', attractions=attractions)

@app.route('/save-itinerary', methods=['POST'])
def save_itinerary():
    if not session.get('user_logged_in'):
        return {'status': 'unauthorized'}, 401
    
    username = session.get('username')
    places = request.form.getlist('places')
    
    SavedPlace.query.filter_by(username=username).delete()
    for p_name in places:
        new_save = SavedPlace(username=username, place_name=p_name)
        db.session.add(new_save)
        
    db.session.commit()
    return {'status': 'success'}

@app.route('/my-itineraries')
def my_itineraries():
    if not session.get('user_logged_in'):
        return redirect(url_for('user_login'))
    username = session.get('username')
    saved_places = SavedPlace.query.filter_by(username=username).all()
    return render_template('my_itineraries.html', saved_places=saved_places)

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_logged_in'] = True
            session['username'] = user.username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('planner'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('user_login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'danger')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('user_login'))
    return render_template('register.html')

@app.route('/logout')
def user_logout():
    session.pop('user_logged_in', None)
    session.pop('username', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username, password=password).first()
        if admin:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials', 'danger')
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    attractions = Attraction.query.all()
    users = User.query.all()
    saved_places = SavedPlace.query.all()
    return render_template('admin_dashboard.html', attractions=attractions, users=users, saved_places=saved_places)

@app.route('/admin/add', methods=['POST'])
def admin_add():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        new_attraction = Attraction(
            name=request.form['name'],
            category=request.form['category'],
            description=request.form['description'],
            opening_hours=request.form['opening_hours'],
            travel_tips=request.form['travel_tips'],
            distance_km=float(request.form['distance_km']),
            latitude=float(request.form['latitude']),
            longitude=float(request.form['longitude']),
            image_url=request.form['image_url'],
            best_time=request.form['best_time'],
            entry_fee=request.form['entry_fee'],
            status=request.form['status'],
            warning=request.form.get('warning')
        )
        db.session.add(new_attraction)
        db.session.commit()
        flash('Attraction added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
def admin_edit(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    attraction = Attraction.query.get_or_404(id)
    if request.method == 'POST':
        attraction.name = request.form['name']
        attraction.category = request.form['category']
        attraction.description = request.form['description']
        attraction.opening_hours = request.form['opening_hours']
        attraction.travel_tips = request.form['travel_tips']
        attraction.distance_km = float(request.form['distance_km'])
        attraction.latitude = float(request.form['latitude'])
        attraction.longitude = float(request.form['longitude'])
        attraction.image_url = request.form['image_url']
        attraction.best_time = request.form['best_time']
        attraction.entry_fee = request.form['entry_fee']
        attraction.status = request.form['status']
        attraction.warning = request.form.get('warning')
        db.session.commit()
        flash('Attraction updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_edit.html', attraction=attraction)

@app.route('/admin/delete/<int:id>')
def admin_delete(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    attraction = Attraction.query.get_or_404(id)
    db.session.delete(attraction)
    db.session.commit()
    flash('Attraction deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)