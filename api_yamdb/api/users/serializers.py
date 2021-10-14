from rest_framework import serializers
from api.users.models import User


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='get_role_display')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def validate_role(self, value):
        return value[0]

