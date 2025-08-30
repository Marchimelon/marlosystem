from flask import Blueprint, jsonify, request, make_response
from datetime import datetime
import csv
import io
from src.models.task import Task, ChecklistItem, TaskLink, db

task_bp = Blueprint('task', __name__)

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    # Get query parameters for filtering
    status = request.args.get('status')
    search = request.args.get('search')
    
    query = Task.query
    
    # Apply filters
    if status:
        query = query.filter(Task.status == status)
    
    if search:
        query = query.filter(Task.name.contains(search) | Task.notes.contains(search))
    
    # Order by created_at descending by default
    tasks = query.order_by(Task.created_at.desc()).all()
    
    return jsonify([task.to_dict() for task in tasks])

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.json
        
        # Create task
        task = Task(
            name=data['name'],
            deadline=datetime.fromisoformat(data['deadline']) if data.get('deadline') else None,
            notes=data.get('notes', ''),
            status=data.get('status', 'pending')
        )
        
        db.session.add(task)
        db.session.flush()  # Get the task ID
        
        # Add checklist items
        if data.get('checklist_items'):
            for i, item_data in enumerate(data['checklist_items']):
                checklist_item = ChecklistItem(
                    task_id=task.id,
                    description=item_data['description'],
                    is_completed=item_data.get('is_completed', False),
                    order_index=i
                )
                db.session.add(checklist_item)
        
        # Add links
        if data.get('links'):
            for link_data in data['links']:
                task_link = TaskLink(
                    task_id=task.id,
                    url=link_data['url'],
                    description=link_data.get('description', '')
                )
                db.session.add(task_link)
        
        db.session.commit()
        return jsonify(task.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())

@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        task = Task.query.get_or_404(task_id)
        data = request.json
        
        # Update task fields
        task.name = data.get('name', task.name)
        task.deadline = datetime.fromisoformat(data['deadline']) if data.get('deadline') else task.deadline
        task.notes = data.get('notes', task.notes)
        task.status = data.get('status', task.status)
        task.updated_at = datetime.utcnow()
        
        # Update checklist items
        if 'checklist_items' in data:
            # Remove existing checklist items
            ChecklistItem.query.filter_by(task_id=task.id).delete()
            
            # Add new checklist items
            for i, item_data in enumerate(data['checklist_items']):
                checklist_item = ChecklistItem(
                    task_id=task.id,
                    description=item_data['description'],
                    is_completed=item_data.get('is_completed', False),
                    order_index=i
                )
                db.session.add(checklist_item)
        
        # Update links
        if 'links' in data:
            # Remove existing links
            TaskLink.query.filter_by(task_id=task.id).delete()
            
            # Add new links
            for link_data in data['links']:
                task_link = TaskLink(
                    task_id=task.id,
                    url=link_data['url'],
                    description=link_data.get('description', '')
                )
                db.session.add(task_link)
        
        db.session.commit()
        return jsonify(task.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

@task_bp.route('/tasks/<int:task_id>/checklist/<int:item_id>', methods=['PATCH'])
def update_checklist_item(task_id, item_id):
    try:
        item = ChecklistItem.query.filter_by(id=item_id, task_id=task_id).first_or_404()
        data = request.json
        
        item.is_completed = data.get('is_completed', item.is_completed)
        item.description = data.get('description', item.description)
        
        db.session.commit()
        return jsonify(item.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@task_bp.route('/reports/export', methods=['GET'])
def export_tasks():
    try:
        # Get query parameters for filtering
        status = request.args.get('status')
        search = request.args.get('search')
        format_type = request.args.get('format', 'csv')
        
        query = Task.query
        
        # Apply filters
        if status:
            query = query.filter(Task.status == status)
        
        if search:
            query = query.filter(Task.name.contains(search) | Task.notes.contains(search))
        
        tasks = query.order_by(Task.created_at.desc()).all()
        
        if format_type.lower() == 'csv':
            return export_csv(tasks)
        else:
            return jsonify({'error': 'Unsupported format'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def export_csv(tasks):
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'ID', 'Name', 'Status', 'Deadline', 'Notes', 
        'Created At', 'Updated At', 'Checklist Items', 'Links'
    ])
    
    # Write data
    for task in tasks:
        checklist_text = '; '.join([
            f"{'✓' if item.is_completed else '○'} {item.description}" 
            for item in task.checklist_items
        ])
        
        links_text = '; '.join([
            f"{link.description or 'Link'}: {link.url}" 
            for link in task.links
        ])
        
        writer.writerow([
            task.id,
            task.name,
            task.status,
            task.deadline.strftime('%Y-%m-%d %H:%M') if task.deadline else '',
            task.notes or '',
            task.created_at.strftime('%Y-%m-%d %H:%M'),
            task.updated_at.strftime('%Y-%m-%d %H:%M'),
            checklist_text,
            links_text
        ])
    
    output.seek(0)
    
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=tasks_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    return response

