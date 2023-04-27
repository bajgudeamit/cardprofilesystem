from rest_framework import serializers
from CustomerApp.models import Custom_user
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

class CustomUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Custom_user
        fields = ['id','user','address', 'phone_no', 'url', 'profile_pic']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        custom_user = Custom_user.objects.create(user=user, **validated_data)
        return custom_user
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            raise serializers.ValidationError(user_serializer.errors)

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

#HhWusozG08srmgxtXLBcWopBNDbKVg -sagar-7
#lGIl9GkIgrSI9WpYWEYyFbalAEJCXH-amit-8