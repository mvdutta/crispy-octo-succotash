from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from weighttrackingapi.models import Weight, Resident
from datetime import date, datetime, timedelta


def get_closest_weight(weight_objects, lookbackdays, datestr):

    '''
    Requires a dictionary of weights and corresponding dates ("weight_objects") and the number of days we are looking back to "lookbackdays"
    Returns a dictionary with the closest date to the time requested and the weight on that date
    '''
    ref_date = datetime.strptime(datestr, '%Y-%m-%d').date()
    lookbackdate = datetime.strptime(datestr, '%Y-%m-%d')- timedelta(days=lookbackdays)
    weights = [x[1] for x in weight_objects if x[0] != ref_date]
    dates = [x[0] for x in weight_objects if x[0] != ref_date]
    diffs = [abs((x[0]-lookbackdate.date()).days) for x in weight_objects if x[0] != ref_date]
    min_diff = min(diffs)
    index = diffs.index(min_diff)
    closest_date = dates[index]
    weight_on_closest_date = weights[index]
    return {"closest_date": closest_date, "weight": weight_on_closest_date }

LOOKBACK_DICT = {"1week": 7, "1month":30, "3month":90, "6month":180}


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
                resident=request.query_params['resident']).order_by('date')

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
    
    @action(detail=False, methods=['get'])
    def closestdate(self, request, pk=None):
        '''Returns the date closest to a certain day for a given resident'''
        resident = Resident.objects.get(pk=request.query_params["resident"])
        weight_objects = Weight.objects.filter(resident=resident).values_list('date','weight')
        if "date" not in request.query_params:
            return Response({"msg": "A reference date must be provided for looking back"}, status=status.HTTP_400_BAD_REQUEST)
        ref_date = request.query_params["date"]
        lookback = request.query_params.get("lookback")
        if lookback not in ["1week", "1month", "3month", "6month"]:
            return Response({"msg": "Invalid lookback value"}, status=status.HTTP_400_BAD_REQUEST)
        lookbackdays = LOOKBACK_DICT[lookback]
        res = get_closest_weight(weight_objects, lookbackdays, ref_date)
        return Response(res, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def closestdate_all(self, request, pk=None):
        '''Returns the date closest to a certain day'''
        if "date" not in request.query_params:
            return Response({"msg": "A reference date must be provided for looking back"}, status=status.HTTP_400_BAD_REQUEST)
        ref_date = request.query_params["date"]
        lookback = request.query_params.get("lookback")
        if lookback not in ["1week", "1month", "3month", "6month"]:
            return Response({"msg": "Invalid lookback value"}, status=status.HTTP_400_BAD_REQUEST)
        lookbackdays = LOOKBACK_DICT[lookback]

        
        residents = Resident.objects.all()
        results = []
        for resident in residents:
            weight_objects = Weight.objects.filter(resident=resident).values_list('date','weight')

            res = get_closest_weight(weight_objects, lookbackdays, ref_date)
            res["resident_id"] = resident.id
            results.append(res)
        return Response(results, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def rd_summary(self, request, pk=None):
        '''Creates a weight summary of patient for RD view'''
        datestr = datetime.now().strftime("%Y-%m-%d")
        resident = Resident.objects.get(pk=request.query_params["resident"])
        resident_data = ResidentSerializer(resident).data
        weight_objects = Weight.objects.filter(
            resident=resident).values_list('date', 'weight')
        # This variable stores the last date
        last_wt_recorded_date = datestr

        try:
            weight = Weight.objects.get(
                resident=resident, date=datetime.today().strftime('%Y-%m-%d'))
            weight_serializer = WeightSerializer(weight)
            current_weight = float(weight_serializer.data["weight"])
            last_wt_recorded_date = datestr

        except Weight.DoesNotExist:
            current_weight = float(get_closest_weight(
                weight_objects, 0, datestr)["weight"])
            last_wt_recorded_date = get_closest_weight(
                weight_objects, 0, datestr)["closest_date"].strftime("%Y-%m-%d")

        next_to_last_recorded = get_closest_weight(
            weight_objects, 7, last_wt_recorded_date)
        next_to_last_recorded_weight = next_to_last_recorded["weight"]
        next_to_last_recorded_date = next_to_last_recorded["closest_date"].strftime(
            '%m-%d-%Y')
        w7 = get_closest_weight(weight_objects, 7, datestr)
        w30 = get_closest_weight(weight_objects, 30, datestr)
        w90 = get_closest_weight(weight_objects, 90, datestr)
        w180 = get_closest_weight(weight_objects, 180, datestr)
        prev_wt_1week = w7["weight"]
        prev_wt_1month = w30["weight"]
        prev_wt_3month = w90["weight"]
        prev_wt_6month = w180["weight"]

        prev_dt_1week = w7["closest_date"].strftime('%m-%d-%Y')
        prev_dt_1month = w30["closest_date"].strftime('%m-%d-%Y')
        prev_dt_3month = w90["closest_date"].strftime('%m-%d-%Y')
        prev_dt_6month = w180["closest_date"].strftime('%m-%d-%Y')
        dts = [prev_dt_6month, prev_dt_3month, prev_dt_1month, next_to_last_recorded_date]
        wts = [prev_wt_6month, prev_wt_3month,
               prev_wt_1month, next_to_last_recorded_weight]
        weight_history = {'dates': [], 'weights': []}
        for (dt, wt) in zip(dts, wts):
            if wt is not None and wt != 0 and dt not in weight_history['dates']:
                weight_history['dates'].append(dt)
                weight_history['weights'].append(float(wt))
        # weight_history["weights"].append(current_weight)
        # weight_history["dates"].append(datetime.today().strftime('%m-%d-%Y'))

        BMI = 703*float(current_weight) / \
            (float(resident_data["height"])*float(resident_data["height"]))

        # Percentage changes

        try:
            perc_change_1week = 100 * \
                (-float(next_to_last_recorded_weight)+current_weight)/float(prev_wt_1week)
        except TypeError:
            perc_change_1week = "Not Available"
        except ZeroDivisionError:
            perc_change_1week = "Not Available"
        try:
            perc_change_1month = 100 * \
                (-float(prev_wt_1month)+current_weight)/float(prev_wt_1month)
        except TypeError:
            perc_change_1month = "Not Available"
        except ZeroDivisionError:
            perc_change_1month = "Not Available"
        try:
            perc_change_3month = 100 * \
                (-float(prev_wt_3month)+current_weight)/float(prev_wt_3month)
        except TypeError:
            perc_change_3month = "Not Available"
        except ZeroDivisionError:
            perc_change_3month = "Not Available"
        try:
            perc_change_6month = 100 * \
                (-float(prev_wt_6month)+current_weight)/float(prev_wt_6month)
        except TypeError:
            perc_change_6month = "Not Available"
        except ZeroDivisionError:
            perc_change_6month = "Not Available"

        response = {
            "patient_name": f"{resident_data['last_name']}, {resident_data['first_name']}",
            "admission_date": resident_data["admission_date"],
            "ABW": resident_data["admission_wt"],
            "CBW": current_weight,
            "BMI": BMI,
            "PBW": next_to_last_recorded_weight,
            "perc_change_1week": perc_change_1week,
            "perc_change_1month": perc_change_1month,
            "perc_change_3month": perc_change_3month,
            "perc_change_6month": perc_change_6month,
            "weight_history": weight_history
        }
        return Response(response, status=status.HTTP_200_OK)


class WeightSerializer(serializers.ModelSerializer):
    """JSON serializer for weights"""
    class Meta:
        model = Weight
        fields = ('id', 'resident', 'date', 'weight')

class ResidentSerializer(serializers.ModelSerializer):
    """JSON serializer for residents"""
    class Meta:
        model = Resident
        fields = ('id', 'first_name', 'last_name', 'room_num', 'admission_wt', 'usual_wt', 'height', 'admission_date')
