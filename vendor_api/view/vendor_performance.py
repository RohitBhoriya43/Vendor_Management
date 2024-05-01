from .imports import *


class VendorPerformance(APIView):

    authentication_classes =(TokenAuthentication,BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args,**kwargs):
        try:
            vendor_id = kwargs.get('vendor_id')
            hp_obj = HistoricalPerformance.objects.filter(vendor__vendor_code = vendor_id)
            if not hp_obj.exists():
                raise ClientSideError("Please provide the vendor_id",status.HTTP_400_BAD_REQUEST)
            
            hp_serializer = HistoricalPerformanceSerializer(hp_obj.first())
            return Response(set_response(True,hp_serializer.data,''),status.HTTP_200_OK)
        except Exception as e:
            try:
                return Response(set_response(False,{},str(e.message)),e.status)
            except:
                return Response(set_response(False,{},str(e)),status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
