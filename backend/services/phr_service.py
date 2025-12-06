"""
Prompt History Record (PHR) Service

This service manages the storage and retrieval of Prompt History Records (PHRs)
as defined in the project's architecture.
"""

import os
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class Stage(Enum):
    """PHR stages as defined in the project"""
    CONSTITUTION = "constitution"
    SPEC = "spec"
    PLAN = "plan"
    TASKS = "tasks"
    RED = "red"
    GREEN = "green"
    REFACTOR = "refactor"
    EXPLAINER = "explainer"
    MISC = "misc"
    GENERAL = "general"

@dataclass
class PHRMetadata:
    """Metadata for a PHR"""
    id: str
    title: str
    stage: Stage
    date_iso: str
    surface: str
    model: str
    feature: str
    branch: str
    user: str
    command: str
    labels: List[str]
    links: Dict[str, str]
    files_yaml: List[str]
    tests_yaml: List[str]

@dataclass
class PHRContent:
    """Content of a PHR"""
    prompt_text: str
    response_text: str
    outcome: Optional[str] = None
    evaluation: Optional[str] = None

@dataclass
class PHR:
    """Complete Prompt History Record"""
    metadata: PHRMetadata
    content: PHRContent

class PHRService:
    """Service for managing PHRs"""

    def __init__(self, base_path: str = None):
        if base_path is None:
            base_path = Path(__file__).parent.parent.parent
        self.base_path = Path(base_path)
        self.phr_path = self.base_path / "history" / "prompts"

    def get_phr_directory(self, stage: Stage, feature: str = None) -> Path:
        """Get the directory for storing PHRs based on stage and feature"""
        if stage == Stage.CONSTITUTION:
            return self.phr_path / "constitution"
        elif stage == Stage.GENERAL:
            return self.phr_path / "general"
        elif feature:
            return self.phr_path / feature
        else:
            return self.phr_path

    def generate_phr_filename(self, stage: Stage, title: str, feature: str = None) -> str:
        """Generate a filename for a PHR"""
        # Create slug from title
        slug = title.lower().replace(" ", "-").replace("/", "-")[:30]
        slug = "".join(c if c.isalnum() or c == "-" else "" for c in slug)

        # Get next ID
        directory = self.get_phr_directory(stage, feature)
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)

        existing_files = list(directory.glob("*.prompt.md"))
        max_id = 0
        for f in existing_files:
            try:
                id_part = f.name.split("-")[0]
                if id_part.isdigit():
                    max_id = max(max_id, int(id_part))
            except:
                continue

        new_id = max_id + 1
        return f"{new_id:04d}-{slug}.{stage.value}.prompt.md"

    def create_phr(
        self,
        title: str,
        stage: Stage,
        prompt_text: str,
        response_text: str,
        surface: str = "agent",
        model: str = "claude-3-opus",
        feature: str = "none",
        branch: str = "main",
        user: str = "user",
        command: str = "",
        labels: List[str] = None,
        links: Dict[str, str] = None,
        files_yaml: List[str] = None,
        tests_yaml: List[str] = None,
        outcome: str = None,
        evaluation: str = None
    ) -> str:
        """Create a new PHR and return the file path"""

        # Generate ID and filename
        filename = self.generate_phr_filename(stage, title, feature)
        directory = self.get_phr_directory(stage, feature)
        file_path = directory / filename

        # Extract ID from filename
        phr_id = filename.split("-")[0]

        # Create metadata
        metadata = PHRMetadata(
            id=phr_id,
            title=title,
            stage=stage,
            date_iso=datetime.now().isoformat(),
            surface=surface,
            model=model,
            feature=feature,
            branch=branch,
            user=user,
            command=command,
            labels=labels or [],
            links=links or {},
            files_yaml=files_yaml or [],
            tests_yaml=tests_yaml or []
        )

        # Create content
        content = PHRContent(
            prompt_text=prompt_text,
            response_text=response_text,
            outcome=outcome,
            evaluation=evaluation
        )

        # Create PHR
        phr = PHR(metadata=metadata, content=content)

        # Write to file
        self._write_phr_to_file(file_path, phr)

        return str(file_path)

    def _write_phr_to_file(self, file_path: Path, phr: PHR):
        """Write PHR to markdown file"""

        # YAML frontmatter
        frontmatter = {
            "ID": phr.metadata.id,
            "TITLE": phr.metadata.title,
            "STAGE": phr.metadata.stage.value,
            "DATE_ISO": phr.metadata.date_iso,
            "SURFACE": phr.metadata.surface,
            "MODEL": phr.metadata.model,
            "FEATURE": phr.metadata.feature,
            "BRANCH": phr.metadata.branch,
            "USER": phr.metadata.user,
            "COMMAND": phr.metadata.command,
            "LABELS": phr.metadata.labels,
            "LINKS": {
                "SPEC": phr.metadata.links.get("spec", "null"),
                "TICKET": phr.metadata.links.get("ticket", "null"),
                "ADR": phr.metadata.links.get("adr", "null"),
                "PR": phr.metadata.links.get("pr", "null")
            },
            "FILES_YAML": "\n".join(f" - {f}" for f in phr.metadata.files_yaml),
            "TESTS_YAML": "\n".join(f" - {t}" for t in phr.metadata.tests_yaml),
            "PROMPT_TEXT": phr.content.prompt_text,
            "RESPONSE_TEXT": phr.content.response_text,
            "OUTCOME": phr.content.outcome or "",
            "EVALUATION": phr.content.evaluation or ""
        }

        # Write markdown file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("---\n")
            yaml.dump(frontmatter, f, default_flow_style=False, allow_unicode=True)
            f.write("---\n\n")

    def load_phr(self, file_path: str) -> Optional[PHR]:
        """Load a PHR from file"""
        try:
            file_path = Path(file_path)

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse YAML frontmatter
            if content.startswith('---\n'):
                parts = content.split('---\n', 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1])

                    # Reconstruct metadata
                    metadata = PHRMetadata(
                        id=frontmatter.get("ID", ""),
                        title=frontmatter.get("TITLE", ""),
                        stage=Stage(frontmatter.get("STAGE", "general")),
                        date_iso=frontmatter.get("DATE_ISO", ""),
                        surface=frontmatter.get("SURFACE", "agent"),
                        model=frontmatter.get("MODEL", "claude-3-opus"),
                        feature=frontmatter.get("FEATURE", "none"),
                        branch=frontmatter.get("BRANCH", "main"),
                        user=frontmatter.get("USER", "user"),
                        command=frontmatter.get("COMMAND", ""),
                        labels=frontmatter.get("LABELS", []),
                        links=frontmatter.get("LINKS", {}),
                        files_yaml=frontmatter.get("FILES_YAML", "").split("\n")[1:],
                        tests_yaml=frontmatter.get("TESTS_YAML", "").split("\n")[1:]
                    )

                    # Reconstruct content
                    content_data = PHRContent(
                        prompt_text=frontmatter.get("PROMPT_TEXT", ""),
                        response_text=frontmatter.get("RESPONSE_TEXT", ""),
                        outcome=frontmatter.get("OUTCOME"),
                        evaluation=frontmatter.get("EVALUATION")
                    )

                    return PHR(metadata=metadata, content=content_data)

            return None
        except Exception as e:
            print(f"Error loading PHR: {e}")
            return None

    def list_phrs(self, stage: Stage = None, feature: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """List PHRs with optional filtering"""
        phrs = []

        if stage == Stage.CONSTITUTION:
            directory = self.phr_path / "constitution"
        elif stage == Stage.GENERAL:
            directory = self.phr_path / "general"
        elif feature:
            directory = self.phr_path / feature
        else:
            # List all PHRs
            directories = [d for d in self.phr_path.iterdir() if d.is_dir()]
            for directory in directories:
                phrs.extend(self._list_phrs_in_directory(directory, limit))
            return sorted(phrs, key=lambda x: x.get("date_iso", ""), reverse=True)[:limit]

        if directory.exists():
            phrs = self._list_phrs_in_directory(directory, limit)

        return sorted(phrs, key=lambda x: x.get("date_iso", ""), reverse=True)[:limit]

    def _list_phrs_in_directory(self, directory: Path, limit: int) -> List[Dict[str, Any]]:
        """List PHRs in a specific directory"""
        phrs = []

        for file_path in directory.glob("*.prompt.md"):
            try:
                phr = self.load_phr(file_path)
                if phr:
                    phrs.append({
                        "id": phr.metadata.id,
                        "title": phr.metadata.title,
                        "stage": phr.metadata.stage.value,
                        "date_iso": phr.metadata.date_iso,
                        "feature": phr.metadata.feature,
                        "file_path": str(file_path),
                        "preview": phr.content.prompt_text[:100] + "..." if len(phr.content.prompt_text) > 100 else phr.content.prompt_text
                    })
            except Exception as e:
                print(f"Error loading PHR {file_path}: {e}")

        return phrs[:limit]

    def search_phrs(self, query: str, stage: Stage = None, feature: str = None) -> List[Dict[str, Any]]:
        """Search PHRs by content"""
        results = []

        phrs = self.list_phrs(stage, feature, limit=1000)

        query_lower = query.lower()

        for phr in phrs:
            # Load full PHR for content search
            full_phr = self.load_phr(phr["file_path"])
            if full_phr:
                # Search in title, prompt, and response
                if (query_lower in full_phr.metadata.title.lower() or
                    query_lower in full_phr.content.prompt_text.lower() or
                    query_lower in full_phr.content.response_text.lower() or
                    any(query_lower in label.lower() for label in full_phr.metadata.labels)):
                    results.append(phr)

        return results[:50]  # Limit search results