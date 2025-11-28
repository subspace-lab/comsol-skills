"""Command-line interface for COMSOL documentation search."""

import typer
import re
from typing import Optional
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .core import ComsolDocSearcher
from .formatters import OutputFormatter
from .config import DEFAULT_VERSION, DEFAULT_MAX_RESULTS

app = typer.Typer(
    name="comsol-search",
    help="Search and retrieve COMSOL Multiphysics documentation using browser automation",
    add_completion=False,
)
console = Console()


@app.command()
def search(
    term: str = typer.Argument(..., help="Search term or phrase"),
    version: str = typer.Option(
        DEFAULT_VERSION,
        "--version", "-v",
        help="COMSOL version"
    ),
    max_results: int = typer.Option(
        DEFAULT_MAX_RESULTS,
        "--max-results", "-n",
        help="Maximum number of results to return"
    ),
    module: Optional[str] = typer.Option(
        None,
        "--module", "-m",
        help="Filter by module name (comma-separated for multiple, partial matches allowed)"
    ),
    format: str = typer.Option(
        "table",
        "--format", "-f",
        help="Output format: table, json, markdown, plain"
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Output file (default: stdout)"
    ),
):
    """Search COMSOL documentation for a given term.

    Examples:

        comsol-search search "phase change materials"

        comsol-search search "heat transfer" --version 6.3 --format json

        comsol-search search "turbulent flow" --max-results 50 --output results.json

        comsol-search search "add physics" --module "Application Programming"

        comsol-search search "battery" --module "Battery Design,Heat Transfer"
    """
    searcher = ComsolDocSearcher(version=version, headless=True)
    try:
        # Show progress
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"Searching COMSOL {version} documentation for '{term}'...", total=None)

            # Perform search
            results = searcher.search(term, max_results=max_results)

            # Filter by module if specified
            # Note: Module information is in the path, not the module field
            if module:
                module_filters = [m.strip().lower() for m in module.split(',')]
                original_count = len(results)

                results = [
                    r for r in results
                    if any(module_filter in r.module.lower() for module_filter in module_filters)
                ]

                filtered_count = len(results)
                progress.update(task, description=f"Found {original_count} results, filtered to {filtered_count} by module")
            else:
                progress.update(task, description=f"Found {len(results)} results")

        # Format output
        formatted_output = OutputFormatter.format_search_results(results, format)

        # Write to file or stdout
        if output:
            output.write_text(formatted_output)
            console.print(f"[green]✓[/green] Results saved to {output}")
        else:
            console.print(formatted_output)

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(code=1)
    finally:
        searcher.close()


@app.command()
def retrieve(
    url: str = typer.Argument(..., help="Documentation URL to retrieve"),
    format: str = typer.Option(
        "markdown",
        "--format", "-f",
        help="Output format: markdown, plain, html"
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="Output file (default: stdout)"
    ),
):
    """Retrieve full content from a COMSOL documentation URL.

    Examples:

        comsol-search retrieve "https://doc.comsol.com/6.4/docserver/#!/..."

        comsol-search retrieve <url> --format markdown --output doc.md
    """
    # Extract version from URL if possible
    version_match = re.search(r"/(\d+\.\d+)/", url)
    version = version_match.group(1) if version_match else DEFAULT_VERSION
    
    searcher = ComsolDocSearcher(version=version, headless=True)
    try:
        # Show progress
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"Retrieving content from URL...", total=None)

            # Retrieve content
            doc = searcher.retrieve_content(url)

            progress.update(task, description=f"Retrieved: {doc.title}")

        # Format output
        formatted_output = OutputFormatter.format_document_content(doc, format)

        # Write to file or stdout
        if output:
            output.write_text(formatted_output)
            console.print(f"[green]✓[/green] Content saved to {output}")
        else:
            console.print(formatted_output)

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(code=1)
    finally:
        searcher.close()


@app.command()
def version():
    """Show version information."""
    from . import __version__
    console.print(f"comsol-search version {__version__}")


def main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
