from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Member, Role, Roster
from .serializers import MemberSerializer, RoleSerializer, RosterSerializer
from django.db.models import Count, Q
from datetime import datetime, timedelta
from rest_framework.pagination import PageNumberPagination

# Custom pagination class
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Viewset for Role
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    pagination_class = StandardResultsSetPagination #use custom pagination
    

# Viewset for Member
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    pagination_class = StandardResultsSetPagination  # Use custom pagination class

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(Q(name__icontains=search))
        return queryset

    def create(self, request, *args, **kwargs):
        role_id = request.data.get('role')  # Make sure the frontend sends "role" (not "roles")
        
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create the member and assign the role
        member = Member.objects.create(
            name=request.data.get('name'),
            age=request.data.get('age'),
            contact=request.data.get('contact'),
            roles=role  # ✅ Assign directly since it's a ForeignKey
        )

        serializer = self.get_serializer(member)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
