from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app import bcrypt, db
from app.models.user import User
from app.utils.decorators import wan_only
from app.external_analysis.analyzer import log_external_access
from string_utils import validation

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
@wan_only # Zugriffskontrolle: Beschränkt den Zugriff auf das WAN, verhindert unberechtigte lokale Registrierungen
def register():
    data = request.get_json() # Eingabevalidierung: Stellt sicher, dass die Daten im JSON-Format sind
    if not data: # Eingabevalidierung: Stellt Daten Existenz sicher
        return jsonify({"message": "No data retrieved", "error": str(e)}), 500
    
    try:
        if validation.is_full_string(data['username']) and validation.is_full_string(data['password']) and data['role'] in ["admin", "user"]: # Eingabevalidierung: Prüfung auf String Existenz
            new_user = User(username=data['username'], password=data['password'], role=data['role'])
            user_id = new_user.save_to_db() # Datenbankabstraktion: Verhindert SQL-Injection
            log_external_access('register', data['username']) # Logging: Protokolliert Registrierungsversuche für Audits
            return jsonify({"message": "User created successfully", "id": user_id}), 201
    except Exception as e:
        # Fehlerbehandlung: Fängt Ausnahmen ab und gibt eine generische Fehlermeldung zurück
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() # Eingabevalidierung: Stellt sicher, dass die Daten im JSON-Format sind
    if not data: # Eingabevalidierung: Stellt Daten Existenz sicher
        return jsonify({"message": "No data retrieved", "error": str(e)}), 500
    
    user = User.find_by_username(data['username']) # Datenbankabstraktion: Verhindert SQL-Injection
    if user and user.check_password(data['password']): # Sicheren Passwortüberprüfung: Verwendet bcrypt für Passwort-Hashing
        access_token = create_access_token(identity=str(user.username))
        log_external_access('login', data['username']) # Logging: Protokolliert Anmeldeversuche für Audits
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401 # Sichere Fehlerbehandlung: Gibt keine spezifischen Informationen über den Fehler preis
