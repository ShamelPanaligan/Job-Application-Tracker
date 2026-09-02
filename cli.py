import typer
from rich.console import Console
from rich.table import Table

from db import get_connection, init_db, add_application, list_applications
from models import Application, Status
from datetime import date

#app setup
app = typer.Typer()
console = Console()

@app.command()
def add(
    company: str = typer.Option(..., "--company"),
    role: str = typer.Option(..., "--role"),
    source: str = typer.Option(None, "--source"),
    link: str = typer.Option(None, "--link"),

):
    conn = get_connection()
    init_db(conn)
    new_app = Application(
        company = company,
        role = role,
        status = Status.APPLIED,
        date_applied = date.today(),
        source = source,
        link = link,
    )
    saved = add_application(conn, new_app)
    console.print(f"Saved application: {saved} with ID: {saved.id}")
    conn.close()

@app.command(name="list")
def list_apps():
    conn = get_connection()
    init_db(conn)
    apps = list_applications(conn)
    table = Table(title="All Applications")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Company", style="magenta")
    table.add_column("Role", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("Date Applied", style="blue")

    for a in apps:
        table.add_row(str(a.id), a.company, a.role, a.status.value, a.date_applied.isoformat())
    console.print(table)
    conn.close()


if __name__ == "__main__":
    app()
    