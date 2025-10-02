from run import create_app, db
from app.models import User, Task  # import your models

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ All tables created successfully in MySQL!")
