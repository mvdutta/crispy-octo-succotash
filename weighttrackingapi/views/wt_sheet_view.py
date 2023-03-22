from django.http import HttpResponseServerError
from django.db import connection
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from weighttrackingapi.models import WeightSheet, Employee, Resident, Weight


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


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
            wt_sheets = wt_sheets.filter(
                resident=request.query_params['resident'])

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

        #Do not create a weightsheet if one already exists
        try:
            resident = Resident.objects.get(pk=request.data["resident"])
            WeightSheet.objects.get(date=request.data["date"], resident=resident)
            return Response({"msg": "Already exists"}, status=status.HTTP_400_BAD_REQUEST)
        except WeightSheet.DoesNotExist:
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
            final=request.data["final"]
        )
            wt_sheet.save()
            new_weight = Weight.objects.create(
                date=request.data["date"],
                resident=resident,
                weight=request.data["weight"]
            )
            new_weight.save()
            serializer = WeightSheetSerializer(wt_sheet)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Handle PUT operations for weight sheet

        Returns
            Response -- Empty body with 204 status code
        """
        employee = Employee.objects.get(user=request.auth.user)  
        wt_sheet = WeightSheet.objects.get(pk=pk)
        resident = Resident.objects.get(pk=request.data["resident"])
        wt_sheet.employee = employee
        wt_sheet.resident = resident
        wt_sheet.reweighed = request.data["reweighed"]
        wt_sheet.refused = request.data["refused"]
        wt_sheet.not_in_room = request.data["not_in_room"]
        wt_sheet.daily_wts = request.data["daily_wts"]
        wt_sheet.show_alert = request.data["show_alert"]
        wt_sheet.scale_type = request.data["scale_type"]
        wt_sheet.final = request.data["final"]
        wt_sheet.save()
        return Response({"msg": "Record updated"}, status=status.HTTP_204_NO_CONTENT)




    # @action(detail=False, methods=['get', 'post', 'delete'])
    # def detailedview(self, request, pk=None):
    #     '''Shows all details for weightsheet'''
    #     # with connection.cursor() as cursor:
    #     #     cursor.execute('''with temp as (
    #     #         select w.weight, w.id as weight_id, ws.id as weight_sheet_id, ws.final, ws.resident_id, ws.reweighed, ws.refused, ws.not_in_room, ws.daily_wts, ws.show_alert, ws.scale_type from weighttrackingapi_weight w
    #     #         join weighttrackingapi_weightsheet ws
    #     #         on ws.resident_id = w.resident_id
    #     #         where w.date = %s
    #     #         and ws.final=0
    #     #         )
    #     #         select r.first_name, r.last_name, r.room_num, temp.* from temp
    #     #         join weighttrackingapi_resident r
    #     #         where temp.resident_id = r.id''', [request.query_params['date']])
    #     #     res = dictfetchall(cursor)

    #     weights = Weight.objects.filter(date=request.query_params["date"])
    #     weights_serialized = WeightSerializer(weights, many=True)
    #     all_weights = weights_serialized.data
    #     weightsheets = WeightSheet.objects.filter(date=request.query_params["date"])
    
    #     return Response(all_weights, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get', 'post', 'delete'])
    def detailedview_rd(self, request, pk=None):
        '''Shows all details for weightsheet'''
        with connection.cursor() as cursor:
            cursor.execute('''with temp as (
                select w.weight, w.id as weight_id, ws.id as weight_sheet_id, ws.final, ws.resident_id, ws.reweighed, ws.refused, ws.not_in_room, ws.daily_wts, ws.show_alert, ws.scale_type from weighttrackingapi_weight w
                join weighttrackingapi_weightsheet ws
                on ws.resident_id = w.resident_id
                where w.date = %s and ws.date = %s
                )
                select r.first_name, r.last_name, r.room_num, temp.* from temp
                join weighttrackingapi_resident r
                where temp.resident_id = r.id''', [request.query_params['date'], request.query_params['date']])
            res = dictfetchall(cursor)
    
        return Response(res)
    

    
    @action(detail=False, methods=['post'])
    def create_all_weightsheets(self, request, pk=None):
        '''Creates ALL weightsheets for a given day Only if they don't already exist'''

        print(request.body)

        employee = Employee.objects.get(user=request.auth.user)
        residents = Resident.objects.all()
        i=0
        for resident in residents:
            existing_wt_sheet = WeightSheet.objects.filter(date=request.data["date"], resident=resident)
            if not  existing_wt_sheet.exists():
                wt_sheet = WeightSheet.objects.create(
                employee=employee,
                resident=resident,
                date=request.data["date"],
                reweighed=False,
                refused=False,
                not_in_room=False,
                daily_wts=False,
                show_alert=True,
                scale_type="",
                final=False)
                wt_sheet.save()
                new_weight = Weight.objects.create(
                date=request.data["date"],
                resident=resident,
                weight=0)
                new_weight.save()
                i+=1
                print("created")

        return Response({"msg": f"{i} Weightsheets created"}, status=status.HTTP_201_CREATED)
    




class WeightSheetSerializer(serializers.ModelSerializer):
    """JSON serializer for weight_sheets"""
    class Meta:
        model = WeightSheet
        fields = ('id', 'employee', 'date', 'resident', 'final',
                  'reweighed', 'refused', 'not_in_room', 'daily_wts', 'show_alert', 'scale_type')
class WeightSerializer(serializers.ModelSerializer):
    """JSON serializer for weights"""
    class Meta:
        model = Weight
        fields = ('id', 'resident', 'date', 'weight')
        depth = 1