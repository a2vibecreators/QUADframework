"""
Gemini API Wrapper
==================

Google Gemini AI integration for QUAD.

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import json
import re
from typing import Dict, Any, Optional


class GeminiAPI:
    """Wrapper for Google Gemini API"""

    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        """
        Initialize Gemini API.

        Args:
            api_key: Google AI API key
            model: Model name (gemini-1.5-flash or gemini-1.5-pro)
        """
        self.api_key = api_key
        self.model = model
        self._client = None

    def _get_client(self):
        """Lazy load Gemini client"""
        if self._client is None:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self._client = genai.GenerativeModel(self.model)
            except ImportError:
                raise ImportError(
                    "google-generativeai library not installed. "
                    "Install with: pip install google-generativeai"
                )
        return self._client

    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """
        Generate text with Gemini.

        Args:
            prompt: The prompt to send
            temperature: Creativity (0.0-1.0)

        Returns:
            Generated text
        """
        client = self._get_client()

        try:
            response = client.generate_content(
                prompt,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": 8192,
                }
            )

            return response.text

        except Exception as e:
            raise Exception(f"Gemini API error: {e}")

    def generate_json(self, prompt: str, temperature: float = 0.7) -> Dict:
        """
        Generate JSON response with Gemini.

        Args:
            prompt: The prompt (should ask for JSON)
            temperature: Creativity

        Returns:
            Parsed JSON dict
        """
        # Add JSON instruction to prompt
        json_prompt = f"{prompt}\n\nIMPORTANT: Return ONLY valid JSON, no explanation."

        response_text = self.generate(json_prompt, temperature)

        # Extract JSON from response (sometimes wrapped in markdown)
        json_text = self._extract_json(response_text)

        try:
            return json.loads(json_text)
        except json.JSONDecodeError as e:
            # If parsing fails, return error with raw text
            return {
                "error": "Failed to parse JSON response",
                "details": str(e),
                "raw_response": response_text
            }

    def _extract_json(self, text: str) -> str:
        """Extract JSON from text (handles markdown code blocks)"""
        # Try to find JSON in markdown code blocks
        json_pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
        match = re.search(json_pattern, text)

        if match:
            return match.group(1)

        # Try to find JSON object directly
        if text.strip().startswith('{') or text.strip().startswith('['):
            return text.strip()

        # Return as-is
        return text

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

    def classify_task(self, task: str) -> Dict[str, Any]:
        """
        Classify task complexity.

        Args:
            task: Task description

        Returns:
            {
                "complexity": "simple" | "complex" | "critical",
                "confidence": 0.0-1.0,
                "reasoning": "..."
            }
        """
        prompt = f"""
Classify this task's complexity:

Task: {task}

Categories:
- simple: Basic queries, explanations, simple analysis
- complex: Code generation, architecture design, refactoring
- critical: Production deployment, security, compliance

Return ONLY valid JSON:
{{
  "complexity": "simple|complex|critical",
  "confidence": 0.85,
  "reasoning": "brief explanation"
}}
"""

        try:
            return self.generate_json(prompt, temperature=0.3)
        except:
            # Fallback
            return {
                "complexity": "complex",
                "confidence": 0.5,
                "reasoning": "Classification failed, defaulting to complex"
            }

    def estimate_confidence(self, response: str) -> float:
        """
        Estimate confidence in Gemini's response.

        Uses heuristics to determine if Gemini is uncertain.

        Args:
            response: Generated response text

        Returns:
            Confidence score (0.0-1.0)
        """
        response_lower = response.lower()

        # Uncertainty markers (reduce confidence)
        uncertainty_markers = [
            "i'm not sure", "i think", "maybe", "possibly",
            "might be", "could be", "uncertain", "probably",
            "i don't know", "unclear", "ambiguous"
        ]

        # Confidence markers (increase confidence)
        confidence_markers = [
            "certainly", "definitely", "clearly", "obviously",
            "specifically", "precisely", "exactly", "confirmed"
        ]

        # Count markers
        uncertainty_count = sum(1 for m in uncertainty_markers if m in response_lower)
        confidence_count = sum(1 for m in confidence_markers if m in response_lower)

        # Base confidence
        base_confidence = 0.8

        # Adjust based on markers
        confidence = base_confidence
        confidence -= uncertainty_count * 0.15  # Each uncertainty marker reduces by 0.15
        confidence += confidence_count * 0.05   # Each confidence marker adds 0.05

        # Length check (very short responses might be uncertain)
        if len(response) < 50:
            confidence -= 0.1

        # Bounds
        confidence = max(0.0, min(1.0, confidence))

        return round(confidence, 2)


def test_gemini():
    """Test Gemini API (for development)"""
    import os

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Set GEMINI_API_KEY environment variable to test")
        return

    gemini = GeminiAPI(api_key)

    # Test 1: Simple generation
    print("Test 1: Simple generation")
    response = gemini.generate("What is an API in simple terms?")
    print(f"Response: {response[:200]}...")
    print(f"Confidence: {gemini.estimate_confidence(response)}")
    print()

    # Test 2: JSON generation
    print("Test 2: JSON generation")
    result = gemini.generate_json("""
    List 3 programming languages with their use cases.
    Return as JSON array: [{"language": "...", "use_case": "..."}]
    """)
    print(f"Result: {json.dumps(result, indent=2)}")
    print()

    # Test 3: Context analysis
    print("Test 3: Context analysis")
    analysis = gemini.analyze_context(
        command="init",
        args={"project_type": "fullstack", "backend": "springboot"},
        result={"success": True}
    )
    print(f"Analysis: {json.dumps(analysis, indent=2)}")
    print()


if __name__ == "__main__":
    test_gemini()
