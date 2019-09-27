import os
import _io
from django.conf import settings

from .models import Images
from rest_framework import serializers, viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

import cv2
import face_recognition
import PIL.Image
import numpy

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
        data = self.recogFace(request.data["image"])
        if data != False:
            request.data["image"].file = data
            serializer = ImagesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("No Face detect", status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        image = Images.objects.get(pk=pk)
        image.delete()
        os.remove('{0}/{1}'.format(settings.MEDIA_ROOT, str(image.image)))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def Rotate(self, src, degrees):
        if degrees == 90:
            dst = cv2.transpose(src)
            dst = cv2.flip(dst, 1)

        elif degrees == 180:
            dst = cv2.flip(src, -1)

        elif degrees == 270:
            dst = cv2.transpose(src)
            dst = cv2.flip(dst, 0)
        else:
            dst = src
        return dst

    def recogFace(self, data):
        print("recog face start")
        image = data
        temp_image = face_recognition.load_image_file(image)

        num = 0
        for i in range(4):
            try:
                face_recognition.face_encodings(temp_image)[0]
            except:
                num = num + 90
                temp_image = self.Rotate(temp_image, num)
            else:
                im = PIL.Image.open(image)
                imageNDArray = cv2.cvtColor(numpy.array(im), cv2.COLOR_RGB2BGR)
                imageNDArray = self.Rotate(imageNDArray, num)
                imageNDArray = cv2.resize(imageNDArray, dsize=(480, 640), interpolation=cv2.INTER_AREA)
                is_success, im_buf_arr = cv2.imencode(".jpg", imageNDArray)
                byte_im = im_buf_arr.tobytes()
                temp = _io.BytesIO(byte_im)
                # cv2.imwrite(image, imageNDArray)
                return temp
        return False