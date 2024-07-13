from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from app import db
from app.utils.decorators import lan_only
from app.utils.helpers import get_user_role
from app.external_analysis.analyzer import log_data_access
from app.models.user import User
from app.models.consumption_data import ConsumptionData

bp = Blueprint('main', __name__)

@bp.route('/consumption', methods=['POST'])
@jwt_required() # Authentifizierung: Stellt sicher, dass nur authentifizierte Benutzer Zugriff haben
@lan_only # Zugriffskontrolle: Beschränkt den Zugriff auf das lokale Netzwerk, verhindert externe Angriffe
def add_consumption():
    current_user_id = get_jwt_identity() # Autorisierung: Identifiziert den aktuellen Benutzer
    user = User.find_by_id(current_user_id) # Datenbankabstraktion: Verhindert SQL-Injection
    data = request.get_json() # Eingabevalidierung: Stellt sicher, dass die Daten im JSON-Format sind
    new_consumption = ConsumptionData(
        user_id=user._id,
        value=data['value']
    )
    new_consumption.save_to_db() # Datenbankabstraktion: Verhindert SQL-Injection
    log_data_access('add_consumption', current_user_id) # Loggings: Protokolliert Zugriffe für z.b. Audits
    return jsonify({"message": "Consumption data added successfully", "id": str(new_consumption._id)}), 201

@bp.route('/consumption', methods=['GET'])
@jwt_required() # Authentifizierung: Stellt sicher, dass nur authentifizierte Benutzer Zugriff haben
def get_consumption():
    current_user_id = get_jwt_identity() # Autorisierung: Identifiziert den aktuellen Benutzer
    user = User.find_by_id(current_user_id) # Datenbankabstraktion: Verhindert SQL-Injection
    user_role = user.role
    
    # Autorisierung: Unterscheidet zwischen Admin- und Benutzer-Zugriff
    if user_role == 'admin':
        data_list = db.consumption_data.find()
    else:
        data_list = db.consumption_data.find({"user_id": ObjectId(user._id)})
    
    # Datenbankabstraktion: Verhindert SQL-Injection durch Verwendung von ORM-ähnlichen Methoden
    result = [ConsumptionData(
                user_id=data['user_id'],
                value=data['value'],
                timestamp=data['timestamp'],
                _id=data['_id']
              ).to_dict() for data in data_list]
    
    log_data_access('get_consumption', current_user_id) # Logging: Protokolliert Zugriffe für Audits
    return jsonify(result), 200 # Sichere Datenübertragung: Sendet Daten im JSON-Format