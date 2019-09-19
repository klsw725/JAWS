# from django.shortcuts import render, redirect
# from django.http import Http404
#
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import FileUploadParser
#
# from .models import Images
# from .api import ImagesSerializer
# # Create your views here.
#
# class Upload(APIView):
#     parser_classes = (FileUploadParser,)
#
#     def get_objects(self):
#         return Images.objects.all()
#
#     def get(self):
#         images = self.get_objects()
#         serializer = ImagesSerializer(images)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = ImagesSerializer(request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class UploadDetail(APIView):
#
#     def get_object(self, pk):
#         try:
#             return Images.objects.get(pk=pk)
#         except Images.DoesNotExist:
#             raise Http404
#
#     def delete(self, request, pk):
#         image = self.get_object(pk)
#         image.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)