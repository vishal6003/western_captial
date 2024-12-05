from flask import Blueprint, jsonify, request
from datetime import datetime
from .models import Task, db

bp = Blueprint('main', __name__)

@bp.route('/')
def read_root():
    return jsonify({
        "message": "Welcome to Task Manager API",
        "status": "running",
        "version": "1.0",
        "endpoints": {
            "get_tasks": "/tasks",
            "create_task": "/tasks",
            "update_task": "/tasks/<id>",
            "delete_task": "/tasks/<id>"
        }
    })

@bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        'id': task.id,
        'contact_person': task.contact_person,
        'entity_name': task.entity_name,
        'task_type': task.task_type,
        'status': task.status,
        'task_time': task.task_time,
        'creation_date': task.creation_date,
        'note': task.note
    } for task in tasks])

@bp.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debug log

        # Create new task with current timestamp for creation_date
        task = Task(
            contact_person=data['contact_person'],
            entity_name=data['entity_name'],
            task_type=data['task_type'],
            status=data.get('status', 'pending'),
            task_time=data['task_time'],
            creation_date=datetime.utcnow(),
            note=data.get('note', '')
        )

        db.session.add(task)
        db.session.commit()

        # Return the created task
        return jsonify({
            'id': task.id,
            'contact_person': task.contact_person,
            'entity_name': task.entity_name,
            'task_type': task.task_type,
            'status': task.status,
            'task_time': task.task_time,
            'creation_date': task.creation_date.isoformat(),
            'note': task.note
        }), 201

    except Exception as e:
        print("Error creating task:", str(e))  # Debug log
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    
    task.contact_person = data['contact_person']
    task.entity_name = data['entity_name']
    task.task_type = data['task_type']
    task.status = data['status']
    task.task_time = data['task_time']
    task.note = data.get('note', task.note)
    
    db.session.commit()
    return jsonify({
        'id': task.id,
        'contact_person': task.contact_person,
        'entity_name': task.entity_name,
        'task_type': task.task_type,
        'status': task.status,
        'task_time': task.task_time,
        'creation_date': task.creation_date,
        'note': task.note
    })

@bp.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return '', 204