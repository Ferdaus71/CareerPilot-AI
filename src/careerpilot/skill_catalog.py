from __future__ import annotations

SKILL_ALIASES: dict[str, tuple[str, ...]] = {
    "python": ("python", "python programming", "python developer"),
    "sql": ("sql", "structured query language", "postgresql", "postgres", "mysql"),
    "machine learning": ("machine learning", "ml", "ml engineer", "predictive modeling"),
    "data analysis": ("data analysis", "analytics", "data analytics", "business intelligence"),
    "deep learning": ("deep learning", "dl", "neural networks", "tensorflow"),
    "natural language processing": ("natural language processing", "nlp", "text analytics", "language processing"),
    "data visualization": ("data visualization", "visualization", "tableau", "power bi", "matplotlib"),
    "cloud": ("cloud", "aws", "azure", "gcp", "cloud computing"),
    "docker": ("docker", "containers", "containerization"),
    "software engineering": ("software engineering", "swe", "backend engineering", "full stack"),
    "pandas": ("pandas", "python pandas", "pandas dataframes"),
    "scikit-learn": ("scikit-learn", "sklearn", "scikit learn"),
    "excel": ("excel", "microsoft excel", "spreadsheets"),
    "statistics": ("statistics", "statistical analysis", "hypothesis testing"),
    "communication": ("communication", "stakeholder communication", "presentations"),
    "project management": ("project management", "agile", "scrum", "jira"),
    "api development": ("api development", "rest api", "fastapi", "flask"),
    "databases": ("database", "databases", "sql database", "postgres database"),
    "javascript": ("javascript", "js", "node.js"),
    "java": ("java", "java development"),
    "csharp": ("c#", "csharp", ".net"),
}

SKILL_CATEGORIES: dict[str, list[str]] = {
    "Programming languages": ["python", "sql", "javascript", "java", "csharp"],
    "Data and analytics": ["data analysis", "statistics", "data visualization", "pandas", "excel"],
    "Machine learning": ["machine learning", "deep learning", "natural language processing", "scikit-learn"],
    "Cloud and deployment": ["cloud", "docker", "api development", "databases"],
    "Leadership and delivery": ["communication", "project management", "software engineering"],
}
