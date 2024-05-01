from .imports import *


class PurchaseOrderTracking(APIView):

    authentication_classes=(TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args,**kwargs):
        try:
            po_id = kwargs.get('po_id')
            vendor_code =request.user.vendor_code
            if vendor_code is None:
                raise ClientSideError("Please provide the valid vendor token",status.HTTP_401_UNAUTHORIZED)
                
            print(vendor_code)
            if po_id is None:
                print(vendor_code)

                po_obj = PurchaseOrder.objects.filter(vendor__vendor_code= vendor_code)
                po_serializer = PurchaseOrderSerializer(po_obj,many=True)
            else:
                po_obj = PurchaseOrder.objects.filter(po_number = po_id,vendor__vendor_code= vendor_code)
                if not po_obj.exists():
                    raise ClientSideError("Purchase order does not exists",status.HTTP_400_BAD_REQUEST)
                po_serializer = PurchaseOrderSerializer(po_obj.first())
                
            
            return Response(set_response(True,po_serializer.data,""),status.HTTP_200_OK)
        except Exception as e:
            try:
                return Response(set_response(False,{},str(e.message)),e.status)
            except:
                return Response(set_response(False,{},str(e)),status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def post(self,request,*args,**kwargs):
        try:            
            vendor_code =request.user.vendor_code
            if vendor_code is None:
                raise ClientSideError("Please provide the valid vendor token",status.HTTP_401_UNAUTHORIZED)
                
            data = request.data
            items = data.get("items")
            quantity = data.get("quantity")

            po_number = f"po_{str(uuid.uuid4()).replace('-','')}"
            vendor_obj = request.user

            po_obj = PurchaseOrder()
            po_obj.po_number = po_number
            po_obj.vendor = vendor_obj
            po_obj.quantity = quantity
            po_obj.items = items
            po_obj.delivery_date = timezone.now() + timezone.timedelta(days=3)



            po_obj.save()
            print(po_obj)
            update_metrics_thread_start(po_obj)
            return Response(set_response(True,{},"New Purchase order created"),status.HTTP_200_OK)
        except Exception as e:
            try:
                return Response(set_response(False,{},str(e.message)),e.status)
            except:
                return Response(set_response(False,{},str(e)),status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        
    def put(self,request,*args,**kwargs):
        try:
            po_id = kwargs.get('po_id')
            vendor_code =request.user.vendor_code
            if vendor_code is None:
                raise ClientSideError("Please provide the valid vendor token",status.HTTP_401_UNAUTHORIZED)
                
            if po_id is None:
                raise ClientSideError("please provide the po_id",status.HTTP_400_BAD_REQUEST)

            po_obj = PurchaseOrder.objects.filter(po_number=po_id,vendor__vendor_code=vendor_code)

            if not po_obj.exists():
                raise ClientSideError("Purchase order does not exists",status.HTTP_400_BAD_REQUEST)
            data = check_field_data(request.data)
            po_obj,po_obj_created=PurchaseOrder.objects.update_or_create(po_number=po_id,vendor__vendor_code=vendor_code,defaults= data)
            po_obj.save()
            update_metrics_thread_start(po_obj)                    
            return Response(set_response(True,{},"Purchase order is updated"),status.HTTP_200_OK)
        except Exception as e:
            try:
                return Response(set_response(False,{},str(e.message)),e.status)
            except:
                return Response(set_response(False,{},str(e)),status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self,request,*args,**kwargs):
        try:
            vendor_code = request.user.vendor_code
            if vendor_code is None:
                raise ClientSideError("Please provide the valid vendor token",status.HTTP_401_UNAUTHORIZED)
                
            po_id = kwargs.get('po_id')
            if po_id is None:
                raise ClientSideError("please provide the po_id",status.HTTP_400_BAD_REQUEST)
            
            po_obj = PurchaseOrder.objects.filter(po_number = po_id)
            if not po_obj.exists():
                raise ClientSideError("Purchase order does not exists",status.HTTP_400_BAD_REQUEST)
            po_obj=po_obj.first()
            instance = po_obj
            po_obj.delete()
            update_metrics_thread_start(instance)
            return Response({},status.HTTP_200_OK)
        except Exception as e:
            try:
                return Response(set_response(False,{},str(e.message)),e.status)
            except:
                return Response(set_response(False,{},str(e)),status.HTTP_500_INTERNAL_SERVER_ERROR)
    


def check_field_data(data):
    default_data = {}

    items = data.get("items")
    quantity = data.get("quantity")
    quality_rating = data.get("quality_rating")
    status = data.get("status")
    delivery_date = data.get("delivery_date")
    acknowledgment_date = data.get("acknowledgment_date")

    if quantity is not None:
        default_data["quantity"] = int(quantity)
    if quality_rating is not None:
        default_data["quality_rating"] = float(quality_rating)
        default_data["acknowledgment_date"] = timezone.now()
        default_data["status"] = PurchaseOrderStatus.completed
    if status is not None and (status.lower() == PurchaseOrderStatus.completed or status.lower() == PurchaseOrderStatus.canceled):
        default_data["status"] = status.lower()
    if delivery_date is not None:
        default_data["delivery_date"] = timezone.now()
    if acknowledgment_date is not None:
        default_data["acknowledgment_date"] = timezone.now()
    
    
    return default_data