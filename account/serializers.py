#Django RestFramework Imports
from rest_framework import serializers

#Django Imports
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, smart_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator

#Local Imports
from account.models import User
from account.utils import get_user_by_email

class UserRegistrationSerializer(serializers.ModelSerializer):
  password_confirmation = serializers.CharField(style={
    'input_type': 'password'
  }, write_only=True)
  
  class Meta:
    model = User
    fields = ['name', 'email', 'password', 'password_confirmation']
    extra_kwargs = {
      'password': { 'write_only': True }
    }

  def validate(self, attrs):
    password = attrs.get('password')
    password_confirmation = attrs.get('password_confirmation')
    if password != password_confirmation:
      raise serializers.ValidationError("Password and confirmation password doesn't match")
    return attrs

  def create(self, validate_data):
    return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'name', 'email']

class UserChangePasswordSerializer(serializers.Serializer):
  old_password = serializers.CharField(max_length=255)
  new_password = serializers.CharField(max_length=255)
  new_password_confirmation = serializers.CharField(max_length=255)

  def validate(self, attrs):
    old_password = attrs.get('old_password')
    new_password = attrs.get('new_password')
    new_password_confirmation = attrs.get('new_password_confirmation')
    user = self.context.get('request').user
    if not user.check_password(old_password):
      raise serializers.ValidationError("Please enter correct old password")
    if new_password!= new_password_confirmation:
      raise serializers.ValidationError("Password and confirmation password doesn't match")
    return attrs

class UserSendPasswordResetSerializer(serializers.Serializer):
  email = serializers.CharField(max_length=255)
  
  def validate(self, attrs):
    email = attrs.get('email')
    user = get_user_by_email(email)
    if user is None:
      raise serializers.ValidationError("User with this email doesn't exist")
    uuid = urlsafe_base64_encode(force_bytes(user.id))
    token = PasswordResetTokenGenerator().make_token(user)
    BASE_URL = "http://localhost:8000"
    link = f"{BASE_URL}/api/v1/reset-password/{uuid}/{token}"
    print(link)
    # Email send code
    return attrs


class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255)
  password_confirmation = serializers.CharField(max_length=255)

  def validate(self, attrs):
    self.validate_password_match(attrs)
    user = self.get_user_from_token()
    self.reset_user_password(user, attrs.get('password'))
    return attrs

  def validate_password_match(self, attrs):
    password = attrs.get('password')
    password_confirmation = attrs.get('password_confirmation')
    if password!= password_confirmation:
      raise serializers.ValidationError("Password and confirmation password doesn't match")

  def get_user_from_token(self):
    uuid = self.context.get('uuid')
    token = self.context.get('token')
    id = smart_str(urlsafe_base64_decode(uuid))
    try:
      user = User.objects.get(id=id)
    except User.DoesNotExist:
      raise serializers.ValidationError("User doesn't exist")

    if not PasswordResetTokenGenerator().check_token(user, token):
      raise serializers.ValidationError("Token is not valid")
    return user

  def reset_user_password(self, user, password):
    user.set_password(password)
    user.save()
    
