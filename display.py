"""Handle all terminal display and formatting"""
from rich.console import Console
from rich.table import Table

console = Console()

def show_welcome():
    console.print("\n[bold cyan]Batz[/bold cyan] - Madness made Memory\n", 
                  highlight=False)
    console.print("Record your campaign notes naturally:")
    console.print("  'Low places, seedy bar'")
    console.print("  'fishhead joe, bouncer'")
    console.print("  Commands: [dim]session <n>, list, list all, exit[/dim]\n")

def show_entities(entities, show_all):
    """Display all entities in a table"""
    if not entities:
        console.print("No entries yet!", style="yellow")
        return
    title = "Campaign Notes" if show_all else "Session Notes"
    table = Table(title=title)
    table.add_column("ID", style="cyan", width=4)
    table.add_column("Session", style="magenta", width=7)
    table.add_column("Entry", style="white")
    
    for entity in entities:
        text = _format_entity_text(entity)
        session_str = str(entity.get('session', '?'))
        table.add_row(str(entity['id']), session_str, text)
    
    console.print(table)

def say_success(entity_id, session):
    console.print(f"✓ Recorded #{entity_id} (Session {session})", style="green")

def say_goodbye():
    console.print("The scribe rests.", style="dim cyan")

def say_error(message):
    console.print(f"[red]Error:[/red] {message}")

def say_session_change(session, is_new):
    if is_new:
        console.print(f"Started session {session}", style="cyan")
    else:
        console.print(f"Switched to session {session}", style="cyan")


### helpers ###

def _format_entity_text(entity):
    """Helper to format entity display text"""
    if 'name' in entity:
        text = f"[bold]{entity['name']}[/bold]"
        if 'description' in entity:
            text += f" - {entity['description']}"
        return text
    return entity.get('content', '')