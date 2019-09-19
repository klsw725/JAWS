from .models import Images
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

class ImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = '__all__'

class ImagesViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer

    @action(detail=True, methods=['delete'])
    def delete_image(self, request, pk=None):
        image = self.get_object(pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



