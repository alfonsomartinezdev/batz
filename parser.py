"""Parse freeform text into structured data"""

def parse(text):
    """
    Parse user input. Returns dict with 'name' and 'description', or 'content'.
    """
    text = text.strip()
    
    if ',' in text:
        parts = [p.strip() for p in text.split(',', 1)]
        return {
            'name': parts[0],
            'description': parts[1]
        }
    
    return {
        'content': text
    }