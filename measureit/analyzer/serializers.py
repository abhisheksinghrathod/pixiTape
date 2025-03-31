from rest_framework import serializers

class MeasureInputSerializer(serializers.Serializer):
    pixel_to_mm_ratio = serializers.FloatField()
    image = serializers.ImageField()