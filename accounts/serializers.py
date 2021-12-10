from rest_framework.serializers import ModelSerializer

from accounts.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance


class LoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'token']
        extra_kwargs = {
            'password': {'write_only': True},
            'token': {'read_only': True},
        }
