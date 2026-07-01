"""
Learning roadmap generator - customized by role and missing skills.
"""

BASE_ROADMAPS = {
    "ML Engineer": [
        ("Week 1–2", "Python Fundamentals + NumPy / Pandas"),
        ("Week 3",   "Data Cleaning & Preprocessing"),
        ("Week 4",   "Data Visualization (Matplotlib, Seaborn)"),
        ("Week 5",   "ML Basics + Scikit-learn"),
        ("Week 6",   "Supervised & Unsupervised Learning"),
        ("Week 7",   "Deep Learning Fundamentals + TensorFlow / PyTorch"),
        ("Week 8",   "Build & Deploy an end-to-end ML Project"),
    ],
    "Data Scientist": [
        ("Week 1",   "Python + Statistics Foundations"),
        ("Week 2–3", "Pandas — data cleaning, merging, aggregation"),
        ("Week 4",   "Exploratory Data Analysis (EDA)"),
        ("Week 5",   "Data Visualization — Matplotlib, Seaborn, Plotly"),
        ("Week 6",   "Machine Learning with Scikit-learn"),
        ("Week 7",   "SQL for data querying"),
        ("Week 8",   "Capstone: Full EDA + ML pipeline project"),
    ],
    "Frontend Developer": [
        ("Week 1",   "HTML5 Semantics + Accessibility"),
        ("Week 2",   "CSS3 — Flexbox, Grid, Animations"),
        ("Week 3",   "JavaScript ES6+ Fundamentals"),
        ("Week 4",   "Responsive Design + Tailwind CSS"),
        ("Week 5",   "React — Components, Props, State, Hooks"),
        ("Week 6",   "React Router + State Management (Redux/Zustand)"),
        ("Week 7",   "REST API Integration + Axios"),
        ("Week 8",   "Deploy a full React app (Vercel/Netlify)"),
    ],
    "Backend Developer": [
        ("Week 1",   "Python OOP + Virtual Environments"),
        ("Week 2",   "Django/FastAPI Fundamentals"),
        ("Week 3",   "SQL — PostgreSQL schema design + queries"),
        ("Week 4",   "REST API design + CRUD operations"),
        ("Week 5",   "Authentication — JWT + OAuth"),
        ("Week 6",   "Caching + Background Tasks"),
        ("Week 7",   "Docker + basic deployment (Railway/Render)"),
        ("Week 8",   "Build a full backend project with docs"),
    ],
    "Full Stack Developer": [
        ("Week 1",   "HTML, CSS, JavaScript Refresh"),
        ("Week 2",   "React — components and hooks"),
        ("Week 3",   "Node.js + Express.js — REST API"),
        ("Week 4",   "Databases — PostgreSQL / MongoDB"),
        ("Week 5",   "Authentication (JWT)"),
        ("Week 6",   "Full stack integration (React + Express)"),
        ("Week 7",   "Docker + CI/CD basics"),
        ("Week 8",   "Deploy a full-stack project"),
    ],
    "AI / GenAI Engineer": [
        ("Week 1",   "Python + APIs — OpenAI, Anthropic basics"),
        ("Week 2",   "Prompt Engineering fundamentals"),
        ("Week 3",   "LangChain — chains, agents, tools"),
        ("Week 4",   "RAG — embeddings + vector databases (Pinecone/Chroma)"),
        ("Week 5",   "HuggingFace — fine-tuning small models"),
        ("Week 6",   "Building an AI-powered app (Streamlit/FastAPI)"),
        ("Week 7",   "Evaluation, safety, and red-teaming basics"),
        ("Week 8",   "Ship a GenAI project with a public demo"),
    ],
    "DevOps / Cloud Engineer": [
        ("Week 1",   "Linux command line + shell scripting"),
        ("Week 2",   "Git + GitHub Actions (CI/CD)"),
        ("Week 3",   "Docker — images, containers, Compose"),
        ("Week 4",   "Kubernetes basics — pods, services, deployments"),
        ("Week 5",   "AWS / Azure core services"),
        ("Week 6",   "Terraform — Infrastructure as Code"),
        ("Week 7",   "Monitoring + Logging (Prometheus, Grafana)"),
        ("Week 8",   "End-to-end pipeline: code → container → cloud"),
    ],
}


def generate_learning_roadmap(target_role: str, missing_skills: list) -> list[dict]:
    """
    Returns roadmap as list of {week, topic, is_skill_gap} dicts.
    Appends extra entries for missing skills not covered by base roadmap.
    """
    # Fuzzy match role name to our keys
    matched_key = None
    for key in BASE_ROADMAPS:
        if key.lower() in target_role.lower() or target_role.lower() in key.lower():
            matched_key = key
            break

    if not matched_key:
        matched_key = "Full Stack Developer"  # sensible default

    roadmap = [
        {"week": week, "topic": topic, "is_skill_gap": False}
        for week, topic in BASE_ROADMAPS[matched_key]
    ]

    # Append missing skills not already mentioned in roadmap topics
    roadmap_text = " ".join(r["topic"].lower() for r in roadmap)
    extras = []
    for skill in missing_skills[:4]:  # max 4 extras to keep it clean
        if skill.lower() not in roadmap_text:
            extras.append(skill)

    if extras:
        roadmap.append({
            "week": "Ongoing",
            "topic": f"Skill gap practice: {', '.join(extras)} — build mini-projects",
            "is_skill_gap": True,
        })

    return roadmap
