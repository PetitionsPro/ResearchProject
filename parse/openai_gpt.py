from openai import OpenAI

from django.conf import settings

OPENAI_API_KEY=settings.OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)





def open_ai_api_call(text):
    prompt = f"""
You are a professional career storyteller.

Task:
Transform the given resume text into a compelling career story.

Story Requirements:
- Write exactly 5 sentences (no more, no less).
- Use a confident, inspiring, and professional tone.
- Focus on achievements, technical skills, growth, and real impact.
- Make the story flow naturally like a short narrative (not bullet points).
- Avoid vague or generic phrases.
- Do NOT invent information that is not in the text.

Output Rules:
- Return ONLY valid JSON.
- No explanations, no extra text.
- Follow this exact structure:

{{"story": "Sentence 1. Sentence 2. Sentence 3. Sentence 4. Sentence 5."}}

Resume Text:
\"\"\"{text}\"\"\"
"""
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

