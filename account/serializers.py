#Django RestFramework Imports
from rest_framework import serializers

#Local Imports
from account.models import User

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
