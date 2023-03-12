from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from weighttrackingapi.models import Resident


class ResidentView(ViewSet):
    """Weight Tracking resident view"""

    def list(self, request):
        """Handle GET requests to get all residents

        Returns:
            Response -- JSON serialized list of residents
        """
        residents = Resident.objects.all()
        serializer = ResidentSerializer(residents, many=True)
        return Response(serializer.data)

class ResidentSerializer(serializers.ModelSerializer):
    """SON serializer for residents"""
    class Meta:
        model = Resident
        fields = ('id', 'first_name', 'last_name', 'room_num', 'admission_wt', 'usual_wt', 'height', 'admission_date')