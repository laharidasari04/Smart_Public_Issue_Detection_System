"""Generative AI service for public issue image analysis."""

import json
import os
import re

from dotenv import load_dotenv
from PIL import Image

load_dotenv()

AI_API_KEY = os.getenv("AI_API_KEY", "").strip()
DEMO_MODE = os.getenv("DEMO_MODE", "True").strip().lower() in ("true", "1", "yes")

VALID_CATEGORIES = [
    "Pothole",
    "Garbage",
    "Drainage",
    "Water Leakage",
    "Broken Street Light",
    "Damaged Road",
    "Open Manhole",
    "Fallen Tree",
    "Other",
]

VALID_SEVERITIES = ["Low", "Medium", "High"]

AI_PROMPT = """You are an AI assistant for identifying public infrastructure problems.

Analyze the uploaded image.

Identify the most likely public issue.

Possible categories:
Pothole
Garbage
Drainage
Water Leakage
Broken Street Light
Damaged Road
Open Manhole
Fallen Tree
Other

Return ONLY valid JSON with these fields:
category
description
severity
suggested_action

Severity must be:
Low
Medium
High

Do not invent information that cannot reasonably be observed from the image.
If the image does not clearly show a public issue, classify it as Other."""

DEMO_RESPONSE = {
    "category": "Pothole",
    "description": "Demo AI detected a possible road damage issue.",
    "severity": "Medium",
    "suggested_action": "Municipal authorities should inspect and repair the location.",
}

FALLBACK_RESPONSE = {
    "category": "Other",
    "description": "Unable to analyze the image clearly. Manual review is recommended.",
    "severity": "Low",
    "suggested_action": "Municipal authorities should inspect the reported location.",
}


def is_demo_mode():
    """Check if demo mode should be used."""
    if DEMO_MODE:
        return True
    if not AI_API_KEY:
        return True
    return False


def _normalize_category(category):
    """Normalize category to a valid value."""
    if not category:
        return "Other"

    category = category.strip()
    for valid in VALID_CATEGORIES:
        if category.lower() == valid.lower():
            return valid
    return "Other"


def _normalize_severity(severity):
    """Normalize severity to a valid value."""
    if not severity:
        return "Low"

    severity = severity.strip().capitalize()
    if severity in VALID_SEVERITIES:
        return severity
    return "Low"


def _parse_ai_response(text):
    """Safely parse JSON from AI response text."""
    if not text:
        return None

    text = text.strip()

    # Try direct JSON parse
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass

    # Try extracting JSON block from markdown or mixed text
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            data = json.loads(match.group())
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass

    return None


def _build_result(raw_data, demo=False):
    """Build a standardized result dictionary."""
    return {
        "category": _normalize_category(raw_data.get("category", "Other")),
        "description": str(raw_data.get("description", FALLBACK_RESPONSE["description"])).strip(),
        "severity": _normalize_severity(raw_data.get("severity", "Low")),
        "suggested_action": str(
            raw_data.get("suggested_action", FALLBACK_RESPONSE["suggested_action"])
        ).strip(),
        "demo_mode": demo,
    }


def analyze_issue(image):
    """
    Analyze an uploaded issue image using Generative AI.
    Returns dict with category, description, severity, suggested_action, demo_mode.
    """
    if is_demo_mode():
        return _build_result(DEMO_RESPONSE, demo=True)

    try:
        import google.generativeai as genai

        genai.configure(api_key=AI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        if isinstance(image, Image.Image):
            pil_image = image
        else:
            pil_image = Image.open(image)

        response = model.generate_content([AI_PROMPT, pil_image])
        response_text = response.text if response and response.text else ""
        parsed = _parse_ai_response(response_text)

        if parsed:
            return _build_result(parsed, demo=False)

        return _build_result(FALLBACK_RESPONSE, demo=False)

    except Exception:
        # If API fails, use fallback instead of crashing
        result = _build_result(FALLBACK_RESPONSE, demo=False)
        result["api_error"] = True
        return result
