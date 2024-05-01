from .imports import *


class UpdateAcknowledgment(APIView):

    authentication_classes =(TokenAuthentication,BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self,request,*args,**kwargs):
        try:
            po_id = kwargs.get('po_id')
            #vendor_id = request.user.vendor_code
            if po_id is None:
                raise ClientSideError("please provide the po_id",status.HTTP_400_BAD_REQUEST)
            
            po_obj = PurchaseOrder.objects.filter(po_number=po_id)
            if not po_obj.exists():
                raise ClientSideError("Purchase order does not exists",status.HTTP_400_BAD_REQUEST)
            po_obj = po_obj.first()
            print(timezone.now())
            po_obj.acknowledgment_date = timezone.now()
            po_obj.save()  
            update_average_response_time_thread(po_obj)      
            return Response(set_response(True,{},'Acknowledgment date is updated'),status.HTTP_200_OK)
        except Exception as e:
            try:
                return Response(set_response(False,{},str(e.message)),e.status)
            except:
                return Response(set_response(False,{},str(e)),status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self,request,*args,**kwargs):
        pass
    def delete(self,request,*args,**kwargs):
        pass