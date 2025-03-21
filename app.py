from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import csv
import yaml  # YAMLライブラリを追加

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pins.db'
CORS(app)

db = SQLAlchemy()

# YAMLファイルへのパス
YAML_FILE_PATH = './get_locate/config.yaml'  # YAMLファイルのパスを設定

class Pin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    checked = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Pin (Lat: {self.latitude}, Lng: {self.longitude}, Checked: {self.checked})>'

    def to_dict(self):
        return {'id': self.id, 'latitude': self.latitude, 'longitude': self.longitude, 'checked': self.checked}

def load_csv_paths_from_yaml(yaml_file_path):
    """YAMLファイルからCSVファイルのパスのリストを読み込む"""
    try:
        with open(yaml_file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data.get('towns',)
    except FileNotFoundError:
        print(f"Error: YAML file not found at {yaml_file_path}")
        return
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return

def populate_database_from_csv(app, towns):
    """指定されたCSVファイルのリストからデータを読み込み、データベースを初期化する"""
    with app.app_context():
        db.create_all()
        for town in towns:
            csv_file_path = f'./get_locate/coordinates/coordinates_{town}.csv'
            print(f"Loading data from: {csv_file_path}")
            try:
                with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        try:
                            latitude = float(row['latitude'])
                            longitude = float(row['longitude'])
                            checked_str = row.get('checked', 'False').strip().lower()
                            checked = checked_str == 'true' or checked_str == '1'

                            existing_pin = Pin.query.filter_by(latitude=latitude, longitude=longitude).first()
                            if not existing_pin:
                                pin = Pin(latitude=latitude, longitude=longitude, checked=checked)
                                db.session.add(pin)
                        except (ValueError, KeyError) as e:
                            print(f"Error processing row in {csv_file_path}: {row}. Error: {e}")
            except FileNotFoundError:
                print(f"Error: CSV file not found at {csv_file_path}")
            except Exception as e:
                print(f"An error occurred while processing {csv_file_path}: {e}")
        db.session.commit()
        print("Initial pins loaded from CSV files.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/pins', methods=['GET'])
def get_pins():
    pins = Pin.query.all()
    return jsonify([pin.to_dict() for pin in pins])

@app.route('/api/pins/<int:pin_id>', methods=['PUT'])
def update_pin(pin_id):
    pin = Pin.query.get_or_404(pin_id)
    data = request.get_json()
    pin.checked = data.get('checked', pin.checked)
    db.session.commit()
    return jsonify({'message': 'Pin updated successfully', 'pin': pin.to_dict()}), 200

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        towns = load_csv_paths_from_yaml(YAML_FILE_PATH)
        populate_database_from_csv(app, towns)
    app.run(debug=True)