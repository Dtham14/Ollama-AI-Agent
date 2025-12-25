"""
Markdown formatter for composer data.
"""

from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path


class MarkdownFormatter:
    """
    Formats composer data into structured markdown files.

    Template includes:
    - YAML frontmatter with metadata
    - Biography section
    - Musical style section
    - Notable works section
    - Legacy section
    - Sources section
    """

    def format(
        self,
        composer_info: Dict[str, Any],
        scraped_data: Dict[str, Any],
        output_path: Path = None,
    ) -> str:
        """
        Format composer data into markdown.

        Args:
            composer_info: Composer metadata (name, birth/death, era, etc.)
            scraped_data: Dictionary of scraped data by source
            output_path: Optional path where file will be saved

        Returns:
            Formatted markdown string
        """
        sections = []

        # YAML Frontmatter
        frontmatter = self._generate_frontmatter(composer_info, scraped_data)
        sections.append(frontmatter)

        # Title
        name = composer_info.get("name", "Unknown Composer")
        birth_year = composer_info.get("birth_year", "")
        death_year = composer_info.get("death_year", "")

        if birth_year and death_year:
            title = f"# {name} ({birth_year}-{death_year})"
        elif birth_year:
            title = f"# {name} (b. {birth_year})"
        else:
            title = f"# {name}"

        sections.append(title)

        # Overview metadata
        overview = []
        if composer_info.get("era"):
            overview.append(f"**Era:** {composer_info['era']}")
        if composer_info.get("nationality"):
            overview.append(f"**Nationality:** {composer_info['nationality']}")

        if overview:
            sections.append("\n".join(overview))

        # Biography section
        biography = self._consolidate_biography(scraped_data)
        if biography:
            sections.append("## Biography\n\n" + biography)

        # Musical Style section
        style = self._consolidate_style(scraped_data)
        if style:
            sections.append("## Musical Style and Characteristics\n\n" + style)

        # Notable Works section
        works = self._consolidate_works(scraped_data)
        if works:
            sections.append("## Notable Works\n\n" + works)

        # Legacy section
        legacy = self._consolidate_legacy(scraped_data)
        if legacy:
            sections.append("## Legacy and Influence\n\n" + legacy)

        # Sources section
        sources = self._generate_sources_section(scraped_data)
        if sources:
            sections.append("## Sources\n\n" + sources)

        return "\n\n---\n\n".join(sections)

    def _generate_frontmatter(
        self, composer_info: Dict[str, Any], scraped_data: Dict[str, Any]
    ) -> str:
        """Generate YAML frontmatter"""
        lines = ["---"]

        # Add metadata
        if composer_info.get("id"):
            lines.append(f"composer_id: {composer_info['id']}")
        lines.append(f"name: {composer_info.get('name', 'Unknown')}")
        if composer_info.get("normalized_name"):
            lines.append(f"normalized_name: {composer_info['normalized_name']}")

        if composer_info.get("birth_year"):
            lines.append(f"birth_year: {composer_info['birth_year']}")
        if composer_info.get("death_year"):
            lines.append(f"death_year: {composer_info['death_year']}")

        if composer_info.get("era"):
            lines.append(f"era: {composer_info['era']}")
        if composer_info.get("nationality"):
            lines.append(f"nationality: {composer_info['nationality']}")

        lines.append(f"scraped_date: {datetime.utcnow().strftime('%Y-%m-%d')}")

        # Add source URLs
        lines.append("sources:")
        for source_name, data in scraped_data.items():
            if data.success and data.metadata.get("url"):
                lines.append(f"  {source_name}: {data.metadata['url']}")

        lines.append("file_version: 1")
        lines.append("---")

        return "\n".join(lines)

    def _consolidate_biography(self, scraped_data: Dict[str, Any]) -> str:
        """Consolidate biography from multiple sources"""
        biographies = []

        # Prioritize Wikipedia
        if "wikipedia" in scraped_data and scraped_data["wikipedia"].success:
            bio = scraped_data["wikipedia"].biography
            if bio:
                biographies.append(bio)

        # Add IMSLP if available and different
        if "imslp" in scraped_data and scraped_data["imslp"].success:
            bio = scraped_data["imslp"].biography
            if bio and bio not in biographies:
                biographies.append(bio)

        # Add AllMusic if available
        if "allmusic" in scraped_data and scraped_data["allmusic"].success:
            bio = scraped_data["allmusic"].biography
            if bio and bio not in biographies:
                biographies.append(bio)

        return "\n\n".join(biographies)

    def _consolidate_style(self, scraped_data: Dict[str, Any]) -> str:
        """Consolidate musical style information"""
        styles = []

        for source_name in ["wikipedia", "allmusic", "imslp"]:
            if source_name in scraped_data and scraped_data[source_name].success:
                style = scraped_data[source_name].musical_style
                if style and style not in styles:
                    styles.append(style)

        return "\n\n".join(styles)

    def _consolidate_works(self, scraped_data: Dict[str, Any]) -> str:
        """Consolidate works lists"""
        all_works = []

        # Collect works from all sources
        for source_name in ["wikipedia", "imslp", "allmusic"]:
            if source_name in scraped_data and scraped_data[source_name].success:
                works = scraped_data[source_name].works
                if works:
                    all_works.extend(works)

        # Remove duplicates while preserving order
        seen = set()
        unique_works = []
        for work in all_works:
            if work not in seen:
                seen.add(work)
                unique_works.append(work)

        # Format as list
        if unique_works:
            return "\n".join([f"- {work}" for work in unique_works[:100]])

        return ""

    def _consolidate_legacy(self, scraped_data: Dict[str, Any]) -> str:
        """Consolidate legacy information"""
        legacies = []

        for source_name in ["wikipedia", "allmusic"]:
            if source_name in scraped_data and scraped_data[source_name].success:
                legacy = scraped_data[source_name].legacy
                if legacy and legacy not in legacies:
                    legacies.append(legacy)

        return "\n\n".join(legacies)

    def _generate_sources_section(self, scraped_data: Dict[str, Any]) -> str:
        """Generate sources section"""
        lines = []

        for source_name, data in scraped_data.items():
            if data.success:
                url = data.metadata.get("url", "")
                if url:
                    status = "✓"
                else:
                    status = "?"
                lines.append(f"{status} **{source_name.title()}**: {url or 'N/A'}")
            else:
                lines.append(f"✗ **{source_name.title()}**: Failed - {data.error}")

        lines.append(f"\n*Scraped on {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}*")

        return "\n".join(lines)


# Singleton instance
markdown_formatter = MarkdownFormatter()
