from django.shortcuts import render, redirect

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser

from .models import Images
from .api import ImagesSerializer

# Create your views here.

class Upload(APIView):
    parser_classes = (FileUploadParser,)

    def get_object(self):
        return Images.objects.all()

    def get(self, request):
        images = self.get_object()
        serializer = ImagesSerializer(images)
        return Response(serializer.data)

    def post(self, request):
        serializer = ImagesSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)