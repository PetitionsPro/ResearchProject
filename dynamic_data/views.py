from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import BulkSkillSerializer, BulkEducationSerializer
from .models import SkillModel, EducationModel


class BulkSkillCreateView(APIView):
    def post(self, request):
        serializer = BulkSkillSerializer(data=request.data)

        if serializer.is_valid():
            skills = [
                SkillModel(name=name)
                for name in serializer.validated_data["bulk_skills"]
            ]
            SkillModel.objects.bulk_create(skills)

            return Response({"message": "Skills created successfully"}, status=201)

        return Response(serializer.errors, status=400)


class BulkEducationCreateView(APIView):
    def post(self, request):
        serializer = BulkEducationSerializer(data=request.data)

        if serializer.is_valid():
            educations = [
                EducationModel(name=name)
                for name in serializer.validated_data["bulk_education"]
            ]
            EducationModel.objects.bulk_create(educations)

            return Response({"message": "Educations created successfully"}, status=201)

        return Response(serializer.errors, status=400)