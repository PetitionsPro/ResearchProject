import asyncio
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import json

from pypdf import PdfReader

from .serializers import CvUploadSerializer
from .utils import (
    fix_spaced_text,
    extract_regex_phone_email,anonimize_personal_info
    
)

from .npl import get_nlp


class CvUploadView(APIView):

    def post(self, request, format=None):
        serializer = CvUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        file = serializer.validated_data['file']

        reader = PdfReader(file)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

      
        text = fix_spaced_text(text)


        phone_email = extract_regex_phone_email(text)

        phones = phone_email.get("phone", [])
        emails = phone_email.get("email", [])
    

        


        print("Extracted Phones:", phones)
        print("Extracted Emails:", emails)

        nlp = get_nlp()
        
        skills = []
        experience = []
        education = []
        soft_skills = []
        address = []
        name = ""

     
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        for i, line in enumerate(lines):
            doc = nlp(line)
            
            for ent in doc.ents:
                if ent.label_ == "SKILL":
                    skills.append(ent.text)

                elif ent.label_ == "EXPERIENCE":
                    
                    if len(line) > 5:
                        experience.append(line)

                elif ent.label_ == "EDUCATION":
                    if len(line) > 5:
                        education.append(line)

                elif ent.label_ == "SOFT_SKILL":
                    soft_skills.append(ent.text)

                elif ent.label_ in ["ADDRESS", "GPE", "LOC"]:
                    invalid_addresses = ["PROJECTS", "EDUCATION", "SKILLS", "CGPA", "LINKEDIN", "GITHUB", "REACT", "REDUX", "PORTFOLIO"]
                    if not any(inv in ent.text.upper() for inv in invalid_addresses):
                        address.append(ent.text)

            
                pass

        if not name and lines:
            invalid_name_keywords = ["RESUME", "CURRICULUM", "VITAE", "DEVELOPER", "ENGINEER", "EMAIL", "PHONE", "ADDRESS", "REACT", "PORTFOLIO", "PROFILE"]
            for line in lines[:8]:  
                clean_line = line.strip()
                words = clean_line.split()
                
            
                if 1 <= len(words) <= 4:
                    if any(char.isdigit() or char in "@#$%" for char in clean_line):
                        continue
                        
                    
                    if any(keyword in clean_line.upper() for keyword in invalid_name_keywords):
                        continue
                        
                    
                    if all(word.replace('.', '').replace('-', '').isalpha() for word in words):
                        name = clean_line
                        break

        result = {
            "name": name,
            "phone": phones,
            "email": emails,
            "skills": list(set(skills)),
            "experience": list(set(experience)),
            "education": list(set(education)),
            "soft_skills": list(set(soft_skills)),
            "address": list(set(address)),
        }

        return Response(result, status=200)
