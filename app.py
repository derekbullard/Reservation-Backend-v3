from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


client = MongoClient(os.getenv('MONGO_URI'), server_api=ServerApi('1'))
db = client.appointment_system
providers = db.providers
appointments = db.appointments

# Index to expire reservations after 30 minutes
appointments.create_index("date", expireAfterSeconds=1800)

@app.route('/submit_availability', methods=['POST'])
def submit_availability():
    provider_id = request.json['provider_id']
    date = request.json['date']
    start_time = request.json['start_time']
    end_time = request.json['end_time']

    # Add availability to the provider's document
    providers.update_one(
        {"provider_id": provider_id},
        {"$push": {"availability": {"date": date, "start_time": start_time, "end_time": end_time}}},
        upsert=True
    )
    return jsonify({'status': 'Availability submitted'}), 200

@app.route('/available_slots', methods=['GET'])
def available_slots():
    provider_id = request.args.get('provider_id')
    date = request.args.get('date')
    provider_data = providers.find_one({"provider_id": provider_id, "availability.date": date})

    if provider_data:
        slots = []
        for av in provider_data['availability']:
            if av['date'] == date:
                start_dt = datetime.strptime(f"{date} {av['start_time']}", '%Y-%m-%d %H:%M')
                end_dt = datetime.strptime(f"{date} {av['end_time']}", '%Y-%m-%d %H:%M')
                while start_dt < end_dt:
                    slot = start_dt.strftime('%Y-%m-%d %H:%M')
                    if appointments.count_documents({"slot": slot}) == 0:
                        slots.append(slot)
                    start_dt += timedelta(minutes=15)
        return jsonify(slots), 200
    return jsonify({'error': 'No availability found'}), 404


@app.route('/reserve_slot', methods=['POST'])
def reserve_slot():
    slot = request.json['slot']
    client_id = request.json['client_id']

    # Atomically check and reserve the slot if not already taken
    result = appointments.find_one_and_update(
        {"slot": slot, "status": {"$exists": False}},
        {"$set": {"client_id": client_id, "created_at": datetime.now(), "status": "reserved"}},
        upsert=True,
        return_document=True
    )
    if result:
        return jsonify({'status': 'Slot reserved'}), 200
    else:
        return jsonify({'error': 'Slot already reserved or confirmed'}), 400


@app.route('/confirm_reservation', methods=['POST'])
def confirm_reservation():
    data = request.get_json()
    slot = data.get('slot')
    client_id = data.get('client_id')

    if not slot or not client_id:
        return jsonify({"error": "Missing slot or client_id"}), 400

    result = appointments.find_one_and_update(
        {"slot": slot, "client_id": client_id, "status": "reserved"},
        {"$set": {"status": "confirmed"}}
    )

    if result is None:
        return jsonify({"error": "Reservation not found or already expired"}), 404

    return jsonify({"status": "Reservation confirmed"}), 200


if __name__ == '__main__':
    app.run(debug=True)
