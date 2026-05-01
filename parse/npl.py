import spacy
from spacy.pipeline import EntityRuler


# =========================
nlp = spacy.load("en_core_web_sm")

nlp.disable_pipes("ner")


ruler = nlp.add_pipe("entity_ruler",before="ner")

patterns = [

    # EMAIL
    {
        "label": "EMAIL",
        "pattern": [{"TEXT": {"REGEX": r"[\w\.-]+@[\w\.-]+\.\w+"}}]
    },

    # PHONE
    {
        "label": "PHONE",
        "pattern": [{"TEXT": {"REGEX": r"(\+88)?01[3-9]\d{8}"}}]
    },

    # EDUCATION
    {
        "label": "EDUCATION",
        "pattern": [{"LOWER": {"IN": [
            "ssc", "hsc", "diploma",
            "bsc", "bachelor",
            "master", "phd"
        ]}}]
    },

    # EXPERIENCE
    {
        "label": "EXPERIENCE",
        "pattern": [{"LOWER": {"IN": [
            "intern", "internship",
            "developer", "engineer",
            "backend", "frontend",
            "software"
        ]}}]
    },

    # SKILLS
    {
        "label": "SKILL",
        "pattern": [{"LOWER": {"IN": [
            "python", "django", "flask",
            "docker", "redis", "nginx",
            "celery", "mysql", "postgresql",
            "javascript", "html", "css",
            "bootstrap", "tailwind",
            "git", "linux", "api", "rest"
        ]}}]
    },

    # SOFT SKILLS
    {
        "label": "SOFT_SKILL",
        "pattern": [{"LOWER": {"IN": [
            "leadership",
            "communication",
            "teamwork",
            "problem-solving",
            "adaptability"
        ]}}]
    },

    # ADDRESS
    {
        "label": "ADDRESS",
        "pattern": [{"LOWER": {"IN": [
            "dhaka", "feni",
            "chittagong", "khulna"
        ]}}]
    },
]


ruler.add_patterns(patterns)


__all__ = ["nlp"]