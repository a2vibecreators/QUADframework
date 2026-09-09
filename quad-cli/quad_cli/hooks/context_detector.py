"""
Context Detection Module
========================

Detects and manages context switching (ticket → project → user).
Implements hierarchical context priority with auto-detection.

Patent Pending: Hierarchical context switching with automatic detection

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import json
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
import uuid


@dataclass
class Context:
    """Context information"""
    context_type: str  # 'ticket', 'project', 'user', 'global'
    context_id: str
    context_name: str
    project_name: Optional[str]
    weight: float  # Priority weight
    started_at: str
    is_active: bool


class ContextDetector:
    """
    Detects and manages hierarchical context switching.

    Priority: ticket (2.0) > project (1.0) > user (0.5)
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize context detector.

        Args:
            config_path: Path to .quad/hook-config.json
        """
        self.config_path = config_path or Path.home() / ".quad" / "hook-config.json"
        self.config = self._load_config()

        # Current active context
        self.active_context: Optional[Context] = None

        # Context stack
        self.context_stack: List[Context] = []

    def _load_config(self) -> Dict[str, Any]:
        """Load context detection configuration"""
        if not self.config_path.exists():
            return self._get_default_config()

        with open(self.config_path, 'r') as f:
            config = json.load(f)
            return config.get('contextDetection', self._get_default_config())

    def _get_default_config(self) -> Dict[str, Any]:
        """Default context detection configuration"""
        return {
            "enabled": True,
            "mode": "auto",
            "hierarchy": {
                "priority": ["ticket", "project", "user"],
                "weights": {
                    "ticket": 2.0,
                    "project": 1.0,
                    "user": 0.5
                }
            },
            "ticket": {
                "enabled": True,
                "activeThresholdMinutes": 30
            },
            "project": {
                "enabled": True,
                "autoDetectFromPath": True
            },
            "contextSwitchDetection": {
                "enabled": True,
                "keywords": {
                    "newProject": ["switch to", "work on", "let's start"],
                    "newTicket": ["ticket", "bug", "issue", "feature"],
                    "resume": ["continue", "back to", "resume"]
                }
            }
        }

    def get_active_context(self, user_id: str) -> Context:
        """
        Get user's current active context.

        Priority: ticket > project > user

        Args:
            user_id: User UUID

        Returns:
            Active context
        """
        if not self.config.get('enabled', True):
            return self._get_user_context(user_id)

        # Check for active ticket (highest priority)
        ticket_context = self._get_active_ticket_context(user_id)
        if ticket_context:
            self.active_context = ticket_context
            return ticket_context

        # Check for active project (medium priority)
        project_context = self._get_active_project_context(user_id)
        if project_context:
            self.active_context = project_context
            return project_context

        # Fallback to user context (lowest priority)
        user_context = self._get_user_context(user_id)
        self.active_context = user_context
        return user_context

    def _get_active_ticket_context(self, user_id: str) -> Optional[Context]:
        """Get active ticket context if exists"""
        if not self.config.get('ticket', {}).get('enabled', True):
            return None

        # TODO: Query database for active ticket
        # SELECT * FROM quad_tickets
        # WHERE user_id = ? AND status = 'in_progress'
        # AND last_active_at > NOW() - INTERVAL '30 minutes'

        # For now, return None (no active ticket)
        return None

    def _get_active_project_context(self, user_id: str) -> Optional[Context]:
        """Get active project context if exists"""
        if not self.config.get('project', {}).get('enabled', True):
            return None

        # TODO: Query database for active project
        # SELECT * FROM quad_hook_context_history
        # WHERE user_id = ? AND context_type = 'project' AND is_active = TRUE

        # For now, auto-detect from working directory
        if self.config.get('project', {}).get('autoDetectFromPath', True):
            project_name = self._detect_project_from_path()
            if project_name:
                return Context(
                    context_type='project',
                    context_id=project_name,
                    context_name=project_name,
                    project_name=project_name,
                    weight=self.config['hierarchy']['weights']['project'],
                    started_at=datetime.now().isoformat(),
                    is_active=True
                )

        return None

    def _detect_project_from_path(self) -> Optional[str]:
        """Detect project name from current working directory"""
        cwd = Path.cwd()

        # Check for .quad directory
        quad_dir = cwd / ".quad"
        if quad_dir.exists():
            return cwd.name

        # Check parent directories
        for parent in cwd.parents:
            quad_dir = parent / ".quad"
            if quad_dir.exists():
                return parent.name

        return None

    def _get_user_context(self, user_id: str) -> Context:
        """Get user context (fallback)"""
        return Context(
            context_type='user',
            context_id=user_id,
            context_name='User Context',
            project_name=None,
            weight=self.config['hierarchy']['weights']['user'],
            started_at=datetime.now().isoformat(),
            is_active=True
        )

    def detect_context_switch(self, user_input: str) -> Optional[Tuple[str, str]]:
        """
        Detect if user is switching context from input text.

        Args:
            user_input: User's input text

        Returns:
            Tuple of (context_type, context_name) if switch detected, None otherwise
        """
        if not self.config.get('contextSwitchDetection', {}).get('enabled', True):
            return None

        keywords = self.config['contextSwitchDetection']['keywords']
        user_input_lower = user_input.lower()

        # Check for new project
        for keyword in keywords.get('newProject', []):
            if keyword in user_input_lower:
                # Extract project name (simple heuristic)
                words = user_input.split()
                keyword_index = next((i for i, w in enumerate(words) if w.lower().startswith(keyword.split()[0])), -1)
                if keyword_index >= 0 and keyword_index + len(keyword.split()) < len(words):
                    project_name = words[keyword_index + len(keyword.split())]
                    return ('project', project_name)

        # Check for new ticket
        for keyword in keywords.get('newTicket', []):
            if keyword in user_input_lower:
                # Extract ticket ID (e.g., "SQUAD-123")
                words = user_input.split()
                for word in words:
                    if '-' in word and any(c.isdigit() for c in word):
                        return ('ticket', word)

        # Check for resume
        for keyword in keywords.get('resume', []):
            if keyword in user_input_lower:
                # Try to extract what to resume
                words = user_input.split()
                keyword_index = next((i for i, w in enumerate(words) if keyword in w.lower()), -1)
                if keyword_index >= 0 and keyword_index + 1 < len(words):
                    resume_target = words[keyword_index + 1]
                    return ('resume', resume_target)

        return None

    def start_ticket(self, user_id: str, ticket_id: str, title: str, project_name: str):
        """
        Start working on a ticket.

        Args:
            user_id: User UUID
            ticket_id: Ticket ID (e.g., "SQUAD-123")
            title: Ticket title
            project_name: Project name
        """
        context = Context(
            context_type='ticket',
            context_id=ticket_id,
            context_name=title,
            project_name=project_name,
            weight=self.config['hierarchy']['weights']['ticket'],
            started_at=datetime.now().isoformat(),
            is_active=True
        )

        # TODO: Insert into database (quad_tickets, quad_hook_context_history)

        # Update active context
        self.active_context = context
        self.context_stack.append(context)

        print(f"[Context] Started ticket: {ticket_id} - {title}")

    def pause_ticket(self, ticket_id: str):
        """
        Pause working on a ticket.

        Args:
            ticket_id: Ticket ID
        """
        # TODO: Update database
        # UPDATE quad_tickets SET status = 'paused', paused_at = NOW() WHERE ticket_id = ?

        # Update context
        if self.active_context and self.active_context.context_id == ticket_id:
            self.active_context.is_active = False

        print(f"[Context] Paused ticket: {ticket_id}")

    def resume_ticket(self, user_id: str, ticket_id: str):
        """
        Resume working on a ticket.

        Args:
            user_id: User UUID
            ticket_id: Ticket ID
        """
        # TODO: Update database
        # UPDATE quad_tickets SET status = 'in_progress', resumed_at = NOW() WHERE ticket_id = ?

        # TODO: Load ticket context from database

        print(f"[Context] Resumed ticket: {ticket_id}")

    def init_project(self, user_id: str, project_name: str):
        """
        Initialize project context.

        Args:
            user_id: User UUID
            project_name: Project name
        """
        context = Context(
            context_type='project',
            context_id=project_name,
            context_name=project_name,
            project_name=project_name,
            weight=self.config['hierarchy']['weights']['project'],
            started_at=datetime.now().isoformat(),
            is_active=True
        )

        # TODO: Insert into database (quad_hook_context_history)

        # Update active context
        self.active_context = context
        self.context_stack.append(context)

        print(f"[Context] Initialized project: {project_name}")

    def get_context_for_memory(self, user_id: str) -> Tuple[str, Optional[str]]:
        """
        Get context for saving memory.

        Args:
            user_id: User UUID

        Returns:
            Tuple of (context_type, context_id)
        """
        context = self.get_active_context(user_id)
        return (context.context_type, context.context_id)

    def get_stats(self) -> Dict[str, Any]:
        """Get context statistics"""
        return {
            'config': self.config,
            'active_context': asdict(self.active_context) if self.active_context else None,
            'context_stack_size': len(self.context_stack)
        }


# Global context detector instance
_context_detector: Optional[ContextDetector] = None


def get_context_detector(config_path: Optional[Path] = None) -> ContextDetector:
    """Get singleton context detector instance"""
    global _context_detector
    if _context_detector is None:
        _context_detector = ContextDetector(config_path)
    return _context_detector
