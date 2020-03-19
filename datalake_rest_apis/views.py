from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import RawDataFile
from .serializers import RawDataFileSerializer


def ParseResponse(res):
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
        serializer = RawDataFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
