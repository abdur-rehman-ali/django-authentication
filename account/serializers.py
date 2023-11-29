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
