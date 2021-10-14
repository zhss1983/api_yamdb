from rest_framework import serializers
from api.users.models import User, ACCESS_LEVEL


class StringToSymbol(serializers.Field):
    def to_representation(self, value):
        for level in ACCESS_LEVEL:
            symbol, role = level
            if value == symbol:
                return role
        return value

    def to_internal_value(self, data):
        role_list = []
        for level in ACCESS_LEVEL:
            role_list.append(level[1])
        if data not in role_list:
            raise serializers.ValidationError('No such user role')
        data = data[:1]
        return data


class UserSerializer(serializers.ModelSerializer):
    role = StringToSymbol(required=False)
    lookup_field = 'username'

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
