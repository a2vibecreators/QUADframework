"""
Intelligent Hook Integration
============================

Integrates all hook system components into a unified flow.

USE CASE:
---------
User presses Enter → Pre-hook waits for more input (pause detection)
→ If user types again, merge messages
→ Score importance with Gemini
→ Save to memory with shelf life
→ Send to QUAD API → Claude API

Patent Pending: Intelligent conversation buffering with adaptive timeout,
importance scoring, and hierarchical memory management

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import asyncio
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

from .pause_detector import get_pause_detector, PauseDetector
from .importance_scorer import get_importance_scorer, ImportanceScorer
from .memory_manager import get_memory_manager, MemoryManager
from .context_detector import get_context_detector, ContextDetector


class IntelligentHook:
    """
    Intelligent pre-hook that implements adaptive pause detection,
    importance scoring, memory management, and context tracking.

    FLOW:
    -----
    1. User types message and presses Enter
    2. Pre-hook WAITS (pause detection) to see if user types more
    3. If user types again within timeout, MERGE messages
    4. Score importance with Gemini (with pattern learning)
    5. If important enough (>= threshold), save to memory
    6. Send merged input to QUAD API (if configured)
    7. Return response to Claude
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize intelligent hook system.

        Args:
            config_path: Path to .quad/hook-config.json
        """
        self.config_path = config_path
        self.pause_detector: PauseDetector = get_pause_detector(config_path)
        self.importance_scorer: ImportanceScorer = get_importance_scorer(config_path)
        self.memory_manager: MemoryManager = get_memory_manager(config_path)
        self.context_detector: ContextDetector = get_context_detector(config_path)

        # User ID (TODO: get from authentication)
        self.user_id = "mock-user-id"

    async def process_user_input(
        self,
        user_input: str,
        command: str,
        args: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process user input with intelligent buffering.

        This is called by the pre-hook BEFORE command execution.

        Args:
            user_input: User's input text
            command: Command being executed
            args: Command arguments

        Returns:
            Processed context with merged input, importance score, etc.
        """
        print(f"\n[Intelligent Hook] Processing input for command: {command}")
        print(f"[Input] {user_input[:100]}...")

        # STEP 1: Add message to pause detector
        self.pause_detector.add_message(user_input)

        # STEP 2: Wait for pause timeout (adaptive)
        timeout_ms = self.pause_detector.calculate_timeout()
        print(f"[Pause Detection] Waiting {timeout_ms}ms for more input...")

        start_time = time.time()
        while True:
            elapsed_ms = (time.time() - start_time) * 1000

            if elapsed_ms >= timeout_ms:
                # Timeout reached, no more input coming
                break

            # Check if user added more input (in real implementation, this would be async)
            # For now, we'll simulate by checking buffer size
            # TODO: Implement async message queue

            await asyncio.sleep(0.5)  # Sleep 500ms, check again

        # STEP 3: Get merged input
        merged_input = self.pause_detector.get_merged_input()
        print(f"[Merged Input] {len(self.pause_detector.message_buffer)} messages merged")
        print(f"[Final Input] {merged_input[:100]}...")

        # STEP 4: Get active context
        context = self.context_detector.get_active_context(self.user_id)
        print(f"[Context] Type: {context.context_type}, ID: {context.context_id}, Weight: {context.weight}")

        # STEP 5: Score importance with Gemini
        project_name = context.project_name or "QUAD"
        current_work = f"Executing command: {command}"

        importance_score = await self.importance_scorer.score_importance(
            user_input=merged_input,
            project=project_name,
            current_work=current_work
        )

        print(f"[Importance] Score: {importance_score}/10")

        # STEP 6: Detect topic
        topic_detected = self.importance_scorer._detect_topic(merged_input)
        print(f"[Topic] {topic_detected}")

        # STEP 7: Save to memory if important enough
        should_save = self.importance_scorer.should_save_to_memory(importance_score)

        if should_save:
            memory = self.memory_manager.save_memory(
                user_id=self.user_id,
                project_name=project_name,
                context_type=context.context_type,
                context_id=context.context_id,
                user_input=merged_input,
                topic_detected=topic_detected,
                importance_score=importance_score,
                importance_suggested=importance_score,  # TODO: track Gemini's original suggestion
                importance_manual_override=False
            )
            print(f"[Memory] Saved with ID: {memory.id}")
        else:
            print(f"[Memory] Not saved (below threshold of {self.importance_scorer.config.get('threshold', 5)})")

        # STEP 8: Clear pause detector buffer
        self.pause_detector.clear_buffer()

        # STEP 9: Return enriched context
        return {
            'merged_input': merged_input,
            'original_input': user_input,
            'importance_score': importance_score,
            'topic_detected': topic_detected,
            'context': {
                'type': context.context_type,
                'id': context.context_id,
                'name': context.context_name,
                'project': project_name,
                'weight': context.weight
            },
            'memory_saved': should_save,
            'pause_timeout_ms': timeout_ms
        }

    async def send_to_quad_api(self, processed_context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Send processed context to QUAD API (optional).

        This could be used for centralized logging, analytics, or RAG enhancement.

        Args:
            processed_context: Processed context from process_user_input()

        Returns:
            QUAD API response if configured, None otherwise
        """
        # TODO: Implement QUAD API integration
        # POST /api/quad/hooks/pre-execution
        # Body: processed_context
        # Response: { suggestions, rag_context, etc. }

        return None

    def get_memory_context_for_claude(self, user_id: str) -> str:
        """
        Get relevant memory context to send to Claude.

        This is sent ALONG WITH the user's input to provide Claude with context.

        Args:
            user_id: User UUID

        Returns:
            Formatted memory context string
        """
        context = self.context_detector.get_active_context(user_id)

        memory_summary = self.memory_manager.get_context_summary(
            user_id=user_id,
            context_type=context.context_type,
            context_id=context.context_id
        )

        return memory_summary

    def handle_manual_importance_adjustment(
        self,
        original_score: int,
        adjusted_score: int,
        user_input: str
    ):
        """
        Handle user's manual importance adjustment (for learning).

        This is called when user manually adjusts the importance score.

        Args:
            original_score: Original score from Gemini
            adjusted_score: User's adjusted score
            user_input: User's input text
        """
        self.importance_scorer.record_adjustment(
            gemini_score=original_score,
            user_score=adjusted_score,
            user_input=user_input
        )

    def get_system_stats(self) -> Dict[str, Any]:
        """Get statistics from all subsystems"""
        return {
            'pause_detector': self.pause_detector.get_pattern_info(),
            'importance_scorer': self.importance_scorer.get_stats(),
            'memory_manager': self.memory_manager.get_stats(),
            'context_detector': self.context_detector.get_stats()
        }


# Global intelligent hook instance
_intelligent_hook: Optional[IntelligentHook] = None


def get_intelligent_hook(config_path: Optional[Path] = None) -> IntelligentHook:
    """Get singleton intelligent hook instance"""
    global _intelligent_hook
    if _intelligent_hook is None:
        _intelligent_hook = IntelligentHook(config_path)
    return _intelligent_hook


# ============================================================================
# Example Usage in Pre-Hook
# ============================================================================

async def example_pre_hook(command: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Example integration with existing pre-hook.

    FLOW:
    -----
    1. User types: "create a function" [Enter]
    2. Pre-hook waits 3 seconds (pause detection)
    3. User types: "to calculate sum" [Enter] (within 3 seconds)
    4. Pre-hook merges: "create a function\nto calculate sum"
    5. Scores importance (e.g., 7/10)
    6. Saves to memory
    7. Sends to QUAD API (optional)
    8. Returns to Claude with enriched context
    """
    # Get user input (from command args or stdin)
    user_input = args.get('user_input', '')

    # Process with intelligent hook
    hook = get_intelligent_hook()
    processed_context = await hook.process_user_input(user_input, command, args)

    # Get memory context for Claude
    memory_context = hook.get_memory_context_for_claude(hook.user_id)

    # Optionally send to QUAD API
    quad_response = await hook.send_to_quad_api(processed_context)

    # Return enriched context to command
    return {
        **processed_context,
        'memory_context': memory_context,
        'quad_api_response': quad_response
    }


# ============================================================================
# CLI Commands for Context Management
# ============================================================================

def cli_ticket_start(ticket_id: str, title: str, project_name: str):
    """CLI command: quad ticket start <ticket-id>"""
    hook = get_intelligent_hook()
    hook.context_detector.start_ticket(hook.user_id, ticket_id, title, project_name)


def cli_ticket_pause():
    """CLI command: quad ticket pause"""
    hook = get_intelligent_hook()
    if hook.context_detector.active_context and hook.context_detector.active_context.context_type == 'ticket':
        ticket_id = hook.context_detector.active_context.context_id
        hook.context_detector.pause_ticket(ticket_id)
    else:
        print("[Error] No active ticket to pause")


def cli_ticket_resume(ticket_id: str):
    """CLI command: quad ticket resume <ticket-id>"""
    hook = get_intelligent_hook()
    hook.context_detector.resume_ticket(hook.user_id, ticket_id)


def cli_project_init(project_name: str):
    """CLI command: quad init <project-name>"""
    hook = get_intelligent_hook()
    hook.context_detector.init_project(hook.user_id, project_name)


def cli_stats():
    """CLI command: quad stats"""
    hook = get_intelligent_hook()
    stats = hook.get_system_stats()

    print("\n=== QUAD Hook System Statistics ===\n")

    print("Pause Detector:")
    print(f"  Current timeout: {stats['pause_detector']['current_timeout']}ms")
    print(f"  Burst mode: {stats['pause_detector']['is_burst_mode']}")
    print(f"  Long thought mode: {stats['pause_detector']['is_long_thought_mode']}")
    print(f"  Buffer size: {stats['pause_detector']['buffer_size']}")

    print("\nImportance Scorer:")
    print(f"  Adjustments learned: {stats['importance_scorer']['adjustment_history_count']}")
    print(f"  Topics learned: {stats['importance_scorer']['topics_learned']}")

    print("\nMemory Manager:")
    print(f"  Total memories: {stats['memory_manager']['total_memories']}")
    print(f"  Active memories: {stats['memory_manager']['active_memories']}")
    print(f"  Expired memories: {stats['memory_manager']['expired_memories']}")
    print(f"  By category: {stats['memory_manager']['by_category']}")

    print("\nContext Detector:")
    print(f"  Active context: {stats['context_detector']['active_context']}")

    print("\n" + "="*40 + "\n")
