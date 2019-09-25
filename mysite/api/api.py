import os
from django.conf import settings

from .models import Images
from rest_framework import serializers, viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

import cv2
import face_recognition

# temp_image = face_recognition.load_image_file(location)
# try:
# # temp_image_encoding = face_recognition.face_encodings(temp_image)[0]
# catch:

class ImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = '__all__'

class ImagesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer

    # def create(self, request):
    #     temp_image = face_recognition.load_image_file(request.data['image'])
    #     height, width, channel = temp_image.shape
    #     for i in range(4):
    #         try:
    #             face_recognition.face_encodings(temp_image)[0]
    #         except:
    #             matrix = cv2.getRotationMatrix2D((width/2, height/2), 90, 1)
    #             temp_image = cv2.warpAffine(temp_image, matrix, (width, height))
    #         else:
    #             serializer = ImagesSerializer(data=request.data)
    #             if serializer.is_valid():
    #                 serializer.save()
    #                 return Response(serializer.data, status=status.HTTP_201_CREATED)
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = ImagesSerializer(data=request.data)
        if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        image = Images.objects.get(pk=pk)
        image.delete()
        os.remove('{0}/{1}'.format(settings.MEDIA_ROOT, str(image.image)))
        return Response(status=status.HTTP_204_NO_CONTENT)






