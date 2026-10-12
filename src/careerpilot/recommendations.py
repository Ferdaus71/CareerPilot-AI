CAREER_FOCUS_MAP: dict[str, tuple[str, ...]] = {
    "python": ("Python Developer", "Data Analyst", "Automation Engineer"),
    "sql": ("Data Analyst", "Business Intelligence Analyst", "Data Engineer"),
    "machine learning": ("Machine Learning Engineer", "Data Scientist", "AI Analyst"),
    "deep learning": ("Deep Learning Engineer", "Research Engineer", "AI Specialist"),
    "natural language processing": ("NLP Engineer", "AI Product Analyst", "Search Engineer"),
    "cloud": ("Cloud Engineer", "DevOps Engineer", "Platform Engineer"),
    "data analysis": ("Data Analyst", "Product Analyst", "Analytics Engineer"),
    "project management": ("Project Manager", "Technical Program Manager", "Scrum Master"),
    "software engineering": ("Software Engineer", "Back-end Engineer", "Full-Stack Engineer"),
    "data engineering": ("Data Engineer", "Analytics Engineer", "ETL Engineer"),
    "business intelligence": ("Business Intelligence Analyst", "Analytics Engineer", "Reporting Analyst"),
    "devops": ("DevOps Engineer", "Platform Engineer", "Cloud Engineer"),
    "product analytics": ("Product Analyst", "Growth Analyst", "Business Analyst"),
}


def build_recommendations(missing_skills: list[str]) -> list[str]:
    """Generate transparent, rule-based career recommendations."""
    if not missing_skills:
        return ["Your profile already aligns well with the job requirements. Keep refining your portfolio and interview preparation."]

    seen: set[str] = set()
    recommendations: list[str] = []
    for skill in missing_skills[:5]:
        lower_skill = skill.lower()
        focus_roles = CAREER_FOCUS_MAP.get(lower_skill, (skill.title(),))
        for role in focus_roles:
            if role not in seen:
                seen.add(role)
                recommendations.append(
                    f"Target a {role} role by building a small project and documenting the skill gap around {skill}."
                )
                break

    if not recommendations:
        recommendations.append(
            f"Build a portfolio that demonstrates {', '.join(missing_skills[:3])} and communicate the work clearly in interviews."
        )

    return recommendations
