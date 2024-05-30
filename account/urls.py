from django.urls import path
from account.views import SendPasswordResetEmailView, UserChangePasswordView, UserLoginView, UserProfileView, UserRegistrationView, UserPasswordResetView , UserProfileUpdateView ,TrainingCalendarList , TestTrain , CourseList , CertificateList , csList
from rest_framework_simplejwt.views import  TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('update_profile/', UserProfileUpdateView.as_view(), name='update_profile'),
    path('Courses/', CourseList.as_view(), name='Courses'),
    path('csList/', csList.as_view(), name='csList'),
    path('Certificate/', CertificateList.as_view(), name='Certificates'),
    path('training_calender/', TrainingCalendarList.as_view(), name='training_calender'),
    path('training-calendars/<int:pk>/', TestTrain.as_view(), name='training_calender'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path("token/" , TokenObtainPairView.as_view()  , name="token_obtain_pair"),
    path("token/refresh/" , TokenRefreshView.as_view()  , name="token_refresh"),

]