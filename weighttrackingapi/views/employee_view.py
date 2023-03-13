from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from weighttrackingapi.models import Employee


class EmployeeView(ViewSet):
    """Weight Tracking employee view"""

    def list(self, request):
        """Handle GET requests to get all employees

        Returns:
            Response -- JSON serialized list of employees
        """
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handle GET requests for single employee

        Returns:
            Response -- JSON serialized employee
        """
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response({'message': 'You sent an invalid employee ID'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class EmployeeSerializer(serializers.ModelSerializer):
    """SON serializer for employees"""
    class Meta:
        model = Employee
        fields = ('id', 'user', 'role')
