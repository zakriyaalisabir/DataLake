import os
import base64
import boto3

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files import File
from django_server import settings


from .models import RawDataFile
from .serializers import RawDataFileSerializer


def ResponseParser(res):  # TODO
    return res


def ResponseBuilder(data, status, error=False):
    if error:
        return Response({"error": data}, status=status)
    return Response({"result": data}, status=status)


class DatalakeViews(APIView):
    def get(self, request):
        rawdata = RawDataFile.objects.all()
        serializer = RawDataFileSerializer(rawdata, many=True)
        return Response({"result": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        filename_req = request.data.get('file')
        # filename_req = request.POST.get('file')

        if not filename_req:
            return Response({"error": "A filename is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        size = request.POST.get('fileSize')
        type_ = request.POST.get('fileType')

        data = {"file_data": filename_req}

        if filename_req:
            session = boto3.session.Session(aws_access_key_id=settings.
                                            AWS_ACCESS_KEY_ID,
                                            aws_secret_access_key=settings.
                                            AWS_SECRET_ACCESS_KEY)
            s3 = session.resource('s3')
            s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
                Key=filename_req.name, Body=filename_req)

            return Response(data, status=status.HTTP_200_OK)

        return Response({"error": "Object persistance failed"},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
