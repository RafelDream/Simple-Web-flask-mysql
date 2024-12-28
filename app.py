# app.py
from flask import Flask, render_template, request, redirect, session, url_for
from models import db, User, Matakuliah

app = Flask(__name__)
app.secret_key = 'supersecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/datamahasiswa'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

#Daftar
    @app.route('/daftar', methods=['GET', 'POST'])
    def daftar():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            nim = request.form['nim']
            password = request.form['password']
            jurusan = request.form['jurusan']
            user = User(username=username, email=email, password=password, jurusan=jurusan, nim=nim)
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        return render_template('daftar.html')

#login
    @app.route('/', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            if user and user.password == password:
                session['id_user'] = user.id
                return redirect('dashboard')
        return render_template('login.html')

#Dashboard
@app.route('/dashboard')
def dashboard():

    user = User.query.get(session['id_user'])
    return render_template('dashboard.html', username=user.username, email=user.email, jurusan=user.jurusan, nim=user.nim)

#Krd
@app.route('/krs', methods=['GET', 'POST'])
def krs():

    user = User.query.get(session['id_user'])

    if request.method == 'POST':
        kode_matkul = request.form.get('kode')
        nama_matkul = request.form.get('matkul')
        sks = request.form.get('sks', type=int)
        nilai = request.form.get('nilai', type=float)

        matkul = Matakuliah(user_id=user.id, kode_matkul=kode_matkul, matkul=nama_matkul, sks=sks, nilai=nilai)
        db.session.add(matkul)
        db.session.commit()
        return redirect(url_for('krs'))

    list_matkul = Matakuliah.query.filter_by(user_id=user.id).all()

    return render_template('krs.html', list_matkul=list_matkul)

#laporan_nilai
@app.route('/laporan_nilai')
def laporan_nilai():

    user = User.query.get(session['id_user'])
    list_matkul = Matakuliah.query.filter_by(user_id=user.id).all()

    # Menghitung total nilai dan IPK
    total_nilai = sum((matkul.nilai * matkul.sks) / 25 for matkul in list_matkul if matkul.nilai is not None)
    total_sks = sum(matkul.sks for matkul in list_matkul)
    ipk = total_nilai / total_sks if total_sks > 0 else 0
    ipk = round(ipk, 2)

    status = 'Aktif' if ipk >= 2 else 'Tidak Aktif'

    matkul_labels = [matkul.matkul for matkul in list_matkul]
    matkul_nilai = [matkul.nilai for matkul in list_matkul]

    return render_template('laporan_nilai.html', user=user, list_matkul=list_matkul, ipk=ipk, total_sks=total_sks, status=status, matkul_labels=matkul_labels,
        matkul_nilai=matkul_nilai)