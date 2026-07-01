"""
Skill extractor - finds skills in resume text using phrase matching.
Handles multi-word skills correctly (e.g. "machine learning" won't
match just the word "machine").
"""

import re
from skills_database import SKILL_LIST, SKILLS_DATABASE


def _normalize(text: str) -> str:
    return re.sub(r'\s+', ' ', text.lower().strip())


def extract_skills(text: str) -> list[str]:
    """
    Return sorted list of skills found in text.
    Uses word-boundary aware matching to avoid false positives.
    """
    text_norm = _normalize(text)
    found = set()

    for skill in SKILL_LIST:
        skill_norm = _normalize(skill)
        # Use word boundary pattern - handles multi-word skills
        pattern = r'(?<![a-z0-9])' + re.escape(skill_norm) + r'(?![a-z0-9])'
        if re.search(pattern, text_norm):
            found.add(skill)

    return sorted(list(found))


def extract_skills_by_category(text: str) -> dict[str, list[str]]:
    """
    Return skills grouped by category.
    """
    found_all = set(extract_skills(text))
    categorized = {}

    for category, skills in SKILLS_DATABASE.items():
        matched = [s for s in skills if s in found_all]
        if matched:
            categorized[category] = sorted(matched)

    return categorized
