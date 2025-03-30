from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create a Patient model
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    insurance_number = db.Column(db.String(50), unique=True, nullable=False)
    folder_number = db.Column(db.String(50), unique=True, nullable=False)

@app.route('/')
def home():
    patients = Patient.query.all()
    return render_template('index.html', patients=patients)

@app.route('/add_patient', methods=['POST'])
def add_patient():
    name = request.form['name']
    insurance_number = request.form['insurance_number']
    folder_number = request.form['folder_number']

    new_patient = Patient(name=name, insurance_number=insurance_number, folder_number=folder_number)
    db.session.add(new_patient)
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run(debug=True)
@app.route('/delete_patient/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if patient:
        db.session.delete(patient)
        db.session.commit()
    return redirect('/')

