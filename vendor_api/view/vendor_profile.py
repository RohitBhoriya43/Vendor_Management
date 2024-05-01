from .imports import *



class VendorProfileManagement(APIView):

    authentication_classes=(BasicAuthentication,TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args,**kwargs):
        try:
            print(request.user.vendor_code)
            if request.user.vendor_code is not None:
                raise ClientSideError("please provide the basic or superuser token",status.HTTP_401_UNAUTHORIZED)
            
            vendor_id = kwargs.get('vendor_id')
            print(request.headers)
            #print(request.headers.get("Authorization"))
            token= None
            if vendor_id is None:
                vendor_obj = Vendors.objects.filter(vendor_code__isnull = False)
                vendor_serializer = VendorSerializer(vendor_obj,many=True)
            else:
                vendors_obj = Vendors.objects.filter(vendor_code = vendor_id)
                if not vendors_obj.exists():
                    raise ClientSideError("Vendor does not exist",status.HTTP_400_BAD_REQUEST)

                vendor_serializer = VendorSerializer(vendors_obj.first())
                token = generate_token(vendors_obj.first())
            return Response(set_response(True,vendor_serializer.data,"",token),status.HTTP_200_OK)
        except Exception as e:
            try:
                return Response(set_response(False,{},str(e.message)),e.status)
            except:
                return Response(set_response(False,{},str(e)),status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self,request,*args,**kwargs):
        try:
            if request.user.vendor_code is not None:
                raise ClientSideError("please provide the basic or superuser token",status.HTTP_401_UNAUTHORIZED)
            
            data = request.data
            name = check_name(data.get("name").strip())
            contact_details = data.get("contact_details")
            address = data.get("address")

            contact_obj = contact_details.split(",")

            contact_number = check_number(contact_obj)

            vendor_obj = Vendors.objects.filter(contact_details__icontains =contact_number)

            if vendor_obj.exists():
                raise ClientSideError("Vendor already exists",status.HTTP_400_BAD_REQUEST)
            else:
                vendor_code = f"vendor_{str(uuid.uuid4()).replace('-','')}"
                vendor_obj = Vendors.objects.create(name= name,contact_details=contact_details,address=address,vendor_code=vendor_code)
                vendor_obj.save()
            
            return Response(set_response(True,{},'New vendor is created'))
             
        except Exception as e:
            try:
                return Response(set_response(False,{},str(e.message)),e.status)
            except:
                return Response(set_response(False,{},str(e)),status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self,request,*args,**kwargs):
        try:
            if request.user.vendor_code is not None:
                raise ClientSideError("please provide the basic or superuser token",status.HTTP_401_UNAUTHORIZED)
            
            vendor_id = kwargs.get("vendor_id")
            if vendor_id is None:
                raise ClientSideError("Please provide the vendor_id",status.HTTP_400_BAD_REQUEST)
            vendor_obj = Vendors.objects.filter(vendor_code = vendor_id)
            if not vendor_obj.exists():
                raise ClientSideError("Vendor does not exists",status.HTTP_400_BAD_REQUEST)
            data = request.data
            name = check_name(data.get("name","").strip())
            contact_details = data.get("contact_details","")
            address = data.get("address","")

            vendor_obj = vendor_obj.first()

            if name != "":
                vendor_obj.name = name
            contact_obj = contact_details.split(",")

            contact_number =  "" if len(contact_obj) == 1 and contact_obj[0] == "" else check_number(contact_obj)
            if name != "":
                vendor_contact_obj = Vendors.objects.filter(contact_details__icontains =contact_number)

                if vendor_contact_obj.exists():
                    raise ClientSideError("Vendor already exists",status.HTTP_400_BAD_REQUEST)
                
                vendor_obj.contact_details = contact_details
            
            if address != "":

                vendor_obj.address = address

            

            vendor_obj.save()


            return Response(set_response(True,{},"Vendor detail updated"),status.HTTP_200_OK)             

        except Exception as e:
            try:
                return Response(set_response(False,{},str(e.message)),e.status)
            except:
                return Response(set_response(False,{},str(e)),status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self,request,*args,**kwargs):
        try:
            if request.user.vendor_code is not None:
                raise ClientSideError("please provide the basic or superuser token",status.HTTP_401_UNAUTHORIZED)
            
            vendor_id = kwargs.get('vendor_id')
            if vendor_id is None:
                return Response({},status.HTTP_400_BAD_REQUEST)
            
            vendor_obj = Vendors.objects.filter(vendor_code = vendor_id)
            if not vendor_obj.exists():
                raise ClientSideError("Vendor does not exist",status.HTTP_400_BAD_REQUEST)
            vendor_obj=vendor_obj.first()
            vendor_obj.delete()
            return Response({},status.HTTP_200_OK)
        except Exception as e:
            try:
                return Response(set_response(False,{},str(e.message)),e.status)
            except:
                return Response(set_response(False,{},str(e)),status.HTTP_500_INTERNAL_SERVER_ERROR)
    