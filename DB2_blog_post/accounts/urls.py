from .views import (Signup, SignIn, SignOut,
                    Activate, UserDetail, EmailVerificationNotice)
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('sign-up/', Signup.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('activate/<str:uid>/<str:token>', Activate.as_view(), name='activate'),
    path('verification-notice/',
         EmailVerificationNotice.as_view(), name='notice'),
    path('my-account/', UserDetail.as_view(), name='detail'),
]
