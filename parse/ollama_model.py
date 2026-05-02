from ollama import AsyncClient

async def extract_pii_from_cv(text):
    prompt = f"""
Extract ONLY the personal identifiable information from this CV text.
Return ONLY valid JSON. If missing, use empty string or array.

RULES:
1. Output MUST be valid JSON. No explanation.
2. Escape quotes and newlines.

EXTRACTION RULES:
- name: Full name
- email: valid email
- phone: valid phone
- address: split into street, city, country (best guess)

CV TEXT:
{text}

OUTPUT FORMAT:
{{
  "name": "",
  "email": "",
  "phone": "",
  "address": []
}}
"""
    client = AsyncClient()
    response = await client.chat(
        model='llama3.2:3b',
        messages=[{'role': 'user', 'content': prompt}],
    )
    return response.message.content

async def call_ollama_model(text):
    prompt = f"""
You are a strict CV/Resume parser.

Your task is to extract structured data from the CV text and return ONLY valid JSON.

RULES:
1. Output MUST be valid JSON. No explanation, no extra text.
2. If any field is missing, return empty string "" or empty array [].
3. Clean and normalize text (remove extra spaces, fix broken words like "A I" -> "AI").
4. Extract information even if formatting is messy.
5. Group similar skills properly (no duplicates).
6. Infer sections based on headings like EXPERIENCE, EDUCATION, SKILLS, PROJECTS.
7. Use proper JSON escaping for quotes, tabs, and newlines within string values. Do NOT use literal newlines inside strings.

EXTRACTION RULES:

- experience:
  Extract even if partially available.
  Example:
  "Junior Backend Developer - September 2025 - Present"
  → role: "Junior Backend Developer"
  → duration: "September 2025 - Present"
  → company: nearby organization if found

- education:
  Extract degree, institution, and year range

- skills:
  Extract ALL technical skills from the CV.  
Do NOT skip any skill, even if it appears multiple times or in different sections.  
If a skill is mentioned multiple times, include it ONLY ONCE in the final list (no duplicates).  
If a skill is written in different forms, merge them into one clean standard version (e.g., "A I" → "AI").  
Include all programming languages(like:python, c, c++, java, etc), frameworks(like:django, flask, fastapi, laravel, nodejs, spring, etc), tools (like:git,github,docker, vps, nginx, etc), databases (like:mysql, postgresql, mongodb, etc), platforms (like:aws, azure, google cloud,etc), and technologies(like:html, css, javascript, bootstrap, tailwind, etc).  
Return a complete, unique list of all technical skills found.
  

- soft_skills:
  Extract ONLY human/behavioral (soft) skills from the CV.  
  Do NOT include technical skills under any condition.  
  Do NOT skip any soft skill if it is clearly mentioned anywhere in the CV.  
  If a skill appears multiple times, include it ONLY ONCE in the final list (remove duplicates).  
  If no soft skills are clearly mentioned, return an empty list [].  
  Return a clean, unique list of soft skills only.

- projects:
  Extract:
    title
    description (generate short summary if missing)
    technologies

- certifications:
  Extract courses, competitions, certificates

-notes:
  don't use any title just response intructed json structure

- summary:
  Generate a short professional summary (2–3 lines) based on CV
-story:
  Generate a short professional story based on the given CV. 
  The story should describe the person's journey, skills, and achievements in a natural and engaging way. 
  Keep the tone inspiring and realistic, not fictional or exaggerated. 
  Limit the story to 5–6 sentences maximum. 
  Return only the story, no extra text.
  


CV TEXT:
{text}

OUTPUT FORMAT:
{{
  "skills": [],
  "experience": [],
  "education": [],
  "soft_skills": [],
  "summary": "",
  "story": "",
  "projects": [],
  "certifications": []
}}
"""

    print("processing...")
    client = AsyncClient()
    response = await client.chat(
        model='llama3.2:3b',
        messages=[{'role': 'user', 'content': prompt}],
    )
    print("processing is done")
    return response.message.content
