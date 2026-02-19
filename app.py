import os
from flask import Flask, render_template, request, redirect, url_for
from models import db, Memory
from dotenv import load_dotenv

# Load local .env file for testing (we will create this next)
load_dotenv()

app = Flask(__name__)

# REQUIREMENT: Use environment variables for DB configuration
# 'sqlite:///test.db' is a backup for local testing before we move to Azure SQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("AZURE_SQL_CONNECTIONSTRING", "sqlite:///test.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create the local database file automatically
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # READ: Get all memories from the database
    memories = Memory.query.all()
    return render_template('index.html', memories=memories)


@app.route('/add', methods=['POST'])
def add_memory():
    # 1. Get text from the form
    title = request.form.get('title')
    description = request.form.get('description')

    # 2. Handle the File (We will link this to Azure later)
    file = request.files.get('photo')
    if file:
        # For now, we'll use a placeholder.
        # In the next step, we write the code to send this to Azure Blob Storage!
        image_url = "https://via.placeholder.com/150"
    else:
        image_url = None

    # 3. Save to Database (Requirement: CRUD - Create)
    new_memory = Memory(title=title, description=description, image_url=image_url)
    db.session.add(new_memory)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_memory(id):
    memory_to_delete = Memory.query.get_or_404(id)
    db.session.delete(memory_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)