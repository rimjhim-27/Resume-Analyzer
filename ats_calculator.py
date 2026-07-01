"""
Weighted ATS Score Calculator.
Scoring breakdown:
  - Skills match (weighted by skill importance): 40%
  - Resume sections completeness:               20%
  - Experience/Internship mentions:             15%
  - Projects:                                   10%
  - Certifications:                              5%
  - Formatting signals (LinkedIn, GitHub, etc.): 5%
  - Education:                                   5%
"""

import re
from skills_database import ALL_SKILLS
from resumes.skill_extractor import extract_skills


def _extract_jd_skills(job_description: str) -> dict[str, float]:
    """
    Find skills mentioned in job description.
    Returns {skill: weight} dict.
    """
    jd_lower = job_description.lower()
    found = {}
    for skill, weight in ALL_SKILLS.items():
        pattern = r'(?<![a-z0-9])' + re.escape(skill) + r'(?![a-z0-9])'
        if re.search(pattern, jd_lower):
            found[skill] = weight
    return found


def _section_score(text: str) -> tuple[int, list[str], list[str]]:
    """Check presence of key resume sections. Returns (score 0-100, found, missing)."""
    sections = {
        "Education":       ["education", "b.tech", "bachelor", "b.e.", "degree", "university", "college"],
        "Skills":          ["skills", "technical skills", "technologies"],
        "Projects":        ["project", "projects", "built", "developed"],
        "Experience":      ["experience", "internship", "intern", "work experience", "employment"],
        "Certifications":  ["certification", "certificate", "certified", "coursera", "udemy"],
        "Summary/Objective": ["summary", "objective", "about me", "profile"],
        "Achievements":    ["achievement", "award", "honor", "distinction"],
    }
    text_lower = text.lower()
    found, missing = [], []
    for section, kws in sections.items():
        if any(kw in text_lower for kw in kws):
            found.append(section)
        else:
            missing.append(section)
    # Weight: required sections count more
    required = {"Education", "Skills", "Projects", "Experience"}
    req_found = len([s for s in found if s in required])
    opt_found = len([s for s in found if s not in required])
    score = min(100, int((req_found / len(required)) * 80 + (opt_found / 3) * 20))
    return score, found, missing


def _formatting_score(text: str) -> int:
    """Check for professional formatting signals."""
    text_lower = text.lower()
    score = 0
    checks = {
        "github":   15,
        "linkedin": 15,
        "@":        20,   # email present
        "phone":     5,
    }
    # Phone pattern
    if re.search(r'[\+\d][\d\s\-]{8,}', text):
        score += 10
    for kw, pts in checks.items():
        if kw in text_lower:
            score += pts
    # Check for bullet points / quantified achievements
    if re.search(r'[\u2022\u2013\-]\s', text):
        score += 10
    if re.search(r'\d+[%x\+]', text_lower):
        score += 15  # quantified results
    return min(100, score)


def calculate_ats_score(resume_skills: list[str], job_description: str, resume_text: str = ""):
    """
    Full weighted ATS score calculation.
    Returns (ats_score, matched_skills, missing_skills, resume_strength, breakdown)
    """

    # ── 1. Skills (40%) ──────────────────────────────────────────────────────
    jd_skills = _extract_jd_skills(job_description)
    resume_skills_set = {s.lower().strip() for s in resume_skills}

    matched_skills = [s for s in jd_skills if s in resume_skills_set]
    missing_skills = [s for s in jd_skills if s not in resume_skills_set]

    if jd_skills:
        # Weighted match: sum weights of matched / sum of all required weights
        matched_weight = sum(jd_skills[s] for s in matched_skills)
        total_weight = sum(jd_skills.values())
        skills_score = round((matched_weight / total_weight) * 100)
    else:
        skills_score = 0

    # ── 2. Sections (20%) ────────────────────────────────────────────────────
    section_score, found_sections, missing_sections = _section_score(resume_text)

    # ── 3. Experience (15%) ──────────────────────────────────────────────────
    text_lower = resume_text.lower()
    exp_keywords = ["experience", "internship", "intern", "worked at", "employed"]
    exp_score = 100 if any(kw in text_lower for kw in exp_keywords) else 40

    # ── 4. Projects (10%) ────────────────────────────────────────────────────
    proj_score = 100 if "project" in text_lower else 30

    # ── 5. Certifications (5%) ───────────────────────────────────────────────
    cert_kws = ["certification", "certificate", "certified", "coursera", "udemy", "nptel"]
    cert_score = 100 if any(kw in text_lower for kw in cert_kws) else 20

    # ── 6. Formatting (5%) ───────────────────────────────────────────────────
    fmt_score = _formatting_score(resume_text)

    # ── 7. Education (5%) ────────────────────────────────────────────────────
    edu_kws = ["education", "b.tech", "bachelor", "b.e.", "degree"]
    edu_score = 100 if any(kw in text_lower for kw in edu_kws) else 50

    # ── Weighted final score ─────────────────────────────────────────────────
    weights = {
        "Skills Match":     (skills_score,  0.40),
        "Sections":         (section_score, 0.20),
        "Experience":       (exp_score,     0.15),
        "Projects":         (proj_score,    0.10),
        "Certifications":   (cert_score,    0.05),
        "Formatting":       (fmt_score,     0.05),
        "Education":        (edu_score,     0.05),
    }

    ats_score = round(sum(score * weight for score, weight in weights.values()))

    breakdown = {k: v[0] for k, v in weights.items()}

    # Resume strength = how well resume skills cover JD requirements
    if jd_skills:
        resume_strength = round((len(matched_skills) / len(jd_skills)) * 100)
    else:
        resume_strength = round((len(resume_skills) / max(1, len(resume_skills) + 5)) * 100)

    return (
        min(ats_score, 99),   # cap at 99 (nothing is perfect)
        sorted(matched_skills),
        sorted(missing_skills),
        resume_strength,
        breakdown,
        found_sections,
        missing_sections,
    )
