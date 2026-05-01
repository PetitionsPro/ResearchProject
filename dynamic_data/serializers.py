from rest_framework import serializers


class BulkSkillSerializer(serializers.Serializer):
    bulk_skills = serializers.JSONField()

    def validate_bulk_skills(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("bulk_skills must be a list of skill names.")
        for skill in value:
            if not isinstance(skill, str):
                raise serializers.ValidationError("Each skill name must be a string.")
        return value


class BulkEducationSerializer(serializers.Serializer):
    bulk_education = serializers.JSONField()

    def validate_bulk_education(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("bulk_education must be a list of education names.")
        for edu in value:
            if not isinstance(edu, str):
                raise serializers.ValidationError("Each education name must be a string.")
        return value