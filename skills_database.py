"""
Skills database organized by category with weights.
Each skill has a weight reflecting its market value/frequency.
"""

SKILLS_DATABASE = {
    "Programming Languages": {
        "python": 1.5,
        "java": 1.3,
        "javascript": 1.5,
        "typescript": 1.4,
        "c": 1.0,
        "c++": 1.2,
        "go": 1.3,
        "rust": 1.2,
        "kotlin": 1.2,
        "swift": 1.1,
        "r": 1.1,
        "scala": 1.1,
    },
    "Web Frontend": {
        "html": 1.0,
        "css": 1.0,
        "react": 1.5,
        "next.js": 1.4,
        "vue": 1.3,
        "angular": 1.2,
        "bootstrap": 1.0,
        "tailwind css": 1.3,
        "redux": 1.2,
        "webpack": 1.1,
    },
    "Web Backend": {
        "node.js": 1.4,
        "express.js": 1.3,
        "django": 1.3,
        "flask": 1.2,
        "fastapi": 1.4,
        "spring boot": 1.3,
        "rest api": 1.3,
        "graphql": 1.3,
    },
    "Databases": {
        "sql": 1.3,
        "mysql": 1.2,
        "postgresql": 1.3,
        "mongodb": 1.2,
        "redis": 1.2,
        "firebase": 1.1,
        "sqlite": 1.0,
        "elasticsearch": 1.2,
    },
    "ML / AI": {
        "machine learning": 1.5,
        "deep learning": 1.5,
        "artificial intelligence": 1.5,
        "data science": 1.4,
        "numpy": 1.2,
        "pandas": 1.3,
        "matplotlib": 1.1,
        "seaborn": 1.1,
        "scikit-learn": 1.3,
        "tensorflow": 1.4,
        "pytorch": 1.4,
        "keras": 1.2,
        "nlp": 1.4,
        "computer vision": 1.4,
        "langchain": 1.4,
        "genai": 1.5,
        "rag": 1.4,
        "openai": 1.4,
        "llm": 1.4,
        "huggingface": 1.3,
    },
    "DevOps / Cloud": {
        "aws": 1.5,
        "azure": 1.4,
        "gcp": 1.4,
        "docker": 1.4,
        "kubernetes": 1.4,
        "linux": 1.3,
        "git": 1.2,
        "github": 1.1,
        "ci/cd": 1.3,
        "terraform": 1.3,
        "jenkins": 1.2,
    },
    "Data & Analytics": {
        "power bi": 1.2,
        "tableau": 1.2,
        "excel": 1.0,
        "statistics": 1.2,
        "data analysis": 1.3,
        "data visualization": 1.2,
        "apache spark": 1.3,
        "hadoop": 1.1,
    },
    "Mobile": {
        "android": 1.3,
        "ios": 1.2,
        "react native": 1.3,
        "flutter": 1.3,
        "kotlin": 1.3,
        "swift": 1.2,
    },
}

# Flat list for quick lookup
ALL_SKILLS = {
    skill: weight
    for category in SKILLS_DATABASE.values()
    for skill, weight in category.items()
}

# Flat skill list (no weights) for simple iteration
SKILL_LIST = list(ALL_SKILLS.keys())
