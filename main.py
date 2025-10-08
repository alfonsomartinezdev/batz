"""Main CLI interface for Itzamna"""
from rich.prompt import Prompt
import storage
import parser
import display

def main():
    """Run the interactive note-taking session"""
    display.show_welcome()
    data = storage.load()
    current_session = storage.get_current_session(data)
    display.say_session_change(current_session, is_new=False)
    
    while True:
        try:
            user_input = Prompt.ask("[bold green]>[/bold green]").strip()
            
            if not user_input:
                continue
            
            cmd = user_input.lower()
            
            if cmd in ['exit', 'quit', 'q']:
                display.say_goodbye()
                break
            
            elif cmd.startswith('session '):
                new_session = handle_session(data, user_input)
                if new_session:
                    current_session = new_session
            
            elif cmd in ['list', 'ls', 'l'] or cmd.startswith(('list ', 'ls ', 'l ')):
                handle_list(data, user_input, current_session)
            
            else:
                handle_note(data, user_input, current_session)
        
        except KeyboardInterrupt:
            display.say_goodbye()
            break
        except Exception as e:
            display.say_error(str(e))


def handle_session(data, user_input):
    """Handle session command"""
    try:
        session_num = int(user_input.split()[1])
        existing = storage.get_entities_by_session(data, session_num)
        is_new = len(existing) == 0
        storage.set_current_session(data, session_num)
        storage.save(data)
        display.say_session_change(session_num, is_new)
        return session_num
    except (IndexError, ValueError):
        display.say_error("Usage: session <number>")
        return None


def handle_list(data, user_input, current_session):
    """Handle list command"""
    show_all = 'all' in user_input.lower()
    entities = storage.get_all_entities(data) if show_all else storage.get_entities_by_session(data, current_session)
    display.show_entities(entities, show_all)


def handle_note(data, user_input, current_session):
    """Handle creating a new note"""
    parsed = parser.parse(user_input)
    entity = storage.add_entity(data, parsed, current_session)
    storage.save(data)
    display.say_success(entity['id'], current_session)


if __name__ == '__main__':
    main()