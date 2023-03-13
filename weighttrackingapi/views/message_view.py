from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from weighttrackingapi.models import Message, Employee, EmployeeMessage


class MessageView(ViewSet):
    """Weight Tracking message view"""

    def list(self, request):
        """Handle GET requests to get all messages

        Returns:
            Response -- JSON serialized list of messages
        """
        message = Message.objects.all()

        # filtering message by date
        if "date_created" in request.query_params:
            message = message.filter(date_created=request.query_params['date_created'])

        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handle GET requests for single message

        Returns:
            Response -- JSON serialized message
        """
        try:
            message = Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            return Response({'message': 'You sent an invalid message ID'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized message instance
        """
        sender = Employee.objects.get(user=request.auth.user)
        recipients =request.data["recipients"]
        print(recipients)
        message = Message.objects.create(
            subject=request.data["subject"],
            message_body=request.data["message_body"],
            date_created=request.data["date_created"],
            read=request.data["read"],
            deleted=request.data["deleted"],
        )
        message.save()
        serializer = MessageSerializer(message)
        # print(f"The new message has id: {serializer.data['id']}")
        new_message_id = serializer.data['id']
        for recipient in recipients:
            employee_message=EmployeeMessage.objects.create(
                message = Message.objects.get(pk=new_message_id),
                sender = sender,
                recipient = Employee.objects.get(pk=recipient)
            )
            employee_message.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT operations for message

        Returns
            Response -- Empty body with 204 status code
        """
        message = Message.objects.get(pk=pk)
        message.subject = request.data["subject"]
        message.message_body = request.data["message_body"]
        message.date_created = request.data["date_created"]
        message.read = request.data["read"]
        message.deleted = request.data["deleted"]
        message.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        """Handle DELETE requests for messages

        Returns:
            Response: None with 204 status code
        """
        message = Message.objects.get(pk=pk)
        message.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class MessageSerializer(serializers.ModelSerializer):
    """JSON serializer for messages"""
    class Meta:
        model = Message
        fields = ('id', 'subject', 'message_body', 'date_created', 'read', 'deleted')
