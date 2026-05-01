from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from pypdf import PdfReader

from .serializers import CvUploadSerializer
from .utils import (
    fix_spaced_text,
    extract_regex_phone_email,
    
)

from .npl import nlp


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

        doc = nlp(text)

        skills = []
        experience = []
        education = []
        soft_skills = []
        address = []
        name= ""

        for ent in doc.ents:
            if ent.label_ == "SKILL":
                skills.append(ent.text)

            elif ent.label_ == "EXPERIENCE":
                experience.append(ent.text)

            elif ent.label_ == "EDUCATION":
                education.append(ent.text)

            elif ent.label_ == "SOFT_SKILL":
                soft_skills.append(ent.text)

            elif ent.label_ == "ADDRESS":
                address.append(ent.text)

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