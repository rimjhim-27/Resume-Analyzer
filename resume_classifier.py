"""
Role classifier - predicts best-fit job roles from resume skills.
Uses weighted keyword matching with confidence percentages.
"""

ROLE_PROFILES = {
    "Frontend Developer": {
        "html": 1.0, "css": 1.0, "javascript": 1.5, "react": 1.5,
        "next.js": 1.3, "typescript": 1.3, "tailwind css": 1.2,
        "bootstrap": 1.0, "redux": 1.1, "webpack": 1.0,
    },
    "Backend Developer": {
        "node.js": 1.5, "express.js": 1.3, "django": 1.5, "flask": 1.3,
        "fastapi": 1.4, "rest api": 1.3, "graphql": 1.2,
        "sql": 1.2, "postgresql": 1.2, "mongodb": 1.1,
    },
    "Full Stack Developer": {
        "html": 1.0, "css": 1.0, "javascript": 1.3, "react": 1.3,
        "node.js": 1.3, "django": 1.2, "sql": 1.1,
        "rest api": 1.2, "mongodb": 1.1, "typescript": 1.1,
    },
    "Data Scientist": {
        "python": 1.3, "pandas": 1.5, "numpy": 1.3, "matplotlib": 1.2,
        "seaborn": 1.1, "statistics": 1.3, "data science": 1.5,
        "scikit-learn": 1.4, "machine learning": 1.3, "sql": 1.1,
        "data visualization": 1.2, "tableau": 1.1,
    },
    "ML Engineer": {
        "machine learning": 1.5, "deep learning": 1.5, "tensorflow": 1.4,
        "pytorch": 1.4, "scikit-learn": 1.3, "python": 1.2,
        "numpy": 1.1, "pandas": 1.1, "mlops": 1.3, "docker": 1.1,
    },
    "AI / GenAI Engineer": {
        "genai": 1.5, "llm": 1.5, "langchain": 1.5, "rag": 1.4,
        "openai": 1.4, "huggingface": 1.3, "nlp": 1.3,
        "deep learning": 1.2, "python": 1.1, "vector database": 1.3,
    },
    "DevOps / Cloud Engineer": {
        "docker": 1.4, "kubernetes": 1.4, "aws": 1.5, "azure": 1.4,
        "gcp": 1.4, "linux": 1.3, "ci/cd": 1.4, "terraform": 1.3,
        "jenkins": 1.2, "git": 1.1,
    },
    "Android Developer": {
        "android": 1.5, "kotlin": 1.5, "java": 1.3, "jetpack compose": 1.4,
        "room": 1.2, "retrofit": 1.2, "mvvm": 1.2, "xml": 1.0,
    },
}


def predict_roles(resume_text: str) -> list[tuple[str, float]]:
    """
    Return top 3 predicted roles with confidence percentages.
    """
    text_lower = resume_text.lower()
    role_scores = []

    for role, profile in ROLE_PROFILES.items():
        matched_weight = 0.0
        total_weight = sum(profile.values())

        for skill, weight in profile.items():
            if skill in text_lower:
                matched_weight += weight

        confidence = round((matched_weight / total_weight) * 100, 1)
        role_scores.append((role, confidence))

    role_scores.sort(key=lambda x: x[1], reverse=True)
    return role_scores[:3]
