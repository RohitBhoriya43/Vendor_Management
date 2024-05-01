from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from vendor_api.models import *
from vendor_api.serializers import *
from vendor_api.utils import *
import uuid
from vendor_api.choices import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime,timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication,BasicAuthentication
from django.utils import timezone