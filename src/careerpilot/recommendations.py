from __future__ import annotations


def build_recommendations(missing_skills: list[str]) -> list[str]:
    """Generate a small list of practical, transparent recommendations."""
    if not missing_skills:
        return ["Your profile already aligns well with the job requirements. Keep refining your portfolio and interview preparation."]

    recommendations: list[str] = []
    for skill in missing_skills[:5]:
        if skill.lower() == "python":
            recommendations.append("Complete a Python project that demonstrates data processing, APIs, or automation workflows.")
        elif skill.lower() == "sql":
            recommendations.append("Practice SQL queries for joins, filtering, aggregation, and data validation.")
        elif skill.lower() == "machine learning":
            recommendations.append("Work through a supervised learning project using scikit-learn and clear evaluation metrics.")
        elif skill.lower() == "cloud":
            recommendations.append("Gain cloud deployment experience with AWS, Azure, or GCP basics.")
        else:
            recommendations.append(f"Build a focused project and documentation set around {skill} to strengthen your application.")

    return recommendations
