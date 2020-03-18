import base64
import hashlib
import hmac
import os
import time
from rest_framework import permissions, status, authentication
from rest_framework.response import Response
from rest_framework.views import APIView

from django_server.settings import (
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_S3_BUCKETS)
from .models import FileItem

class
