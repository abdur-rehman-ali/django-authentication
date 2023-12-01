#Django Imports
from django.shortcuts import render
from django.contrib.auth import authenticate

#Rest Framework Imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

#Rest Framework Simple JWT Imports
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
import pdb

#Local Imports
from account.serializers import (
  UserRegistrationSerializer,
  UserLoginSerializer,
  UserProfileSerializer,
  UserChangePasswordSerializer
)
from account.renderers import UserRenderer

def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
    'refresh': str(refresh),
    'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  renderer_classes = (UserRenderer,)
  def post(self, request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      tokens = get_tokens_for_user(user)
      return Response({'success': True, 'tokens': tokens}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
  renderer_classes = (UserRenderer,)
  def post(self, request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
      email = serializer.data.get('email')
      password = serializer.data.get('password')
      user = authenticate(request, email=email, password=password)
      if user is not None:
        tokens = get_tokens_for_user(user)
        return Response({'success': True, 'tokens': tokens}, status=status.HTTP_200_OK)
      else:
        response = {
          'errors': {
            'non_field_errors': 'Username or password is invalid'
          }
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
  renderer_classes = (UserRenderer,)
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request):
    user = request.user
    serializer = UserProfileSerializer(user)
    return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
  renderer_classes = (UserRenderer,)
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request):
    serializer = UserChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
      new_password = serializer.data.get('new_password')
      user = request.user
      user.set_password(new_password)
      user.save()
      return Response({'success': True}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
