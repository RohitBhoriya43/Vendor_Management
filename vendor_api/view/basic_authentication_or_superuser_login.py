from .imports import *
from django.contrib.auth import get_user_model


class LoginSuperUser(APIView):
    authentication_classes = ()
    permission_classes = ()
    def post(self,request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")

            vendor_obj = Vendors.objects.filter(username=username)
            if not vendor_obj.exists():
                raise ClientSideError("Vendor does not exist",status.HTTP_400_BAD_REQUEST)
            vendor_obj = vendor_obj.first()
            if not vendor_obj.is_superuser:
                raise ClientSideError("This is a not superuser please login as a basic auth",status.HTTP_400_BAD_REQUEST)
            
            if not vendor_obj.check_password(password):
                raise ClientSideError("Invalid Credentials",status.HTTP_400_BAD_REQUEST)
            
            token = generate_token(vendor_obj)
            return Response(set_response(True,{},"SuperUser login successfully",token))

        except Exception as e:
            try:
                return Response(set_response(False,{},str(e.message)),e.status)
            except:
                return Response(set_response(False,{},str(e)),status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        

class CreateBasicAuthentication(APIView):
    authentication_classes = ()
    permission_classes = ()
    def post(self,request):
        try:
            print(request.data)
            username = request.data.get("username")
            password = request.data.get("password")
            

            if not username or not password:
                raise ClientSideError("Please provide a username,password",status.HTTP_400_BAD_REQUEST)

            User = get_user_model()
            user_obj = User.objects.filter(username = username)
            if user_obj.exists():
                raise ClientSideError("This username is already exists",status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.create_user(username=username,password=password)
            user.save()

            return Response(set_response(True,{},"Basic authentication user is created"))

        except Exception as e:
            try:
                return Response(set_response(False,{},str(e.message)),e.status)
            except:
                return Response(set_response(False,{},str(e)),status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        

        
        