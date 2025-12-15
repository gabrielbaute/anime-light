from rich.console import Console
from rich.table import Table

console = Console()

__version__ = "0.3.2"

def show_version() -> None:
    """
    Shows the CLI version
    """
    console = Console()
    table = Table(
        title="[bold magenta]anime-light[/bold magenta]",
        show_header=False,
        border_style="blue",
        padding=(0, 2),
    )
    table.add_column("Key", style="cyan", justify="right")
    table.add_column("Value", style="green")
    
    table.add_row("[yellow]Build[/yellow]", "[bold]stable[/bold]")
    table.add_row("Versión", f"[bold]{__version__}[/bold]")
    table.add_row("Author", "Gabriel Baute")
    table.add_row("License", "MIT")
    table.add_row("Repo", "https://github.com/gabrielbaute/anime-light")

    console.print(table)