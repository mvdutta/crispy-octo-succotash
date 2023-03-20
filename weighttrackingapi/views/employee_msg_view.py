from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from weighttrackingapi.models import EmployeeMessage


class EmployeeMessageView(ViewSet):
    """Weight Tracking employee message view"""

    def list(self, request):
        """Handle GET requests to get all employee_msgs

        Returns:
            Response -- JSON serialized list of employees
        """
        employee_msgs = EmployeeMessage.objects.all()

        if "recipient" in request.query_params:
            employee_msgs = employee_msgs.filter(
                recipient=request.query_params['recipient'])
            
        serializer = EmployeeMessageSerializer(employee_msgs, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        """Handle GET requests for single employee_msg

        Returns:
            Response -- JSON serialized employee_msg
        """
        try:
            employee_msg = EmployeeMessage.objects.get(pk=pk)
        except EmployeeMessage.DoesNotExist:
            return Response({'message': 'You sent an invalid employee_msg ID'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeMessageSerializer(employee_msg)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        """Handle DELETE requests for employee messages

        Returns:
            Response: None with 204 status code
        """
        employee_msg = EmployeeMessage.objects.get(pk=pk)
        employee_msg.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class EmployeeMessageSerializer(serializers.ModelSerializer):
    """JSON serializer for employee_msgs"""
    class Meta:
        model = EmployeeMessage
        fields = ('id', 'sender', 'recipient', 'message')
        depth = 2
