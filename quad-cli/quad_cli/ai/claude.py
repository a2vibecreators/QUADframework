"""
Claude API Wrapper
==================

Anthropic Claude AI integration for QUAD.

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import json
from typing import Dict, Any, Optional


class ClaudeAPI:
    """Wrapper for Anthropic Claude API"""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4"):
        """
        Initialize Claude API.

        Args:
            api_key: Anthropic API key
            model: Model name (claude-sonnet-4, claude-opus-4, etc.)
        """
        self.api_key = api_key
        self.model = model
        self._client = None

    def _get_client(self):
        """Lazy load Claude client"""
        if self._client is None:
            try:
                import anthropic
                self._client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                raise ImportError(
                    "anthropic library not installed. "
                    "Install with: pip install anthropic"
                )
        return self._client

    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 4096) -> str:
        """
        Generate text with Claude.

        Args:
            prompt: The prompt to send
            temperature: Creativity (0.0-1.0)
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text
        """
        client = self._get_client()

        try:
            response = client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return response.content[0].text

        except Exception as e:
            raise Exception(f"Claude API error: {e}")

    def generate_json(self, prompt: str, temperature: float = 0.7) -> Dict:
        """
        Generate JSON response with Claude.

        Args:
            prompt: The prompt (should ask for JSON)
            temperature: Creativity

        Returns:
            Parsed JSON dict
        """
        # Add JSON instruction to prompt
        json_prompt = f"{prompt}\n\nIMPORTANT: Return ONLY valid JSON, no explanation."

        response_text = self.generate(json_prompt, temperature)

        # Claude usually returns clean JSON, but let's be safe
        try:
            # Try direct parse first
            return json.loads(response_text)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown
            import re
            json_pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
            match = re.search(json_pattern, response_text)

            if match:
                try:
                    return json.loads(match.group(1))
                except:
                    pass

            # If all fails, return error
            return {
                "error": "Failed to parse JSON response",
                "raw_response": response_text
            }

    def analyze_context(
        self,
        command: str,
        args: Dict[str, Any],
        result: Any
    ) -> Dict[str, Any]:
        """
        Analyze command execution context.

        This is used by post-hook to extract learnings.

        Args:
            command: Command name (story, code, init, etc.)
            args: Command arguments
            result: Command result

        Returns:
            {
                "topics": ["finance", "project"],
                "decisions": [{type: "...", value: "..."}],
                "preferences": [{type: "...", value: "..."}],
                "memory": {...}
            }
        """
        prompt = f"""
You are analyzing a QUAD command execution to extract important context.

Command: {command}
Arguments: {json.dumps(args, indent=2)}
Result: {json.dumps(str(result)[:1000], indent=2)}  # Truncate long results

Your task: Extract structured information for future reference.

Analyze and extract:

1. **Topics** - Which context categories apply?
   Options: project, health, finance, preferences, memory
   Examples:
   - "banking app" → finance, project
   - "fitness tracker" → health, project
   - "user prefers React" → preferences

2. **Decisions** - Technical decisions made
   Examples:
   - {{"type": "tech_stack", "value": "Spring Boot"}}
   - {{"type": "authentication", "value": "JWT"}}
   - {{"type": "database", "value": "PostgreSQL"}}

3. **Preferences** - User's coding preferences
   Examples:
   - {{"type": "framework", "value": "React", "frequency": 1}}
   - {{"type": "style", "value": "TypeScript over JavaScript"}}

4. **Memory** - Important information to remember
   Any other relevant context that doesn't fit above categories.

Return ONLY valid JSON in this exact format:
{{
  "topics": ["topic1", "topic2"],
  "decisions": [
    {{"type": "category", "value": "decision"}}
  ],
  "preferences": [
    {{"type": "category", "value": "preference"}}
  ],
  "memory": {{
    "key": "value"
  }}
}}

Do NOT include explanations, only the JSON object.
"""

        try:
            result = self.generate_json(prompt, temperature=0.3)  # Lower temp for structured output
            return result
        except Exception as e:
            # Fallback to empty structure
            return {
                "topics": [],
                "decisions": [],
                "preferences": [],
                "memory": {},
                "error": str(e)
            }

    def estimate_confidence(self, response: str) -> float:
        """
        Estimate confidence in Claude's response.

        Claude is generally very confident, so this returns high values.

        Args:
            response: Generated response text

        Returns:
            Confidence score (0.0-1.0)
        """
        # Claude is typically very accurate
        # We'll use simple heuristics

        response_lower = response.lower()

        # Check for explicit uncertainty
        if any(marker in response_lower for marker in [
            "i'm not sure", "i don't know", "unclear", "uncertain"
        ]):
            return 0.85

        # Check for hedging language
        if any(marker in response_lower for marker in [
            "might", "possibly", "probably", "perhaps"
        ]):
            return 0.90

        # Default: High confidence
        return 0.95


def test_claude():
    """Test Claude API (for development)"""
    import os

    api_key = os.environ.get("CLAUDE_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Set CLAUDE_API_KEY or ANTHROPIC_API_KEY environment variable to test")
        return

    claude = ClaudeAPI(api_key)

    # Test 1: Simple generation
    print("Test 1: Simple generation")
    response = claude.generate("What is an API in simple terms?")
    print(f"Response: {response[:200]}...")
    print(f"Confidence: {claude.estimate_confidence(response)}")
    print()

    # Test 2: JSON generation
    print("Test 2: JSON generation")
    result = claude.generate_json("""
    List 3 programming languages with their use cases.
    Return as JSON array: [{"language": "...", "use_case": "..."}]
    """)
    print(f"Result: {json.dumps(result, indent=2)}")
    print()

    # Test 3: Context analysis
    print("Test 3: Context analysis")
    analysis = claude.analyze_context(
        command="init",
        args={"project_type": "fullstack", "backend": "springboot"},
        result={"success": True}
    )
    print(f"Analysis: {json.dumps(analysis, indent=2)}")
    print()


if __name__ == "__main__":
    test_claude()
