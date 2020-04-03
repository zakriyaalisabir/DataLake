import boto3
import json
import calendar
import time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
        serializer = RawDataFileSerializer(rawdata, many=True).data

        result = {
            "counts": len(serializer),
            "data": serializer
        }
        return Response({"result": result}, status=status.HTTP_200_OK)

    def post(self, request):
        file_obj = request.data.get('file')

        if not file_obj:
            return Response({"error": "A file object is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        fName, fType = str(file_obj.name).split('.')

        data = {
            "file_meta_data": {
                "title": fName,
                "file_type": fType
            }
        }

        session = boto3.session.Session(aws_access_key_id=settings.
                                        AWS_ACCESS_KEY_ID,
                                        aws_secret_access_key=settings.
                                        AWS_SECRET_ACCESS_KEY)
        s3 = session.resource('s3')
        s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
            Key=fType+'/file'+'.'+fType,
            Body=file_obj)

        return Response({"result": data},
                        status=status.HTTP_200_OK)
