"""Handle all data persistence operations"""
import json
import os

DATA_FILE = 'batz.json'


def load():
    """Load all campaign data from file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'entities': [], 'counter': 0, 'current_session': 1}  # Add current_session


def get_current_session(data):
    """Get the current session number"""
    return data.get('current_session', 1)


def set_current_session(data, session):
    """Update the current session"""
    data['current_session'] = session


def save(data):
    """Save all campaign data to file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def add_entity(data, entity_data, session):
    """Add a new entity and return it"""
    data['counter'] += 1
    entity = {
        'id': data['counter'],
        'session': session,
        **entity_data
    }
    data['entities'].append(entity)
    return entity


def get_all_entities(data):
    """Return all entities"""
    return data['entities']


def get_entities_by_session(data, session):
    """Return entities from a specific session"""
    return [e for e in data['entities'] if e.get('session') == session]