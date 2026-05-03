import asyncio
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import json

from pypdf import PdfReader


from .serializers import CvUploadSerializer, CandidateParsedDataSerializer
from .utils import fix_spaced_text, extract_regex_phone_email, anonimize_personal_info,decrypt_personal_info
from .npl import get_nlp
from .openai_gpt import open_ai_api_call
from .models import Candidate_parsed_data
from rest_framework import permissions
from .services.crypto import generate_blind_index
from .services.masking import mask_emails, mask_phones, mask_addresses

class CvUploadView(APIView):

    permission_classes = [permissions.IsAuthenticated]

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
                    invalid_addresses = ["PROJECTS", "EDUCATION", "SKILLS", "CGPA", "LINKEDIN", "GITHUB", "REACT", "REDUX", "PORTFOLIO","Express.js","Node.js","MERN","MEAN","LAMP","Django","Flask","Spring Boot","Ruby on Rails","Laravel","ASP.NET"]
                    if not any(inv in ent.text.upper() for inv in invalid_addresses):
                        address.append(ent.text)

            
                pass

        # if not name and lines:
        #     invalid_name_keywords = ["RESUME", "CURRICULUM", "VITAE", "DEVELOPER", "ENGINEER", "EMAIL", "PHONE", "ADDRESS", "REACT", "PORTFOLIO", "PROFILE"]
        #     for line in lines[:8]:  
        #         clean_line = line.strip()
        #         words = clean_line.split()
                
            
        #         if 1 <= len(words) <= 4:
        #             if any(char.isdigit() or char in "@#$%" for char in clean_line):
        #                 continue
                        
                    
        #             if any(keyword in clean_line.upper() for keyword in invalid_name_keywords):
        #                 continue
                        
                    
        #             if all(word.replace('.', '').replace('-', '').isalpha() for word in words):
        #                 name = clean_line
        #                 break

        result = {
            "phone": phones,
            "email": emails,
            "skills": list(set(skills)),
            "experience": list(set(experience)),
            "education": list(set(education)),
            "soft_skills": list(set(soft_skills)),
            "address": list(set(address)),
        }
        payload={
            "name": name,
            "phone": phones,
            "email": emails,
            "address": list(set(address)),
        }
        anonimized_data=anonimize_personal_info(payload)
        if payload['email']:
            payload['email']=payload['email'][0]
        if payload['phone']:
            payload['phone']=payload['phone'][0]
        if payload['address']:
            payload['address']=payload['address'][0]
       
        email_idx=generate_blind_index(payload['email'])
        phone_idx=generate_blind_index(payload['phone'])
        address_idx=generate_blind_index(payload['address'])
        print("Anonymous Data:", anonimized_data)


        candidate_parsed_data=Candidate_parsed_data.objects.create(
            user=request.user,
            name=anonimized_data['name'],
            email=anonimized_data['email'],
            email_idx=email_idx,
            phone=anonimized_data['phone'],
            phone_idx=phone_idx,
            address=anonimized_data['address'],
            address_idx=address_idx,
            skills=", ".join(result['skills']),
            experience=", ".join(result['experience']),
            education=", ".join(result['education']),
            soft_skills=", ".join(result['soft_skills']),
            resume=file
        )




        exclude_keys=["name","phone","email","address"]



        excludee_personal_info={k:v for k,v in result.items() if k not in exclude_keys}
        print(excludee_personal_info)

        story=open_ai_api_call(excludee_personal_info)

        if story:
            story=json.loads(story)
            candidate_parsed_data.story=story.get("story")
            candidate_parsed_data.save()

        print(story.get("story"))

        return Response({"story":story.get("story")}, status=200)






from .serializers import CvUploadSerializer, CandidateParsedDataSerializer

class StoryDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Candidate_parsed_data.objects.all().order_by('-created_at').only('id', 'story', 'resume')
        return Candidate_parsed_data.objects.filter(user=user).order_by('-created_at').only('id', 'story', 'resume')
    
    def get(self, request, format=None):
        candidate_parsed_data = self.get_queryset()
        serializer = CandidateParsedDataSerializer(candidate_parsed_data, many=True)
        return Response(serializer.data, status=200)    


        
from django.db.models import Q

class UserSearchAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]
    

    def get(self, request):
        search_query = request.query_params.get('search', '').strip('"')

        queryset = Candidate_parsed_data.objects.all()

        if search_query:
            queryset = queryset.filter(
                Q(story__icontains=search_query)
            )

        serializer = CandidateParsedDataSerializer(queryset, many=True)

        data = serializer.data
        decrypt_personal_info_list = {"name": [], "phone": [], "email": [], "address": []}
        for item in data:
            decrypt_personal_info_list["name"].append(item.get("name"))
            decrypt_personal_info_list["phone"].append(item.get("phone"))
            decrypt_personal_info_list["email"].append(item.get("email"))
            decrypt_personal_info_list["address"].append(item.get("address"))
            
        data_with_personal_info = decrypt_personal_info(decrypt_personal_info_list)

        emails=data_with_personal_info.get("email", [])
        phones=data_with_personal_info.get("phone", [])
        addresses=data_with_personal_info.get("address", [])

        masked_emails=mask_emails(emails)
        masked_phones=mask_phones(phones)
        masked_addresses=mask_addresses(addresses)

        masked_data_personal_info={
            "email": masked_emails,
            "phone": masked_phones,
            "address": masked_addresses
        }

        return Response(masked_data_personal_info, status=200)




class StorySearchByEmailOrPhone(APIView):
    permission_classes= [permissions.IsAdminUser]
    def get(self,request):
        search_query=request.query_params.get('search','').strip('"')
        idx=generate_blind_index(search_query)
    
        queryset=Candidate_parsed_data.objects.filter(
            Q(email_idx=idx) |
            Q(phone_idx=idx)
        )
        print(queryset)
        serializer=CandidateParsedDataSerializer(queryset,many=True,fields=['id','story','resume'])
        return Response(serializer.data,status=200)
        