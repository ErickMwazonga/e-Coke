from rest_framework.serializers import (
    EmailField,
    CharField,
    ModelSerializer,
    HyperlinkedIdentityField,
    ValidationError,
)
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

# hyperlink to detail view
user_detail_url = HyperlinkedIdentityField(
    view_name='api_users:detail',
    lookup_field='pk',
)
# hyperlink to update view
user_update_url = HyperlinkedIdentityField(
    view_name='api_users:update',
    lookup_field='pk',
)
# hyperlink to delete view
user_delete_url = HyperlinkedIdentityField(
    view_name='api_users:delete',
    lookup_field='pk',
)

class UserCreateSerializer(ModelSerializer):
    email = EmailField(label='Email Address')
    class Meta:
        model = User
        fields  = [
            'username',
            'email',
            'password'
        ]
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def create(self, validated_data):
        username        = validated_data['username']
        email           = validated_data['email']
        password        = validated_data['password']
        user_obj        = User(
            username = username,
            email    = email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserListSerializer(ModelSerializer):
    url = user_detail_url
    delete_url = user_delete_url
    class Meta:
        model = User
        fields  = [
            'url',
            'username',
            'email',
            'delete_url',
        ]


class UserRetrieveSerializer(ModelSerializer):
    update_url = user_update_url

    class Meta:
        model = User
        fields  = [
            'id',
            'update_url',
            'username',
            'email',
        ]


class UserLoginSerializer(ModelSerializer):
    token    = CharField(allow_blank=True, read_only=True)
    username = CharField(required=False, allow_blank=True)
    email    = EmailField(label='Email Address', required=False, allow_blank=True)

    class Meta:
        model = User
        fields  = [
            'username',
            'email',
            'password',
            'token'
        ]
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate(self, data):
        user_obj    = None
        email       = data.get("email", None)
        username    = data.get("username", None)
        password    = data["password"]
        if not email and not username:
            raise ValidationError("A username or email is required.")

        user = User.objects.filter(
                Q(email=email) |
                Q(username=username)
            ).distinct()
        user = user.exclude(email__isnull=True).exclude(email__iexact='')
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This username or email is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect Credentials, please try again.")
        data["token"] = "Random Token"

        return data
