"""Parse freeform text into structured data"""
import json
import ollama


def parse(text):
    """Main parse function - tries LLM, falls back to simple"""
    text = text.strip()
    
    try:
        extracted = parse_with_llama(text)
        
        if extracted and extracted.get("is_entity"):
            return build_entity(extracted)
        else:
            return build_note(text)
            
    except Exception as e:
        print(f"LLM failed: {e}, using fallback")
        return parse_simple(text)


def parse_with_llama(text):
    """Extract entity information using LLM"""
    raw_response = call_llama(text)
    return json.loads(raw_response)


def build_entity(extracted):
    """Build entity structure from LLM extraction"""
    return {
        'name': extracted['entity_name'],
        'type': extracted['entity_category'],
        'traits': extracted.get('entity_attributes', [])
    }


def build_note(text):
    """Build note structure"""
    return {
        'content': text
    }


def parse_simple(text):
    """Fallback: simple comma-based parsing"""
    if ',' in text:
        parts = [p.strip() for p in text.split(',', 1)]
        return {
            'name': parts[0],
            'description': parts[1]
        }
    return {
        'content': text
    }

def call_llama(text):
    """Send text to LLM and get raw response"""
    prompt = f"""This text is a gamemaster's RPG campaign note: "{text}"

Does this mention a SPECIFIC named entity? (A person or place with a PROPER NAME)

If YES, extract:
  - The entity's NAME (proper noun only)
  - Its CATEGORY (person, place, thing, or event)
  - ALL descriptive information (what it is, traits, appearance, etc.)

Examples:
"Low places is a sleazy bar" → name: "Low places", category: "place", attributes: ["sleazy", "bar"]
"Fishhead Joe, bouncer" → name: "Fishhead Joe", category: "person", attributes: ["bouncer"]

If NOT a named entity, return:
{{"is_entity": false}}

If IS a named entity, return:
{{"is_entity": true, "entity_name": "Entity Name", "entity_category": "person", "entity_attributes": ["trait1", "trait2"]}}

Return ONLY JSON. No other text.
"""
    
    response = ollama.chat(
        model='llama3.2:3b',
        messages=[{'role': 'user', 'content': prompt}],
        options={'temperature': 0}
    )
    
    return response['message']['content'].strip()