import spacy
from spacy.pipeline import EntityRuler
from dynamic_data.models import SkillModel, EducationModel

# Cache the NLP model so we don't load it heavily on every request
_nlp_instance = None

def get_nlp():
    global _nlp_instance
    if _nlp_instance is not None:
        return _nlp_instance

    nlp = spacy.load("en_core_web_md")
    # Kept NER enabled so we can globally detect GPE (countries, cities) and PERSON (names)


    ruler = nlp.add_pipe("entity_ruler", before="ner")

    patterns = [
       
        {
            "label": "EMAIL",
            "pattern": [{"TEXT": {"REGEX": r"[\w\.-]+@[\w\.-]+\.\w+"}}]
        },
   
        {
            "label": "PHONE",
            "pattern": [{"TEXT": {"REGEX": r"\+?[0-9]{6,15}"}}]
        },

        {
            "label": "EXPERIENCE",
            "pattern": [{"LOWER": {"IN": [
                "intern", "internship", "developer", "engineer",
                "manager", "lead", "architect", "analyst"
            ]}}]
        },
       
        {
            "label": "SOFT_SKILL",
            "pattern": [{"LOWER": {"IN": [
                "leadership", "communication", "teamwork", "adaptability",
                "creativity", "flexibility", "organization", "multitasking",
                "negotiation", "empathy", "mentoring", "coaching",
                "initiative", "dependability", "reliability", "punctuality",
                "collaboration", "motivation", "patience", "integrity",
                "dedication", "persuasion"
            ]}}]
        },
 
        {"label": "SOFT_SKILL", "pattern": [{"LOWER": "time"}, {"LOWER": "management"}]},
        {"label": "SOFT_SKILL", "pattern": [{"LOWER": "critical"}, {"LOWER": "thinking"}]},
        {"label": "SOFT_SKILL", "pattern": [{"LOWER": "problem"}, {"LOWER": "solving"}]},
        {"label": "SOFT_SKILL", "pattern": [{"LOWER": "problem"}, {"TEXT": "-"}, {"LOWER": "solving"}]},
        {"label": "SOFT_SKILL", "pattern": [{"LOWER": "attention"}, {"LOWER": "to"}, {"LOWER": "detail"}]},
        {"label": "SOFT_SKILL", "pattern": [{"LOWER": "conflict"}, {"LOWER": "resolution"}]},
        {"label": "SOFT_SKILL", "pattern": [{"LOWER": "emotional"}, {"LOWER": "intelligence"}]},
        {"label": "SOFT_SKILL", "pattern": [{"LOWER": "decision"}, {"LOWER": "making"}]},
        {"label": "SOFT_SKILL", "pattern": [{"LOWER": "active"}, {"LOWER": "listening"}]},
        {"label": "SOFT_SKILL", "pattern": [{"LOWER": "public"}, {"LOWER": "speaking"}]},
        {"label": "SOFT_SKILL", "pattern": [{"LOWER": "work"}, {"LOWER": "ethic"}]},
  
        {
            "label": "ADDRESS",
            "pattern": [{"LOWER": {"IN": [
                "dhaka", "feni", "chittagong", "khulna"
            ]}}]
        },
     
        {
            "label":"EDUCATION",
            "pattern":[
                {"LOWER": {"IN": ["ssc", "hsc", "diploma", "bsc", "bachelor", "master", "phd"]}}
            ]
        }
    ]


    try:
        tech_skills = list(SkillModel.objects.values_list('name', flat=True))  

        if tech_skills:
            patterns.append({
                "label": "SKILL",
                "pattern": [{"LOWER": {"IN": [str(s).lower() for s in tech_skills if s]}}]
            })
        else:
            patterns.append({
                "label": "SKILL",
                "pattern": [{"LOWER": {"IN": ["python", "django", "flask", "docker", "redis", "nginx", "celery", "mysql", "postgresql", "javascript", "html", "css", "bootstrap", "tailwind", "git", "linux", "api", "rest"]}}]
            })
    except Exception as e:
        patterns.append({
            "label": "SKILL",
            "pattern": [{"LOWER": {"IN": ["python", "django", "flask", "docker", "redis", "nginx", "celery", "mysql", "postgresql", "javascript", "html", "css", "bootstrap", "tailwind", "git", "linux", "api", "rest"]}}]
        })

    ruler.add_patterns(patterns)
    _nlp_instance = nlp
    return _nlp_instance

__all__ = ["get_nlp"]