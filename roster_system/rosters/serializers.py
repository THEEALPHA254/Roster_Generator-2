from rest_framework import serializers
from .models import Member, Role, Roster

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name']

class MemberSerializer(serializers.ModelSerializer):
    roles = serializers.CharField(source='roles.name', read_only=True)  # Display role as a string

    class Meta:
        model = Member
        fields = ['id', 'name', 'age', 'contact', 'roles']  # Include age field

class RosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roster
        fields = ['sunday_date', 'members']
