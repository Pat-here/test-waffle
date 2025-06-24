import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, UTC
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'twoj-super-sekretny-klucz-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gofry_biznes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modele bazy danych

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))

class Kategorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(100), nullable=False)
    kolor = db.Column(db.String(7), default='#007bff')

class Dodatki(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(100), nullable=False)
    kategoria_id = db.Column(db.Integer, db.ForeignKey('kategorie.id'))
    koszt_opakowania = db.Column(db.Float, nullable=False)
    jednostka = db.Column(db.String(20), default='g')
    porcja = db.Column(db.Float, nullable=False)
    koszt_porcyjny = db.Column(db.Float, nullable=False)
    cena_sprzedazy = db.Column(db.Float, nullable=False)
    marza = db.Column(db.Float, default=0)
    kategoria = db.relationship('Kategorie', backref=db.backref('dodatki', lazy=True))

class KosztyWykonania(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(100), nullable=False)
    koszt_mieszanki_kg = db.Column(db.Float, default=12.0)
    zuzycie_mieszanki_g = db.Column(db.Float, default=80.0)
    koszt_energii = db.Column(db.Float, default=0.15)
    koszt_gazu = db.Column(db.Float, default=0.05)
    koszt_pracy = db.Column(db.Float, default=1.50)
    koszt_calkowity = db.Column(db.Float, default=0)

class Gofry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(100), nullable=False)
    cena_sprzedazy = db.Column(db.Float, nullable=False)
    koszt_wykonania_id = db.Column(db.Integer, db.ForeignKey('koszty_wykonania.id'))
    koszt_calkowity = db.Column(db.Float, default=0)
    marza = db.Column(db.Float, default=0)
    koszt_wykonania = db.relationship('KosztyWykonania', backref=db.backref('gofry', lazy=True))

class Kompozycje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(100), nullable=False)
    gofr_id = db.Column(db.Integer, db.ForeignKey('gofry.id'))
    cena_sprzedazy = db.Column(db.Float, nullable=False)
    koszt_surowcow = db.Column(db.Float, default=0)
    marza = db.Column(db.Float, default=0)
    gofr = db.relationship('Gofry', backref=db.backref('kompozycje', lazy=True))

class KompozycjeDodatki(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kompozycja_id = db.Column(db.Integer, db.ForeignKey('kompozycje.id'))
    dodatek_id = db.Column(db.Integer, db.ForeignKey('dodatki.id'))
    ilosc_porcji = db.Column(db.Float, default=1.0)

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    priority = db.Column(db.String(10), default='medium') # low, medium, high

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='pending') # pending, ordered, delivered
    order_date = db.Column(db.Date, default=lambda: datetime.now(UTC).date())
    delivery_date = db.Column(db.Date)
    total_cost = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)

class OrderItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    item_name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), default='szt')
    unit_price = db.Column(db.Float, default=0)
    total_price = db.Column(db.Float, default=0)
    order = db.relationship('Orders', backref=db.backref('items', lazy=True))

class WorkHours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(100), nullable=False)
    work_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    break_minutes = db.Column(db.Integer, default=0)
    hourly_rate = db.Column(db.Float, default=20.0)
    total_hours = db.Column(db.Float, default=0)
    total_pay = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)

class DailyReports(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_date = db.Column(db.Date, nullable=False, unique=True)
    revenue = db.Column(db.Float, default=0)
    costs = db.Column(db.Float, default=0)
    profit = db.Column(db.Float, default=0)
    gofry_sold = db.Column(db.Integer, default=0)
    weather = db.Column(db.String(50))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))

# Funkcje pomocnicze

def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def calculate_marza(cena, koszt):
    if cena > 0:
        return round(((cena - koszt) / cena) * 100, 1)
    return 0

# Strona logowania

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Zalogowano pomyślnie!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Nieprawidłowy login lub hasło!', 'error')
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Wylogowano pomyślnie!', 'success')
    return redirect(url_for('login'))

# Dashboard główny

@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    stats = {
        'kategorie_count': Kategorie.query.count(),
        'dodatki_count': Dodatki.query.count(),
        'gofry_count': Gofry.query.count(),
        'kompozycje_count': Kompozycje.query.count(),
        'notes_count': Notes.query.count(),
        'orders_pending': Orders.query.filter_by(status='pending').count(),
        'today_report': DailyReports.query.filter_by(report_date=datetime.now(UTC).date()).first()
    }
    # Oblicz średnią marżę
    dodatki = Dodatki.query.all()
    if dodatki:
        stats['avg_marza'] = round(sum([d.marza for d in dodatki]) / len(dodatki), 1)
    else:
        stats['avg_marza'] = 0
    return render_template('dashboard/index.html', stats=stats)

# CRUD dla kategorii

@app.route('/api/kategorie', methods=['GET', 'POST'])
@login_required
def api_kategorie():
    if request.method == 'POST':
        data = request.json
        kategoria = Kategorie(nazwa=data['nazwa'], kolor=data.get('kolor', '#007bff'))
        db.session.add(kategoria)
        db.session.commit()
        return jsonify({'success': True, 'id': kategoria.id})
    kategorie = Kategorie.query.all()
    return jsonify([{
        'id': k.id,
        'nazwa': k.nazwa,
        'kolor': k.kolor,
        'dodatki_count': len(k.dodatki)
    } for k in kategorie])

@app.route('/api/kategorie/<int:id>', methods=['PUT', 'DELETE'])
@login_required
def api_kategoria(id):
    kategoria = Kategorie.query.get_or_404(id)
    if request.method == 'PUT':
        data = request.json
        kategoria.nazwa = data['nazwa']
        kategoria.kolor = data.get('kolor', kategoria.kolor)
        db.session.commit()
        return jsonify({'success': True})
    elif request.method == 'DELETE':
        db.session.delete(kategoria)
        db.session.commit()
        return jsonify({'success': True})

# CRUD dla dodatków

@app.route('/api/dodatki', methods=['GET', 'POST'])
@login_required
def api_dodatki():
    if request.method == 'POST':
        data = request.json
        koszt_porcyjny = (data['koszt_opakowania'] / 1000) * data['porcja'] if data['jednostka'] == 'g' else data['koszt_opakowania'] * data['porcja']
        marza = calculate_marza(data['cena_sprzedazy'], koszt_porcyjny)
        dodatek = Dodatki(
            nazwa=data['nazwa'],
            kategoria_id=data['kategoria_id'],
            koszt_opakowania=data['koszt_opakowania'],
            jednostka=data['jednostka'],
            porcja=data['porcja'],
            koszt_porcyjny=koszt_porcyjny,
            cena_sprzedazy=data['cena_sprzedazy'],
            marza=marza
        )
        db.session.add(dodatek)
        db.session.commit()
        return jsonify({'success': True, 'id': dodatek.id})
    dodatki = db.session.query(Dodatki, Kategorie).join(Kategorie).all()
    return jsonify([{
        'id': d.Dodatki.id,
        'nazwa': d.Dodatki.nazwa,
        'kategoria': d.Kategorie.nazwa,
        'kategoria_kolor': d.Kategorie.kolor,
        'koszt_opakowania': d.Dodatki.koszt_opakowania,
        'jednostka': d.Dodatki.jednostka,
        'porcja': d.Dodatki.porcja,
        'koszt_porcyjny': round(d.Dodatki.koszt_porcyjny, 2),
        'cena_sprzedazy': d.Dodatki.cena_sprzedazy,
        'marza': d.Dodatki.marza
    } for d in dodatki])

@app.route('/api/dodatki/<int:id>', methods=['PUT', 'DELETE'])
@login_required
def api_dodatek(id):
    dodatek = Dodatki.query.get_or_404(id)
    if request.method == 'PUT':
        data = request.json
        koszt_porcyjny = (data['koszt_opakowania'] / 1000) * data['porcja'] if data['jednostka'] == 'g' else data['koszt_opakowania'] * data['porcja']
        marza = calculate_marza(data['cena_sprzedazy'], koszt_porcyjny)
        dodatek.nazwa = data['nazwa']
        dodatek.kategoria_id = data['kategoria_id']
        dodatek.koszt_opakowania = data['koszt_opakowania']
        dodatek.jednostka = data['jednostka']
        dodatek.porcja = data['porcja']
        dodatek.koszt_porcyjny = koszt_porcyjny
        dodatek.cena_sprzedazy = data['cena_sprzedazy']
        dodatek.marza = marza
        db.session.commit()
        return jsonify({'success': True})
    elif request.method == 'DELETE':
        db.session.delete(dodatek)
        db.session.commit()
        return jsonify({'success': True})

# CRUD dla notatek

@app.route('/notes')
@login_required
def notes():
    return render_template('dashboard/notes.html')

@app.route('/api/notes', methods=['GET', 'POST'])
@login_required
def api_notes():
    if request.method == 'POST':
        data = request.json
        note = Notes(
            title=data['title'],
            content=data['content'],
            priority=data.get('priority', 'medium')
        )
        db.session.add(note)
        db.session.commit()
        return jsonify({'success': True, 'id': note.id})
    notes = Notes.query.order_by(Notes.created_at.desc()).all()
    return jsonify([{
        'id': n.id,
        'title': n.title,
        'content': n.content,
        'priority': n.priority,
        'created_at': n.created_at.strftime('%Y-%m-%d %H:%M'),
        'updated_at': n.updated_at.strftime('%Y-%m-%d %H:%M')
    } for n in notes])

@app.route('/api/notes/<int:id>', methods=['PUT', 'DELETE'])
@login_required
def api_note(id):
    note = Notes.query.get_or_404(id)
    if request.method == 'PUT':
        data = request.json
        note.title = data['title']
        note.content = data['content']
        note.priority = data.get('priority', note.priority)
        note.updated_at = datetime.now(UTC)
        db.session.commit()
        return jsonify({'success': True})
    elif request.method == 'DELETE':
        db.session.delete(note)
        db.session.commit()
        return jsonify({'success': True})

# Lista zamówień

@app.route('/orders')
@login_required
def orders():
    return render_template('dashboard/orders.html')

@app.route('/api/orders', methods=['GET', 'POST'])
@login_required
def api_orders():
    if request.method == 'POST':
        data = request.json
        order = Orders(
            supplier=data['supplier'],
            order_date=datetime.strptime(data['order_date'], '%Y-%m-%d').date(),
            delivery_date=datetime.strptime(data['delivery_date'], '%Y-%m-%d').date() if data.get('delivery_date') else None,
            notes=data.get('notes', '')
        )
        db.session.add(order)
        db.session.commit()
        total_cost = 0
        for item in data.get('items', []):
            order_item = OrderItems(
                order_id=order.id,
                item_name=item['item_name'],
                quantity=item['quantity'],
                unit=item['unit'],
                unit_price=item['unit_price'],
                total_price=item['quantity'] * item['unit_price']
            )
            total_cost += order_item.total_price
            db.session.add(order_item)
        order.total_cost = total_cost
        db.session.commit()
        return jsonify({'success': True, 'id': order.id})
    orders = Orders.query.order_by(Orders.order_date.desc()).all()
    return jsonify([{
        'id': o.id,
        'supplier': o.supplier,
        'status': o.status,
        'order_date': o.order_date.strftime('%Y-%m-%d'),
        'delivery_date': o.delivery_date.strftime('%Y-%m-%d') if o.delivery_date else None,
        'total_cost': o.total_cost,
        'items_count': len(o.items),
        'notes': o.notes
    } for o in orders])

# Czas pracy

@app.route('/work-hours')
@login_required
def work_hours():
    return render_template('dashboard/work_hours.html')

@app.route('/api/work-hours', methods=['GET', 'POST'])
@login_required
def api_work_hours():
    if request.method == 'POST':
        data = request.json
        start_time = datetime.strptime(data['start_time'], '%H:%M').time()
        end_time = datetime.strptime(data['end_time'], '%H:%M').time()
        start_datetime = datetime.combine(datetime.today(), start_time)
        end_datetime = datetime.combine(datetime.today(), end_time)
        if end_datetime < start_datetime:
            end_datetime += timedelta(days=1)
        total_minutes = (end_datetime - start_datetime).total_seconds() / 60
        total_minutes -= data.get('break_minutes', 0)
        total_hours = total_minutes / 60
        total_pay = total_hours * data['hourly_rate']
        work_hour = WorkHours(
            employee_name=data['employee_name'],
            work_date=datetime.strptime(data['work_date'], '%Y-%m-%d').date(),
            start_time=start_time,
            end_time=end_time,
            break_minutes=data.get('break_minutes', 0),
            hourly_rate=data['hourly_rate'],
            total_hours=round(total_hours, 2),
            total_pay=round(total_pay, 2),
            notes=data.get('notes', '')
        )
        db.session.add(work_hour)
        db.session.commit()
        return jsonify({'success': True, 'id': work_hour.id})
    work_hours = WorkHours.query.order_by(WorkHours.work_date.desc()).all()
    return jsonify([{
        'id': w.id,
        'employee_name': w.employee_name,
        'work_date': w.work_date.strftime('%Y-%m-%d'),
        'start_time': w.start_time.strftime('%H:%M'),
        'end_time': w.end_time.strftime('%H:%M'),
        'break_minutes': w.break_minutes,
        'hourly_rate': w.hourly_rate,
        'total_hours': w.total_hours,
        'total_pay': w.total_pay,
        'notes': w.notes
    } for w in work_hours])

# Raporty dzienne

@app.route('/reports')
@login_required
def reports():
    return render_template('dashboard/reports.html')

@app.route('/api/reports', methods=['GET', 'POST'])
@login_required
def api_reports():
    if request.method == 'POST':
        data = request.json
        profit = data['revenue'] - data['costs']
        existing_report = DailyReports.query.filter_by(
            report_date=datetime.strptime(data['report_date'], '%Y-%m-%d').date()
        ).first()
        if existing_report:
            existing_report.revenue = data['revenue']
            existing_report.costs = data['costs']
            existing_report.profit = profit
            existing_report.gofry_sold = data['gofry_sold']
            existing_report.weather = data.get('weather', '')
            existing_report.notes = data.get('notes', '')
        else:
            report = DailyReports(
                report_date=datetime.strptime(data['report_date'], '%Y-%m-%d').date(),
                revenue=data['revenue'],
                costs=data['costs'],
                profit=profit,
                gofry_sold=data['gofry_sold'],
                weather=data.get('weather', ''),
                notes=data.get('notes', '')
            )
            db.session.add(report)
        db.session.commit()
        return jsonify({'success': True})
    reports = DailyReports.query.order_by(DailyReports.report_date.desc()).limit(30).all()
    return jsonify([{
        'id': r.id,
        'report_date': r.report_date.strftime('%Y-%m-%d'),
        'revenue': r.revenue,
        'costs': r.costs,
        'profit': r.profit,
        'gofry_sold': r.gofry_sold,
        'weather': r.weather,
        'notes': r.notes
    } for r in reports])

@app.route('/api/monthly-summary/<int:year>/<int:month>')
@login_required
def api_monthly_summary(year, month):
    from sqlalchemy import extract
    reports = DailyReports.query.filter(
        extract('year', DailyReports.report_date) == year,
        extract('month', DailyReports.report_date) == month
    ).all()
    if not reports:
        return jsonify({
            'total_revenue': 0,
            'total_costs': 0,
            'total_profit': 0,
            'total_gofry': 0,
            'working_days': 0,
            'avg_daily_revenue': 0
        })
    total_revenue = sum(r.revenue for r in reports)
    total_costs = sum(r.costs for r in reports)
    total_profit = sum(r.profit for r in reports)
    total_gofry = sum(r.gofry_sold for r in reports)
    working_days = len(reports)
    avg_daily_revenue = total_revenue / working_days if working_days > 0 else 0
    return jsonify({
        'total_revenue': total_revenue,
        'total_costs': total_costs,
        'total_profit': total_profit,
        'total_gofry': total_gofry,
        'working_days': working_days,
        'avg_daily_revenue': round(avg_daily_revenue, 2)
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                email='admin@gofry.pl',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Utworzono konto administratora: admin / admin123")
    app.run(host='0.0.0.0', port=5000, debug=True)
