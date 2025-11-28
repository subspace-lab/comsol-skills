"""Output formatting for COMSOL documentation search results."""

from typing import List
import json
from rich.console import Console
from rich.table import Table

from .models import SearchResult, DocumentContent


class OutputFormatter:
    """Formats search results and document content for different output modes."""

    @staticmethod
    def format_search_results(results: List[SearchResult], format: str) -> str:
        """Format search results based on output format.

        Args:
            results: List of SearchResult objects
            format: Output format (table, json, markdown, plain)

        Returns:
            Formatted string ready for output
        """
        if format == "json":
            return OutputFormatter._format_json(results)
        elif format == "markdown":
            return OutputFormatter._format_markdown(results)
        elif format == "plain":
            return OutputFormatter._format_plain(results)
        elif format == "table":
            return OutputFormatter._format_table(results)
        else:
            raise ValueError(f"Unknown format: {format}")

    @staticmethod
    def _format_table(results: List[SearchResult]) -> str:
        """Format results as a rich table."""
        console = Console()

        table = Table(title=f"COMSOL Documentation Search Results ({len(results)} found)")
        table.add_column("Module", style="cyan", no_wrap=False)
        table.add_column("Title", style="green", no_wrap=False)
        table.add_column("Path", style="yellow")
        table.add_column("Snippet", style="white", no_wrap=False, max_width=50)

        for result in results:
            table.add_row(
                result.module,
                result.title,
                result.path,
                result.snippet[:100] + "..." if len(result.snippet) > 100 else result.snippet
            )

        # Capture table output as string
        from io import StringIO
        string_io = StringIO()
        temp_console = Console(file=string_io, force_terminal=True)
        temp_console.print(table)
        return string_io.getvalue()

    @staticmethod
    def _format_json(results: List[SearchResult]) -> str:
        """Format results as JSON."""
        return json.dumps(
            [result.to_dict() for result in results],
            indent=2,
            ensure_ascii=False
        )

    @staticmethod
    def _format_markdown(results: List[SearchResult]) -> str:
        """Format results as Markdown."""
        lines = [f"# COMSOL Documentation Search Results\n"]
        lines.append(f"**Found {len(results)} results**\n")

        current_module = None
        for i, result in enumerate(results, 1):
            # Add module header if it changed
            if result.module != current_module:
                current_module = result.module
                lines.append(f"\n## {current_module}\n")

            lines.append(f"### {i}. {result.title}\n")
            lines.append(f"**Path:** {result.path}\n")
            lines.append(f"**Snippet:** {result.snippet}\n")

        return '\n'.join(lines)

    @staticmethod
    def _format_plain(results: List[SearchResult]) -> str:
        """Format results as plain text."""
        lines = [f"COMSOL Documentation Search Results ({len(results)} found)\n"]
        lines.append("=" * 70 + "\n")

        for i, result in enumerate(results, 1):
            lines.append(f"\n{i}. [{result.module}]")
            lines.append(f"   Title: {result.title}")
            lines.append(f"   Path: {result.path}")
            lines.append(f"   Snippet: {result.snippet}")
            lines.append("")

        return '\n'.join(lines)

    @staticmethod
    def format_document_content(doc: DocumentContent, format: str) -> str:
        """Format document content based on output format.

        Args:
            doc: DocumentContent object
            format: Output format (markdown, plain, html)

        Returns:
            Formatted string ready for output
        """
        if format == "markdown":
            return OutputFormatter._format_doc_markdown(doc)
        elif format == "plain":
            return OutputFormatter._format_doc_plain(doc)
        elif format == "html":
            return OutputFormatter._format_doc_html(doc)
        else:
            raise ValueError(f"Unknown format: {format}")

    @staticmethod
    def _format_doc_markdown(doc: DocumentContent) -> str:
        """Format document as Markdown."""
        lines = [f"# {doc.title}\n"]

        if doc.breadcrumb:
            lines.append(f"**Location:** {' > '.join(doc.breadcrumb)}\n")

        lines.append(f"**URL:** {doc.url}\n")
        lines.append("---\n")
        lines.append(doc.content)

        return '\n'.join(lines)

    @staticmethod
    def _format_doc_plain(doc: DocumentContent) -> str:
        """Format document as plain text."""
        lines = [doc.title]
        lines.append("=" * len(doc.title))
        lines.append("")

        if doc.breadcrumb:
            lines.append(f"Location: {' > '.join(doc.breadcrumb)}")

        lines.append(f"URL: {doc.url}")
        lines.append("-" * 70)
        lines.append("")
        lines.append(doc.content)

        return '\n'.join(lines)

    @staticmethod
    def _format_doc_html(doc: DocumentContent) -> str:
        """Format document as simple HTML."""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{doc.title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        .breadcrumb {{ color: #666; margin-bottom: 20px; }}
        .content {{ line-height: 1.6; }}
    </style>
</head>
<body>
    <h1>{doc.title}</h1>
    <div class="breadcrumb">Location: {' > '.join(doc.breadcrumb)}</div>
    <p><a href="{doc.url}">{doc.url}</a></p>
    <hr>
    <div class="content">
        <pre>{doc.content}</pre>
    </div>
</body>
</html>"""
        return html
