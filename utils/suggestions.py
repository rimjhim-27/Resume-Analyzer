"""
Generate actionable, specific improvement suggestions.
"""

import re


def generate_suggestions(
    ats_score: int,
    missing_skills: list,
    resume_text: str,
    missing_sections: list,
    matched_skills: list,
) -> list[dict]:
    """
    Returns list of suggestion dicts: {icon, type, message, priority}
    Priority: 'high', 'medium', 'low'
    """
    suggestions = []
    text_lower = resume_text.lower()

    # ── ATS Score ───────────────────────────────────────────────────────────
    if ats_score < 40:
        suggestions.append({
            "icon": "🔴", "type": "ATS Score",
            "message": "Your ATS score is low. Rewrite your resume to mirror the exact keywords from the job description.",
            "priority": "high"
        })
    elif ats_score < 65:
        suggestions.append({
            "icon": "🟡", "type": "ATS Score",
            "message": f"ATS score of {ats_score}% is moderate. Add more job-specific keywords to push past 70%.",
            "priority": "medium"
        })
    else:
        suggestions.append({
            "icon": "🟢", "type": "ATS Score",
            "message": f"Strong ATS score of {ats_score}%! Your resume aligns well with this job description.",
            "priority": "low"
        })

    # ── Missing Skills ───────────────────────────────────────────────────────
    if missing_skills:
        top_missing = missing_skills[:5]
        suggestions.append({
            "icon": "📚", "type": "Missing Skills",
            "message": f"Add these high-priority skills if you have experience: {', '.join(top_missing)}.",
            "priority": "high"
        })

    # ── Missing Sections ─────────────────────────────────────────────────────
    required_missing = [s for s in missing_sections if s in {"Education", "Skills", "Projects", "Experience"}]
    optional_missing = [s for s in missing_sections if s not in {"Education", "Skills", "Projects", "Experience"}]

    if required_missing:
        suggestions.append({
            "icon": "📋", "type": "Missing Sections",
            "message": f"Add these required sections: {', '.join(required_missing)}. ATS parsers look for these headings explicitly.",
            "priority": "high"
        })
    if optional_missing:
        suggestions.append({
            "icon": "➕", "type": "Optional Sections",
            "message": f"Consider adding: {', '.join(optional_missing)} — they improve completeness scores.",
            "priority": "low"
        })

    # ── Quantification ───────────────────────────────────────────────────────
    if not re.search(r'\d+[%x\+kmKM]', resume_text):
        suggestions.append({
            "icon": "📊", "type": "Quantify Achievements",
            "message": "Add numbers to your bullet points (e.g. 'Improved load time by 40%', 'Built app used by 500+ users').",
            "priority": "high"
        })

    # ── GitHub / LinkedIn ────────────────────────────────────────────────────
    if "github" not in text_lower:
        suggestions.append({
            "icon": "🐙", "type": "GitHub Profile",
            "message": "Add your GitHub link (github.com/rimjhim-27). Recruiters check this — it's your live portfolio.",
            "priority": "high"
        })
    if "linkedin" not in text_lower:
        suggestions.append({
            "icon": "💼", "type": "LinkedIn Profile",
            "message": "Include your LinkedIn URL. Many ATS systems and recruiters require it.",
            "priority": "medium"
        })

    # ── Action Verbs ─────────────────────────────────────────────────────────
    strong_verbs = ["built", "developed", "designed", "implemented", "optimized",
                    "led", "created", "deployed", "reduced", "increased"]
    if not any(v in text_lower for v in strong_verbs):
        suggestions.append({
            "icon": "✍️", "type": "Action Verbs",
            "message": "Start bullet points with strong action verbs: Built, Developed, Designed, Optimized, Deployed.",
            "priority": "medium"
        })

    # ── Length ───────────────────────────────────────────────────────────────
    word_count = len(resume_text.split())
    if word_count < 200:
        suggestions.append({
            "icon": "📝", "type": "Resume Length",
            "message": f"Your resume seems short ({word_count} words). Aim for 400–600 words for a 1-page resume.",
            "priority": "medium"
        })
    elif word_count > 1000:
        suggestions.append({
            "icon": "✂️", "type": "Resume Length",
            "message": f"Resume may be too long ({word_count} words). Keep it under 600 words for entry-level/intern roles.",
            "priority": "low"
        })

    return sorted(suggestions, key=lambda x: {"high": 0, "medium": 1, "low": 2}[x["priority"]])
