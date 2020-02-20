from rest_framework import serializers
from users import models

from drf_extra_fields.fields import Base64ImageField

INVALID_CREDENTIALS_ERROR = 'Invalid Credentials'


class TokenSerializer(serializers.ModelSerializer):

    access_token = serializers.CharField(source='key')

    class Meta:
        model = models.Token
        fields = ('access_token', 'expires_at')


class LoginSerializer(serializers.Serializer):

    phone_number = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate(self, data):
        validated_data = super().validate(data)
        phone_number = validated_data['phone_number']
        password = validated_data['password']
        try:
            user = models.User.objects.get(phone_number=phone_number)
            if not user.check_password(password):
                raise serializers.ValidationError(INVALID_CREDENTIALS_ERROR)
            validated_data['user'] = user
        except models.User.DoesNotExist:
            raise serializers.ValidationError(INVALID_CREDENTIALS_ERROR)
        return validated_data

    def save(self):
        user = self.validated_data['user']
        token = models.Token.create_token(user)
        self.token = token
        return token


class UserSerializer(serializers.ModelSerializer):

    profile_picture = Base64ImageField(required=False)

    class Meta:
        model = models.User
        fields = ('id', 'name', 'email', 'phone_number', 'address', 'profile_picture', 'coordinates',
                  'landmark')


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        abstract = True

    def to_internal_value(self, data):
        if 'user' not in data:
            data['user'] = {}
        for field in UserSerializer.Meta.fields:
            if field in data:
                data['user'][field] = data.pop(field)
        return super().to_internal_value(data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_data = UserSerializer(instance=instance.user).data
        for key in user_data:
            data[key] = user_data[key]
        return data

    def update(self, instance, validated_data):
        user_obj = validated_data.pop('user').save()
        for key in validated_data:
            setattr(instance, key, validated_data[key])
        instance.save()
        return instance

    def validate_user(self, user):
        if self.instance:
            user_obj = self.instance.user
            partial = True
        else:
            phone_number = user.get('phone_number')
            try:
                user_obj = models.User.objects.get(phone_number=phone_number)
                partial = True
            except models.User.DoesNotExist:
                user_obj = None
                partial = False

        serializer = UserSerializer(data=user, instance=user_obj, partial=partial)
        if not serializer.is_valid():
            raise serializers.ValidationError(serializer.errors)
        return serializer


class DesignerSerializer(CustomUserSerializer):
    user = UserSerializer()


    class Meta:
        model = models.Designer
        fields = ('work_radius', 'user')


class CustomerSerializer(CustomUserSerializer):
    user = serializers.DictField(write_only=True)

    class Meta:
        model = models.Customer
        fields = ('age', 'user')

    def create(self, validated_data):
        user_obj = validated_data.pop('user').save()
        print(user_obj)
        try:
            customer = models.Customer.objects.get(user=user_obj)
            for key in validated_data:
                setattr(customer, key, validated_data[key])
            customer.save()
        except models.Customer.DoesNotExist:
            validated_data['user'] = user_obj
            customer = models.Customer.objects.create(**validated_data)
        return customer
