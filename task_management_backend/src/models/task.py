from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    deadline = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.Enum('pending', 'in_progress', 'completed', 'cancelled', name='task_status'), 
                      default='pending', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    checklist_items = db.relationship('ChecklistItem', backref='task', lazy=True, cascade='all, delete-orphan')
    links = db.relationship('TaskLink', backref='task', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Task {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'notes': self.notes,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'checklist_items': [item.to_dict() for item in self.checklist_items],
            'links': [link.to_dict() for link in self.links]
        }

class ChecklistItem(db.Model):
    __tablename__ = 'checklist_items'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    is_completed = db.Column(db.Boolean, default=False, nullable=False)
    order_index = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<ChecklistItem {self.description}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'description': self.description,
            'is_completed': self.is_completed,
            'order_index': self.order_index,
            'created_at': self.created_at.isoformat()
        }

class TaskLink(db.Model):
    __tablename__ = 'task_links'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    url = db.Column(db.String(2000), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<TaskLink {self.url}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'url': self.url,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }

