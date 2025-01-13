from rest_framework import viewsets
from rest_framework.response import Response
from .models import Member, Role, Roster
from .serializers import MemberSerializer, RoleSerializer, RosterSerializer
from django.db.models import Count
from datetime import datetime, timedelta

# Viewset for Role
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

# Viewset for Member
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def create(self, request, *args, **kwargs):
        role_id = request.data.get('roles')
        role = Role.objects.get(id=role_id)
        member = Member.objects.create(
            name=request.data.get('name'),
            age=request.data.get('age'),
            contact=request.data.get('contact'),
            roles=role
        )
        serializer = self.get_serializer(member)
        return Response(serializer.data)

# Custom Viewset for generating and displaying roster
class RosterViewSet(viewsets.ViewSet):
    def list(self, request):
        rosters = Roster.objects.all()
        serializer = RosterSerializer(rosters, many=True)
        return Response(serializer.data)

    def create(self, request):
        # Get the input data (including sunday_date and members)
        sunday_date = request.data.get('sunday_date')
        members_data = request.data.get('members')

        # Create the Roster object
        roster = Roster.objects.create(sunday_date=sunday_date)

        # Add members to roster
        for member_data in members_data:
            member = Member.objects.get(id=member_data['id'])
            roster.members.add(member)

        # Save the roster
        roster.save()

        return Response({"message": "Roster created successfully!"})
