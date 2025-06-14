from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash, jsonify, after_this_request
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os, sys, csv, json, tempfile, socket
from datetime import datetime 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../database')))
from database import ensure_db_initialized, get_db_connection

app = Flask(__name__)
app.secret_key = 'cle-super-secrete'

# Envoyer user_id à la sonde/sniffer
def envoyer_user_id_au_sniffer(user_id):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 5002))
        s.sendall(str(user_id).encode())
        s.close()
    except Exception as e:
        print(f"❌ Erreur envoi user_id : {e}")

# --- Récupérer les détections de l'utilisateur connecté ---
def recuperer_detections():
    if 'user_id' not in session:
        return []
    conn = get_db_connection()
    detections = conn.execute('''
        SELECT ip_src, ip_dst, protocole, verdict, timestamp, url
        FROM detections
        WHERE user_id = ?
        ORDER BY timestamp DESC
    ''', (session['user_id'],)).fetchall()

    conn.close()
    return [dict(d) for d in detections]

# --- Route JSON temps réel ---
@app.route('/detections_json')
def detections_json():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify(recuperer_detections())

# --- ACCUEIL ---
@app.route("/")
def accueil():
    return redirect(url_for('login'))

# --- LOGIN ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    ensure_db_initialized()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['fullname'] = user['fullname'] or user['username']
            session['email'] = user['email'] or 'Non renseigné'
            session['role'] = user['role']
            
            # Envoi dynamique du user_id au sniffer
            envoyer_user_id_au_sniffer(user['id'])

            return redirect(url_for('profile_admin' if user['role'] == 'Admin' else 'profile_user'))

        flash("Nom d'utilisateur ou mot de passe incorrect.", "error")

    return render_template('login.html')

# --- REGISTER ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    ensure_db_initialized()
    if request.method == 'POST':
        username = request.form['username']
        fullname = request.form['fullname']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        try:
            conn = get_db_connection()
            conn.execute('''
                INSERT INTO users (username, fullname, email, password)
                VALUES (?, ?, ?, ?)
            ''', (username, fullname, email, password))
            conn.commit()
            conn.close()
            flash("Inscription réussie, veuillez vous connecter.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Nom d’utilisateur déjà pris.", "error")

    return render_template('register.html')

# --- LOGOUT ---
@app.route('/logout')
def logout():
    session.clear()
    flash("Déconnecté avec succès.", "success")
    return redirect(url_for('login'))

# --- INDEX (détections) ---
@app.route("/index")
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    search = request.args.get("search", "").lower()
    filtre = request.args.get("filtre", "").lower()

    detections = recuperer_detections()

    if search:
        detections = [
            d for d in detections if
            search in d["ip_src"].lower() or
            search in d["ip_dst"].lower() or
            search in d["protocole"].lower() or
            search in d["verdict"].lower() or
            search in d["timestamp"].lower() or
            search in d["url"].lower()
        ]

    if filtre:
        detections = [d for d in detections if filtre in map(str.lower, d.values())]

    stats = afficher_stats(render=False)  # Pour ne pas rendre la page stats, juste récupérer les stats
    return render_template("index.html", alertes=detections, stats=stats)

# --- STATS ---
@app.route("/stats")
def afficher_stats(render=True):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    total = conn.execute("SELECT COUNT(*) FROM detections WHERE user_id = ?", (session['user_id'],)).fetchone()[0]
    phish = conn.execute("SELECT COUNT(*) FROM detections WHERE user_id = ? AND LOWER(verdict) = 'phishing'", (session['user_id'],)).fetchone()[0]
    legit = total - phish
    conn.close()

    phish_rate = round((phish / total) * 100, 2) if total else 0.0

    stats = {
        'total': total,
        'phish': phish,
        'legit': legit,
        'phish_rate': phish_rate
    }

    if render:
        return render_template('stats.html', stats=stats)
    else:
        return stats

# --- EXPORT CSV ---
@app.route('/export_csv')
def export_csv():
    if 'user_id' not in session:
        flash("Connexion requise.", "error")
        return redirect(url_for('login'))

    detections = recuperer_detections()

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv', mode='w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(tmp_file)
        writer.writerow(['Timestamp', 'IP Source', 'IP Destination', 'Protocole', 'URL', 'Verdict'])
        for d in detections:
            writer.writerow([d['timestamp'], d['ip_src'], d['ip_dst'], d['protocole'], d['url'], d['verdict']])
    finally:
        tmp_file.close()

    @after_this_request
    def remove_file(response):
        try:
            os.remove(tmp_file.name)
        except Exception as e:
            print(f"Erreur suppression fichier temporaire : {e}")
        return response

    return send_file(tmp_file.name, as_attachment=True, download_name='export_detections.csv')

# --- EXPORT JSON ---
@app.route('/export_json')
def export_json():
    if 'user_id' not in session:
        flash("Connexion requise.", "error")
        return redirect(url_for('login'))

    detections = recuperer_detections()

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json', mode='w', encoding='utf-8')
    try:
        json.dump(detections, tmp_file, indent=4, ensure_ascii=False)
    finally:
        tmp_file.close()

    @after_this_request
    def remove_file(response):
        try:
            os.remove(tmp_file.name)
        except Exception as e:
            print(f"Erreur suppression fichier print : {e}")
        return response

    return send_file(tmp_file.name, as_attachment=True, download_name='export_detections.json')

# --- PROFILS ---
@app.route('/profil/utilisateur')
def profile_user():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('profile_user.html', user=session)

@app.route('/profil/admin')
def profile_admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('profile_admin.html', user=session)

# --- CHANGER MOT DE PASSE ---
@app.route('/changer-mot-de-passe', methods=['GET', 'POST'])
def changer_mot_de_passe():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not all([current_password, new_password, confirm_password]):
            flash("Merci de remplir tous les champs.", "error")
            return redirect(url_for('changer_mot_de_passe'))

        if new_password != confirm_password:
            flash("Le nouveau mot de passe et la confirmation ne correspondent pas.", "error")
            return redirect(url_for('changer_mot_de_passe'))

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()

        if not user or not check_password_hash(user['password'], current_password):
            conn.close()
            flash("Mot de passe actuel incorrect.", "error")
            return redirect(url_for('changer_mot_de_passe'))

        conn.execute('UPDATE users SET password = ? WHERE id = ?', (generate_password_hash(new_password), session['user_id']))
        conn.commit()
        conn.close()

        flash("Mot de passe modifié avec succès !", "success")
        return redirect(url_for('profile_admin' if session['role'] == 'Admin' else 'profile_user'))

    return render_template('changer_mot_de_passe.html')

# --- SUPPRIMER COMPTE ---
@app.route('/supprimer_compte', methods=['POST'])
def supprimer_compte():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE username = ?', (session['username'],))
    conn.commit()
    conn.close()

    session.clear()
    flash("Ton compte a bien été supprimé.", "success")
    return redirect(url_for('register'))

# --- RUN ---
if __name__ == "__main__":
    ensure_db_initialized()
    app.run(debug=True, port=5003)
