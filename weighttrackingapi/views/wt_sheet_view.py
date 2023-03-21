from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from weighttrackingapi.models import WeightSheet, Employee, Resident, Weight


class WeightSheetView(ViewSet):
    """Weight Tracking weight_sheet view"""

    def list(self, request):
        """Handle GET requests to get all weight_sheets

        Returns:
            Response -- JSON serialized list of weight_sheets
        """
        wt_sheets = WeightSheet.objects.all()
        # filtering weight_sheet by resident id and by date
        if "resident" in request.query_params and "date" in request.query_params:
            wt_sheets = wt_sheets.filter(
                resident=request.query_params['resident'], date=request.query_params['date'])
        # filtering weight_sheet by date
        if "date" in request.query_params:
            wt_sheets = wt_sheets.filter(date=request.query_params['date'])  
        # filtering weight_sheet by resident id
        if "resident" in request.query_params:
            wt_sheets = wt_sheets.filter(resident=request.query_params['resident'])

        serializer = WeightSheetSerializer(wt_sheets, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handle GET requests for single weight sheet

        Returns:
            Response -- JSON serialized weight sheet
        """
        try:
            wt_sheet = WeightSheet.objects.get(pk=pk)
        except WeightSheet.DoesNotExist:
            return Response({'message': 'You sent an invalid weight_sheet ID'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WeightSheetSerializer(wt_sheet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized weight sheet instance
        """
        employee = Employee.objects.get(user=request.auth.user)
        
        try:
            resident = Resident.objects.get(pk=request.data["resident"])
            wt_sheet = WeightSheet.objects.create(
                employee=employee,
                resident=resident,
                date=request.data["date"],
                reweighed=request.data["reweighed"],
                refused=request.data["refused"],
                not_in_room=request.data["not_in_room"],
                daily_wts=request.data["daily_wts"],
                show_alert=request.data["show_alert"],
                scale_type=request.data["scale_type"],
                final = request.data["final"]
            )
            wt_sheet.save()
            new_weight = Weight.objects.create(
                date=request.data["date"],
                resident = resident,
                weight = request.data["weight"]
            )
            new_weight.save()
            # serializer = WeightSheetSerializer(wt_sheet)
            return Response({"msg": "Data saved successfully"}, status=status.HTTP_201_CREATED)
        except TypeError:
            weightsheet_bulk_creation_list = []
            weight_bulk_creation_list = []
            for entry in request.data:
                resident = Resident.objects.get(pk=entry["resident"])
                weightsheet_bulk_creation_list.append(WeightSheet(
                employee=employee,
                resident=resident,
                date=entry["date"],
                reweighed=entry["reweighed"],
                refused=entry["refused"],
                not_in_room=entry["not_in_room"],
                daily_wts=entry["daily_wts"],
                show_alert=entry["show_alert"],
                scale_type=entry["scale_type"],
                final = entry["final"]
                ))
                weight_bulk_creation_list.append(Weight(
                    date = entry["date"],
                    resident = resident,
                    weight = entry["weight"]
                ))
            WeightSheet.objects.bulk_create(weightsheet_bulk_creation_list)
            Weight.objects.bulk_create(weight_bulk_creation_list)
            return Response({"msg": "All records updated"}, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT operations for weight sheet

        Returns
            Response -- Empty body with 204 status code
        """
        employee = Employee.objects.get(user=request.auth.user)
        resident = Resident.objects.get(pk=request.data["resident"])
        wt_sheet = WeightSheet.objects.get(pk=pk)

        wt_sheet.employee=employee
        wt_sheet.resident=resident
        wt_sheet.date=request.data["date"]
        wt_sheet.reweighed=request.data["reweighed"]
        wt_sheet.refused=request.data["refused"]
        wt_sheet.not_in_room=request.data["not_in_room"]
        wt_sheet.daily_wts=request.data["daily_wts"]
        wt_sheet.show_alert=request.data["show_alert"]
        wt_sheet.scale_type=request.data["scale_type"]
        wt_sheet.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class WeightSheetSerializer(serializers.ModelSerializer):
    """JSON serializer for weight_sheets"""
    class Meta:
        model = WeightSheet
        fields = ('id', 'employee', 'date', 'resident',
                  'reweighed', 'refused', 'not_in_room', 'daily_wts', 'show_alert', 'scale_type')
