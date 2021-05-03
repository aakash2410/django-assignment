from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
import datetime


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class UserAPIView(APIView):
    def post(self, request):
        if (request.POST['username'] == '') or (request.POST['username'] is None):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username = request.POST['username'])
        
        if user.exists():
            serializer = UserSerializer(user, many= True)
            return Response(serializer.data, status= status.HTTP_204_NO_CONTENT)
        elif not user.exists():
            user = User.objects.create(**request.POST)
            serializer = UserSerializer(user)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        

class AdvisorAdminAPIView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(username = request.user['username'], is_superuser = True)
        except User.DoesNotExist:
            return Response({"Error": "User does not exist or isn't an admin"}, status = status.HTTP_400_BAD_REQUEST)
        advisor_name = request.POST.get('advisor_name')
        advisor_photo_url = request.POST.get('advisor_photo_url')
        if (advisor_name is None) or (advisor_photo_url is None):
            return Response({"Error": "Fields are missing"}, status = status.HTTP_400_BAD_REQUEST)
        advisor = Advisor.objects.create(advisor_name = advisor_name, advisor_photo_url = advisor_photo_url)
        serializer = AdvisorSerializer(advisor)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AdvisorAdminAPIListView(APIView):
    def get(self, request, user_id):
        users = User.objects.filter(pk = user_id)
        if not users.exists():
            return Response({"Error": "User doesnt exist"}, status=status.HTTP_404_NOT_FOUND)
        advisors = AdvisorUser.objects.filter(user_id__in = users)
        advisors_list = list()

        for advisor in advisors:
            advisors_list.append(advisor.advisor_id)
        serializer = AdvisorSerializer(advisors_list)

        return Response(serializer.data, status=status.HTTP_200_OK)


class BookingAPIView(APIView):
    def post(self, request, user_id, advisor_id):
        advisor_user = AdvisorUser.objects.filter(advisor_id_id = advisor_id, user_id_id = user_id)
        if not advisor_user.exists():
            user = User.objects.filter(pk = user_id)
            advisor = Advisor.objects.filter(pk = advisor_id)
            if not user.exists():
                return Response({"Error":"User doesnt exist"}, status = status.HTTP_400_BAD_REQUEST)
            if not advisor.exists():
                return Response({"Error":"Advisor doesnt exist"}, status = status.HTTP_400_BAD_REQUEST)
            advisor_user = AdvisorUser.objects.create(advisor_id = advisor[0], user_id = user[0])
        
        booking_time = request.POST.get('booking_time')
        if booking_time is None:
            return Response({"Error": "Booking time is not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        booking_time = datetime.datetime(booking_time)
        booking = Bookings.objects.create(advisor_user_id = advisor_user, date_and_time = booking_time)
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class BookedAPIView(APIView):
    def get(self, request, user_id):
        advisor_user = AdvisorUser.objects.filter(user_id_id = user_id)
        if not advisor_user.exists():
            user = User.objects.filter(pk = user_id)
            if not user.exists():
                return Response({"Error":"User doesnt exist"}, status = status.HTTP_400_BAD_REQUEST)
        bookings = Bookings.objects.filter(advisor_user_id = advisor_user)
        serializer = BookingSerializer(bookings)
        return Response(serializer.data, status=status.HTTP_200_OK)


            
