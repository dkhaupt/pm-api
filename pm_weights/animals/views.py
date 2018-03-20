from django.shortcuts import render, get_object_or_404
from django.utils.dateparse import parse_datetime
from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.response import Response

# models
from .models import Animal, AnimalWeight

# serializer
from .serializers import AnimalSerializer, AnimalWeightSerializer

# Create your views here.

class AnimalViewSet(viewsets.ModelViewSet):

    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    def add_weight(self, request, id=None):
        # add a weight record for a single animal
        queryset = Animal.objects.all()
        animal = get_object_or_404(queryset, pk=id)
        serializer = AnimalWeightSerializer(data=request.data, context={'request': request, 'animal': animal})
        if serializer.is_valid():
            instance = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def estimated_weight(self, request, date=None):
        '''
        Function to estimate the total animal weight at a given time
        This finds all animals with weight records and interpolates their weight at the given time
        Returns:
         num_animals: total animals included in estimate
         estimated_weight: total estimated weight of num_animals at the provided time
        '''
        response = {}
        weight = 0
        # pull the date query param, if not present default to current time
        try:
            time = parse_datetime(request.GET['date'])
        except:
            time = datetime.now()
        # get all animals with at least a single weight record
        animals = Animal.objects.filter(animalweight__isnull=False).distinct()
        response['num_animals'] = animals.count()
        for animal in animals:
            # get all weight records for the animal & order 
            weights = animal.animalweight_set.order_by('-weigh_date')
            # if only 1 weight record, that's the estimate. add and continue to next
            if weights.count() == 1:
                weight += weights[0].weight
                continue
            # if more than 1 weight, calc the line equation with the 2 closest records
            before = weights.filter(weigh_date__lte=time)
            after = weights.filter(weigh_date__gt=time).reverse()
            if before.count() > 0 and after.count() > 0:
                w1 = before[0]
                w2 = after[0]
            elif before.count() == 0 and after.count() > 0:
                w1 = after[0]
                w2 = after[1]
            elif before.count() > 0 and after.count() == 0:
                w1 = before[0]
                w2 = before[1]
            else:
                # this should never happen but account for it anyway
                # potential place to raise an exception
                pass

            # calculate slope & x-intercept
            m = (w2.weight - w1.weight)/(w2.weigh_date - w1.weigh_date).total_seconds()
            b = w1.weight - m * w1.weigh_date.timestamp()
            # plug in given time and add to total
            weight += m * time.timestamp() + b

        # set the final weight in the response
        response['estimated_total_weight'] = weight
        return Response(response, status=status.HTTP_200_OK)

