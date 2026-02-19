from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Memory(db.Model):
    # This creates a table in Azure SQL called 'memory'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))  # This stores the link to your Azure Blob