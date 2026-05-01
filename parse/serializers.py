from rest_framework import serializers

def extract_regex(text):
    return {
        "email": re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+", text),
        "phone": re.findall(r"\+?\d{10,15}", text),
    }

class CvUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are allowed.")
        return value
