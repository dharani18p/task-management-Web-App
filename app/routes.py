from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models import User, Task
from flask_jwt_extended import (
    create_access_token, 
    set_access_cookies, 
    jwt_required, 
    get_jwt_identity
)

api_bp = Blueprint("api_bp", __name__)

# ---------------- USER API ROUTES ----------------
@api_bp.route("/users/register", methods=["POST"])
def register_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all([name, email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(name=name, email=email, password_hash=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully", "user_id": user.user_id}), 201


@api_bp.route("/users/login", methods=["POST"])
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    if bcrypt.check_password_hash(user.password_hash, password):
        # 👇 THIS IS THE ONLY LINE THAT CHANGED
        token = create_access_token(identity=str(user.user_id))
        
        response = jsonify({"msg": "Login successful", "user_id": user.user_id})
        set_access_cookies(response, token)
        
        return response
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@api_bp.route("/users/me", methods=["GET"])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "registration_date": user.registration_date.isoformat()
    })


# ---------------- TASK ROUTES ----------------
@api_bp.route("/tasks", methods=["POST"])
@jwt_required(locations=['cookies']) # <--- This now correctly looks for a cookie
def add_task():
    data = request.get_json()
    user_id = int(get_jwt_identity()) # Securely get user ID from token
    title = data.get("title")
    if not title:
        return jsonify({"error": "Title required"}), 400

    task = Task(
        title=title,
        description=data.get("description"),
        status=data.get("status", "pending"),
        priority=data.get("priority", "medium"),
        assigned_user_id=user_id,
        due_date=data.get("due_date"),
        due_time=data.get("due_time")
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({"msg": "Task created", "task_id": task.task_id}), 201


@api_bp.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = int(get_jwt_identity())
    
    # Get query parameters from the URL for filtering and pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    status = request.args.get('status', None, type=str)
    priority = request.args.get('priority', None, type=str)

    # Start building the query
    query = Task.query.filter_by(assigned_user_id=user_id)

    # Apply filters if they were provided in the request
    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    
    # Apply pagination and order the results
    paginated_tasks = query.order_by(Task.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    tasks = paginated_tasks.items
    
    return jsonify({
        "tasks": [{
            "task_id": t.task_id,
            "title": t.title,
            "description": t.description,
            "status": t.status,
            "priority": t.priority,
            "due_date": t.due_date.isoformat() if t.due_date else None,
            "due_time": t.due_time.isoformat() if t.due_time else None,
            "created_at": t.created_at.isoformat() if t.created_at else None
        } for t in tasks],
        "pagination": {
            "total_pages": paginated_tasks.pages,
            "current_page": paginated_tasks.page,
            "has_next": paginated_tasks.has_next,
            "has_prev": paginated_tasks.has_prev
        }
    })

# ---------------- ANALYTICS ROUTE ----------------
@api_bp.route("/analytics", methods=["GET"])
@jwt_required()
def get_analytics():
    user_id = get_jwt_identity()
    
    # Base query for the logged-in user's tasks
    user_tasks = Task.query.filter_by(assigned_user_id=user_id)
    
    total_tasks = user_tasks.count()
    
    # Efficiently count tasks for each status
    tasks_by_status = {
        "pending": user_tasks.filter_by(status='pending').count(),
        "in_progress": user_tasks.filter_by(status='in-progress').count(),
        "completed": user_tasks.filter_by(status='completed').count(),
    }
    
    return jsonify({
        "total_tasks": total_tasks,
        "tasks_by_status": tasks_by_status
    })

# In app/routes.py

# In app/routes.py, replace your existing update_task function with this one.

@api_bp.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required(locations=['cookies'])
def update_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.get(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404
    if str(task.assigned_user_id) != user_id:
        return jsonify({"error": "Unauthorized to update this task"}), 403

    data = request.get_json()

    # NEW: Check if any data was sent in the body
    if not data:
        return jsonify({"error": "Request body cannot be empty"}), 400

    # Update fields if they are provided in the request
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    task.priority = data.get('priority', task.priority)
    
    # Safely handle date updates if provided
    if 'due_date' in data:
        task.due_date = data['due_date']
    
    db.session.commit()

    return jsonify({"msg": "Task updated successfully"})
# In app/routes.py

@api_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required(locations=['cookies'])
def delete_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.get(task_id)

    # Security check
    if not task:
        return jsonify({"error": "Task not found"}), 404
    if str(task.assigned_user_id) != user_id:
        return jsonify({"error": "Unauthorized"}), 403
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({"msg": "Task deleted successfully"})