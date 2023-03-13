from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from weighttrackingapi.models import Weight, Resident


class WeightView(ViewSet):
    """Weight Tracking weight view"""

    def list(self, request):
        """Handle GET requests to get all weights

        Returns:
            Response -- JSON serialized list of weights
        """
        weight = Weight.objects.all()

        # filtering weight by date
        if "date" in request.query_params:
            weight = weight.filter(date=request.query_params['date'])
        # filtering weight by resident id
        if "resident" in request.query_params:
            weight = weight.filter(
                resident=request.query_params['resident'])
        if "resident" in request.query_params and "date" in request.query_params:
            weight = weight.filter(
                resident=request.query_params['resident'], date=request.query_params['date'])
        serializer = WeightSerializer(weight, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handle GET requests for single weight

        Returns:
            Response -- JSON serialized weight
        """
        try:
            weight = Weight.objects.get(pk=pk)
        except Weight.DoesNotExist:
            return Response({'message': 'You sent an invalid weight ID'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WeightSerializer(weight)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized weight instance
        """
        resident = Resident.objects.get(pk=request.data["resident"])

        weight = Weight.objects.create(
            resident=resident,
            date=request.data["date"],
            weight=request.data["weight"],
        )
        weight.save()
        serializer = WeightSerializer(weight)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT operations for weight 

        Returns
            Response -- Empty body with 204 status code
        """
        resident = Resident.objects.get(pk=request.data["resident"])
        weight = Weight.objects.get(pk=pk)

        weight.resident = resident
        weight.date = request.data["date"]
        weight.weight = request.data["weight"]
        weight.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class WeightSerializer(serializers.ModelSerializer):
    """JSON serializer for weights"""
    class Meta:
        model = Weight
        fields = ('id', 'resident', 'date', 'weight')
