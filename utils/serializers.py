from rest_framework.serializers import Serializer, IntegerField


class FamilyRequiredSerializer(Serializer):
    family = IntegerField()

    def create(self, validated_data):
        print(validated_data.family)
        return None

    def update(self, instance, validated_data):
        return instance
