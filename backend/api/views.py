from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.views import generic
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import HttpResponse

from .models import Profile, Log
from django.contrib.auth.models import User

@api_view(['GET'])
def get_data(request):
    # do something to fetch token
    return Response({'adam': 'markon', 'phil': 'windmueller'})


@api_view(['GET','POST'])
def create_account(request):
    newUserInfo = request.data
    user = User.objects.create_user(username = newUserInfo['newUsername'], 
        password = newUserInfo['newPassword'])
    user.save()
    userID = user.id
    profile = Profile.objects.get(user_id = userID)
    profile.facebook_email = newUserInfo['newFacebookEmail']
    profile.save()
    return Response({'Account has been added'})




# def LoginPage(request):
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         return HttpResponse("Hello, world. You're at the polls index.")
#         # login(request, user)
#         # Redirect to a success page.
#     else:
#         return HttpResponse("Hello, world. You're at the polls index.")
#         # Return an 'invalid login' error message.