#!/usr/bin/env python3
"""
Sync .ai/context.md to tool-specific files.

Output:
  Cursor:
    - AGENTS.md: Project context only
    - .cursor/rules/*.mdc: Agent rules (loaded on-demand by globs/description)
    - .cursor/commands/*.md: Slash commands (invoked with /)

  GitHub Copilot:
    - AGENTS.md: Project context (shared with Cursor)
    - .github/prompts/*.prompt.md: Prompts (invoked with /name)

  Claude Code:
    - CLAUDE.md: Project context only
    - .claude/commands/*.md: Slash commands (/project:name)
    - .claude/agents/*.md: Subagents (invoked via Task tool)
"""

import re
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# =============================================================================
# Domain Models
# =============================================================================


@dataclass
class Frontmatter:
    """Parsed YAML frontmatter."""

    type: str = ""
    name: str = ""
    description: str = ""
    triggers: list[str] = field(default_factory=list)
    usage: list[str] = field(default_factory=list)
    globs: str = ""


@dataclass
class SourceItem:
    """Agent or command item with metadata."""

    path: Path
    frontmatter: Frontmatter
    body: str

    @property
    def stem(self) -> str:
        return self.path.stem

    @property
    def name(self) -> str:
        return self.path.name


# =============================================================================
# Frontmatter Utilities
# =============================================================================


def parse_frontmatter(content: str) -> tuple[Optional[Frontmatter], str]:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return None, content

    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", content, re.DOTALL)
    if not match:
        return None, content

    yaml_str, body = match.groups()
    fm = Frontmatter()
    current_key = None
    current_list = []

    for line in yaml_str.split("\n"):
        if re.match(r"^\s+-\s+", line):
            current_list.append(re.sub(r"^\s+-\s+", "", line))
            continue

        kv_match = re.match(r"^(\w+):\s*(.*)$", line)
        if kv_match:
            if current_key and current_list:
                setattr(fm, current_key, current_list)
                current_list = []

            key, value = kv_match.groups()
            current_key = key
            if value:
                setattr(fm, key, value)

    if current_key and current_list:
        setattr(fm, current_key, current_list)

    return fm, body.lstrip("\n")


def build_frontmatter(fields: dict[str, str]) -> str:
    """Build YAML frontmatter string from key-value pairs."""
    if not fields:
        return ""
    lines = ["---"]
    for key, value in fields.items():
        if value:
            lines.append(f"{key}: {value}")
    lines.append("---\n\n")
    return "\n".join(lines)


# =============================================================================
# File Operations
# =============================================================================


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def load_markdown_files(directory: Path, exclude: list[str] = None) -> list[Path]:
    """Load markdown files from directory, excluding specified names."""
    exclude = exclude or []
    if not directory.exists():
        return []
    return sorted(f for f in directory.glob("*.md") if f.name not in exclude)


# =============================================================================
# Source Loader
# =============================================================================


class SourceLoader:
    """Loads agents and commands from .ai directory."""

    def __init__(self, base_dir: Path):
        self.agents_dir = base_dir / ".ai" / "agents"
        self.commands_dir = base_dir / ".ai" / "commands"

    def load_agents(self) -> list[SourceItem]:
        return self._load_items(self.agents_dir, exclude=["_index.md"])

    def load_commands(self) -> list[SourceItem]:
        return self._load_items(self.commands_dir)

    def _load_items(self, directory: Path, exclude: list[str] = None) -> list[SourceItem]:
        items = []
        for path in load_markdown_files(directory, exclude):
            content = read_file(path)
            fm, body = parse_frontmatter(content)
            if fm is None:
                fm = Frontmatter(name=path.stem)
            items.append(SourceItem(path=path, frontmatter=fm, body=body))
        return items


# =============================================================================
# Tool Writers (Strategy Pattern)
# =============================================================================


class ToolWriter(ABC):
    """Base class for tool-specific file writers."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    @property
    @abstractmethod
    def name(self) -> str:
        """Tool display name."""
        pass

    @abstractmethod
    def write(self, context: str, agents: list[SourceItem], commands: list[SourceItem]) -> list[str]:
        """Write files and return list of output descriptions."""
        pass


class CursorWriter(ToolWriter):
    """Writes Cursor-specific files."""

    @property
    def name(self) -> str:
        return "Cursor"

    def write(self, context: str, agents: list[SourceItem], commands: list[SourceItem]) -> list[str]:
        outputs = []
        outputs.extend(self._write_rules(agents))
        outputs.extend(self._write_commands(commands))
        return outputs

    def _write_rules(self, agents: list[SourceItem]) -> list[str]:
        if not agents:
            return []

        rules_dir = self.base_dir / ".cursor" / "rules"
        for item in agents:
            content = self._build_rule_content(item)
            write_file(rules_dir / f"{item.stem}.mdc", content)

        return [f".cursor/rules/ ({len(agents)} rules)"]

    def _build_rule_content(self, item: SourceItem) -> str:
        fm = item.frontmatter
        fields = {"globs": fm.globs, "alwaysApply": "false", "description": fm.description}
        return build_frontmatter(fields) + item.body

    def _write_commands(self, commands: list[SourceItem]) -> list[str]:
        if not commands:
            return []

        cmds_dir = self.base_dir / ".cursor" / "commands"
        for item in commands:
            write_file(cmds_dir / item.name, item.body)

        return [f".cursor/commands/ ({len(commands)} commands)"]


class CopilotWriter(ToolWriter):
    """Writes GitHub Copilot-specific files."""

    @property
    def name(self) -> str:
        return "GitHub Copilot"

    def write(self, context: str, agents: list[SourceItem], commands: list[SourceItem]) -> list[str]:
        outputs = []
        outputs.extend(self._write_context(context))
        outputs.extend(self._write_prompts(agents, commands))
        return outputs

    def _write_context(self, context: str) -> list[str]:
        write_file(self.base_dir / "AGENTS.md", context)
        return ["AGENTS.md"]

    def _write_prompts(self, agents: list[SourceItem], commands: list[SourceItem]) -> list[str]:
        prompts_dir = self.base_dir / ".github" / "prompts"
        count = 0

        for item in agents:
            content = self._build_prompt(item.frontmatter.description, item.body)
            write_file(prompts_dir / f"{item.stem}.prompt.md", content)
            count += 1

        for item in commands:
            content = self._build_prompt(item.frontmatter.description, item.body)
            write_file(prompts_dir / f"{item.stem}.prompt.md", content)
            count += 1

        if count:
            return [f".github/prompts/ ({count} prompts)"]
        return []

    def _build_prompt(self, description: str, body: str) -> str:
        fields = {"mode": "'agent'", "description": f"'{description}'" if description else ""}
        return build_frontmatter(fields) + body


class ClaudeWriter(ToolWriter):
    """Writes Claude Code-specific files."""

    @property
    def name(self) -> str:
        return "Claude Code"

    def write(self, context: str, agents: list[SourceItem], commands: list[SourceItem]) -> list[str]:
        outputs = []
        outputs.extend(self._write_context(context))
        outputs.extend(self._write_commands(commands))
        outputs.extend(self._write_agents(agents))
        return outputs

    def _write_context(self, context: str) -> list[str]:
        write_file(self.base_dir / "CLAUDE.md", context)
        return ["CLAUDE.md"]

    def _write_commands(self, commands: list[SourceItem]) -> list[str]:
        if not commands:
            return []

        cmds_dir = self.base_dir / ".claude" / "commands"
        for item in commands:
            fields = {"description": item.frontmatter.description}
            content = build_frontmatter(fields) + item.body
            write_file(cmds_dir / item.name, content)

        return [f".claude/commands/ ({len(commands)} commands)"]

    def _write_agents(self, agents: list[SourceItem]) -> list[str]:
        if not agents:
            return []

        agents_dir = self.base_dir / ".claude" / "agents"
        for item in agents:
            agent_name = item.stem.lower().replace("_", "-")
            fields = {"name": agent_name, "description": item.frontmatter.description}
            content = build_frontmatter(fields) + item.body
            write_file(agents_dir / item.name, content)

        return [f".claude/agents/ ({len(agents)} agents)"]


# =============================================================================
# Context Syncer (Orchestrator)
# =============================================================================


class ContextSyncer:
    """Orchestrates context synchronization to various AI tools."""

    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or Path.cwd()
        self.source_path = self.base_dir / ".ai" / "context.md"
        self.loader = SourceLoader(self.base_dir)
        self.writers: list[ToolWriter] = [
            CursorWriter(self.base_dir),
            CopilotWriter(self.base_dir),
            ClaudeWriter(self.base_dir),
        ]

    def sync(self) -> bool:
        if not self.source_path.exists():
            print(f"Error: {self.source_path} not found", file=sys.stderr)
            return False

        context = read_file(self.source_path)
        agents = self.loader.load_agents()
        commands = self.loader.load_commands()

        all_outputs = []
        for writer in self.writers:
            all_outputs.extend(writer.write(context, agents, commands))

        print("Synced: " + ", ".join(all_outputs))
        return True


# =============================================================================
# Entry Point
# =============================================================================


def main():
    syncer = ContextSyncer()
    success = syncer.sync()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
