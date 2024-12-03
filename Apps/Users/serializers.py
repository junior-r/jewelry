from rest_framework import serializers

from Apps.Users.models import User


class UserSerializer(serializers.ModelSerializer):
    pk = serializers.UUIDField(read_only=True, source='code')
    full_name = serializers.CharField(read_only=True, source='get_full_name')
    image = serializers.CharField(read_only=True, source='get_avatar')
    role = serializers.CharField(read_only=True, source='get_role')
    role_display = serializers.CharField(read_only=True, source='get_role_display')
    absolute_url = serializers.CharField(read_only=True, source='get_absolute_url')
    update_url = serializers.CharField(read_only=True, source='get_update_url')
    change_rol_url = serializers.CharField(read_only=True, source='get_change_rol_url')
    change_status_url = serializers.CharField(read_only=True, source='get_change_status_url')

    class Meta:
        model = User
        fields = [
            'pk',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'image',
            'is_active',
            'date_joined',
            'last_login',
            'role',
            'role_display',
            'absolute_url',
            'update_url',
            'change_rol_url',
            'change_status_url',
        ]
