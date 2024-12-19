import os,json,datetime
import hashlib,platform,uuid
from flask import Flask, jsonify, request

app = Flask(__name__)

LICENSE_FILE = "tmp/licenses.json"

def get_key_from_device():
    hostname = platform.node()
    system_info = platform.system() + platform.machine()
    raw_data = f"{hostname}-{system_info}"
    hashed_id = hashlib.sha256(raw_data.encode()).hexdigest()[:33]
    return hashed_id
    
@app.route("/generate", methods=["POST"])
def generate_license():
    license_key = get_key_from_device()
    try:
        with open(LICENSE_FILE, "r") as file:
            licenses = json.load(file)
    except FileNotFoundError:
        licenses = {}
    if license_key in licenses:
        return jsonify({
            "message": "License already exists", 
            "license_key": licenses[license_key]["license_key"], 
            "expiry": licenses[license_key]["expiry_date"]
        })
    else:
        expiry_date = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%d-%m-%Y")
        licenses[license_key] = {
            "license_key": license_key,
            "expiry_date": expiry_date
        }
        with open(LICENSE_FILE, "w") as file:
            json.dump(licenses, file, indent=4)
        return jsonify({
            "message": "License created successfully",
            "license_key": license_key,
            "expiry": expiry_date
        })
        

if __name__ == "__main__":
    app.run(debug=True)
