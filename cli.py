import typer
from rich.console import Console
from rich.table import Table

from db import get_connection, init_db, add_application, list_applications, update_status, archive_application, filter_applications
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

@app.command(name="update")
def update(
    application_id = typer.Argument(..., help = "The ID of the application to update"),
    new_status: Status = typer.Option(..., "--status", help="The new status for the application")
):
    conn =get_connection()
    init_db(conn)
    updated_app = update_status(conn, application_id, new_status)
    console.print(f"Updated application: {updated_app} with new status: {updated_app.status.value}")
    conn.close()

@app.command(name="archive")
def archive(application_id: int):
    conn = get_connection()
    init_db(conn)
    existing_app = conn.execute("SELECT * FROM applications WHERE id = ?", (application_id,)).fetchone()
    if existing_app is None:
        console.print(f"No application found with ID: {application_id}")
        conn.close()
        raise typer.Exit(code=1)
    archived_app = archive_application(conn, application_id)
    console.print(f"Archived application: {archived_app} with ID: {archived_app.id}")
    conn.close()

@app.command(name="filter")
def filter_apps(
    status: Status | None = typer.Option(None, "--status", help="Filter by application status"),
    company: str | None = typer.Option(None, "--company", help="Filter by company name")
):
    conn = get_connection()
    init_db(conn)
    filter_apps = filter_applications(conn, status, company)
    table = Table(title="Filtered Applications")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Company", style="magenta")
    table.add_column("Role", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("Date Applied", style="blue")

    for a in filter_apps:
        table.add_row(str(a.id), a.company, a.role, a.status.value, a.date_applied.isoformat())
    console.print(table)
    conn.close()

if __name__ == "__main__":
    app()
