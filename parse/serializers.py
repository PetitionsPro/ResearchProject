from rest_framework import serializers

from .models import Candidate_parsed_data

class CvUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are allowed.")
        return value

class CandidateParsedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate_parsed_data
        fields = "__all__"
    

    def __init__(self,*args,**kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)