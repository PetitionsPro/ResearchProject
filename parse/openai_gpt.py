from openai import OpenAI

from django.conf import settings

OPENAI_API_KEY=settings.OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)





def open_ai_api_call(text):
    prompt=f"""Analyze the following text extracted from a user’s resume or CV. Using this information, generate a compelling and powerful story in exactly 5 sentences that highlights the user’s achievements, skills, growth, and impact. The tone should be confident, inspiring, and professional, transforming the raw details into a strong narrative of success and progress.
    Return only valid JSON output with no extra text, using this structure:
    "story": "Your generated story"
     Resume Text:
    "{text}" 
    """
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

