from .models import Images
from rest_framework import serializers, viewsets

class ImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = '__all__'

class ImagesViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer