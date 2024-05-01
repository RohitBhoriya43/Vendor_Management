import re

from vendor_api.signals import update_average_response_time, update_historical_performance_and_vendor_metrics
from .choices import *
from datetime import timedelta
from django.utils import timezone
from rest_framework.authtoken.models import Token
import threading
from rest_framework import status



def set_response(success,data,message,token=None):
    return {
        "success":success,
        "message":message,
        "data":data,
        "token":token,
    }

def check_status(status):
    if status is None:
        return status
    try:
        return PurchaseOrderStatus[status.lower()]
    except Exception as e:
        raise Exception("Please provide the status is (pending,completed,canceled)")
    

def generate_token(vendor_obj):
    try:
        token = Token.objects.get(user=vendor_obj)
        # if token.expires_at < timezone.now():
        #     token.delete()
        #     token = Token.objects.create(user=vendor_obj)
        #     token.expires_at = timezone.now()+timedelta(hours=1)
        #     token.save()
        #     return token.key
        # else:
        #     return token.key
        return token.key
    except:
        token = Token.objects.create(user=vendor_obj)
        token.expires_at = timezone.now()+timedelta(hours=1)
        token.save()
        return token.key
    
def update_metrics_threading(instance):

    update_historical_performance_and_vendor_metrics(None,instance)

def update_metrics_thread_start(instance):
    print(instance)
    thread = threading.Thread(target=update_metrics_threading,args=(instance,))
    print(thread)
    thread.start()


def update_acknowledge(instance):

    update_average_response_time(None,instance)

def update_average_response_time_thread(instance):
    print(instance)
    thread = threading.Thread(target=update_acknowledge,args=(instance,))
    print(thread)
    thread.start()


class ClientSideError(Exception):
    def __init__(self,message,status):
        self.message = message
        self.status = status
        
class ServerSideError(Exception):
    def __init__(self,message,status):
        self.message = message
        self.status = status



def check_name(name):
    if name == "":
        return name
    pattern = r'^[A-Za-z\s]+$'

    if re.match(pattern, name):
        return name
    else:
        raise ClientSideError("Special character not provide in name",status.HTTP_400_BAD_REQUEST)



def check_number(contact_obj):
    pattern = r'^[0-9]{10}$'
    number1 = contact_obj[0]
    number2 = contact_obj[len(contact_obj)-1]
    if re.match(pattern, number1):
        return number1
    elif re.match(pattern, number2):
        return number2
    else:
        raise ClientSideError("Please provide the mobile number in contact_details (0000000000,asddsff,kkkl) or (asdfg,sdfg,0000000000)",status.HTTP_400_BAD_REQUEST) 



