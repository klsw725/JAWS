import os
import _io
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http.request import QueryDict


from rest_framework import serializers, viewsets, status, mixins, permissions
from rest_framework.response import Response
from knox.models import AuthToken

import cv2
import face_recognition
import PIL.Image
import numpy
import datetime
import pickle

from .models import Images, Device
from .serializers import (
    SignupUserSerializer,
    UserSerializer,
    LoginUserSerializer,
    ImagesSerializer
)


class ImagesViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
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

    def list(self, request):
        if not Images.objects.filter(owner=request.user).exists():
            queryset = None

        queryset = Images.objects.filter(owner= request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = self.recogFace(request.data["image"])
        if data != False:
            request.data["image"].file = data
            # with open('james.p', 'wb') as file:
            #     pickle.dump(encodings_data, file)
            encoding_file = '{0}/{1}'.format(settings.BASE_DIR, 'encodings/temp.pkl')
            suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
            filename = "{0}_{1}".format(request.user, suffix)
            encoding_rename = '{0}/{1}/{2}'.format(settings.BASE_DIR, 'encodings', filename)
            os.rename(encoding_file, encoding_rename)

            serializer = ImagesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=request.user, encoding=encoding_rename)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "No Face detect"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        image = Images.objects.get(pk=pk)
        os.remove(str(image.encoding))
        os.remove('{0}/{1}'.format(settings.MEDIA_ROOT, str(image.image)))
        image.delete()
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
                encodings_image = face_recognition.face_encodings(temp_image)[0]
            except:
                num = num + 90
                temp_image = self.Rotate(temp_image, num)
            else:
                with open('{0}/{1}'.format(settings.BASE_DIR, 'encodings/temp.pkl'), 'wb') as file:
                    pickle.dump(encodings_image, file)
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

class SignupViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignupUserSerializer

    def create(self, request):
        # if len(request.data["userid"]) < 6 or len(request.data["userpw"]) < 4:
        #     body = {"message": "short field"}
        #     return Response(body, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=request.data["username"]).exists():
            body = {"message": "이미 있는 아이디 입니다. 다른 아이디를 사용해 주세요"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)

        if not Device.objects.filter(devicecode=request.data["devicecode"]).exists():
            body = {"message": "This is Not our Device"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)

        device = Device.objects.get(devicecode=request.data["devicecode"])
        if device.owner:
            body = {"message": "This is Not Your Device"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)

        serializer = SignupUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            device.owner = User.objects.get(id=serializer.data["id"])
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = LoginUserSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            return Response(
                {
                    "user": UserSerializer(
                        user, context=self.get_serializer_context()
                    ).data,
                    "token": AuthToken.objects.create(user)[1],
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer


