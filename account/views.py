from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import TrainingCalendar , course , certificate , TestModel
from .serializers import *
from django.contrib.auth import authenticate
from .renderers import UserRenderer  # Adjust import path for UserRenderer if necessary
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny  # Import AllowAny
from .models import User  # Import User model
from rest_framework.generics import ListAPIView , CreateAPIView , UpdateAPIView , DestroyAPIView

# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]  # Allow any user to register
    
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    permission_classes = [AllowAny]  # Allow any user to attempt login
    
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication for user profile view
    
    renderer_classes = [UserRenderer]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication to change password
    
    def put(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
    permission_classes = [AllowAny]  # Allow any user to request password reset
    
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
    permission_classes = [AllowAny]  # Allow any user to reset password
    
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)

class UserList(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication for user list view
    
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication to update user profile
    
    def put(self, request, format=None):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrainingCalendarList(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        training_calendars = TrainingCalendar.objects.all()
        serializer = TrainingCalenderSerializer(training_calendars, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = TrainingPostCalenderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
class TestTrain(UpdateAPIView , DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrainingPostCalenderSerializer

    def get_object(self):
        # Assuming 'pk' is passed in URL kwargs
        pk = self.kwargs.get('pk')
        return TrainingCalendar.objects.get(pk=pk)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CourseList(ListAPIView, CreateAPIView):
    queryset = course.objects.all()  # Assuming 'course' is the name of your model
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method == 'GET':  # If it's a GET request (list view)
            permission_classes = [AllowAny]
        else:  # For any other request (create view)
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class CertificateList(ListAPIView , CreateAPIView):
    queryset = certificate.objects.all()
    serializer_class = CertificateSerializer
    def get_permissions(self):
        if self.request.method == 'GET':  # If it's a GET request (list view)
            permission_classes = [AllowAny]
        else:  # For any other request (create view)
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    

class csList(ListAPIView, CreateAPIView):
    permission_classes = [AllowAny]
    queryset = TestModel.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TestModelPostSerializer
        return TestModelSerializer