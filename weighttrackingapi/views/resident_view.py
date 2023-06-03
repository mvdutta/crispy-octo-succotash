from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.db.models import Q
from weighttrackingapi.models import Resident


class ResidentView(ViewSet):
    """Weight Tracking resident view"""

    def list(self, request):
        """Handle GET requests to get all residents

        Returns:
            Response -- JSON serialized list of residents
        """
        

        if "keyword" in request.query_params:
           print(request.query_params['keyword'])
           residents = Resident.objects.filter(
               Q(first_name__icontains=request.query_params['keyword'])
               | Q(last_name__icontains=request.query_params['keyword'])
           ) 
           serializer = ResidentSerializer(residents, many=True)
           return Response(serializer.data)
        
        residents = Resident.objects.all()
        serializer = ResidentSerializer(residents, many=True)
        return Response(serializer.data)
        
    
    def retrieve(self, request, pk):
        """Handle GET requests for single resident

        Returns:
            Response -- JSON serialized resident
        """
        try:
            resident = Resident.objects.get(pk=pk)
        except Resident.DoesNotExist:
            return Response({'message': 'You sent an invalid resident ID'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ResidentSerializer(resident)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ResidentSerializer(serializers.ModelSerializer):
    """JSON serializer for residents"""
    class Meta:
        model = Resident
        fields = ('id', 'first_name', 'last_name', 'room_num', 'admission_wt', 'usual_wt', 'height', 'admission_date')