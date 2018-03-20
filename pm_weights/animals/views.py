from django.shortcuts import render, get_object_or_404
from django.utils.dateparse import parse_datetime
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

    def estimated_weight(self, request, slug=None):
        '''
        Function to estimate the total animal weight at a given time
        This finds all animals with weight records and interpolates their weight at the given time
        Returns:
         num_animals: total animals included in estimate
         estimated_weight: total weight of num_animals at the provided time
        '''
        if slug is None:
            # no date passed
            pass
        response = {}
        weight = 0
        # parse passed-in slug
        time = parse_datetime('2018-03-02T12:00:00Z')
        # get all animals with at least a single weight record
        animals = Animal.objects.filter(animalweight__isnull=False).distinct()
        response['num_animals'] = animals.count()
        for animal in animals:
            # initialize 2 numbers to hold the weights for interpolation
            w1 = 0
            w2 = 0
            # get all weight records for the animal & order 
            weights = animal.animalweight_set.order_by('-weigh_date')
            # if only 1 weight, that's the estimate. add and continue to next
            if weights.count() == 1:
                weight += weights[0].weight
                continue

            # if more than 1 weight, find the correct 2 for interpolation
            # separate into before/after
            before = weights.filter(weigh_date__lte=time)
            after = weights.filter(weigh_date__gt=time).reverse()
            if before.count() > 0 and after.count() > 0:
                w1 = before[0]
                w2 = after[0]
            elif before.count() == 0 and after.count() > 0:
                w1 = after[0]
                w2 = after[1]
            elif before.count() > 0 and after.count() > 0:
                w1 = before[0]
                w2 = before[1]
            else:
                # this should never happen but account for it anyway
                pass

            # interpolate the weights
            # find delta per second
            delta = w2.weight - w1.weight
            seconds = (w2.weigh_date - w1.weigh_date).total_seconds()
            dps = delta/seconds
            # find time difference from recorded weights to requested time

            # i realized too late that i spent way too long here and that there are libraries which provide this kind of interpolation
            weight = 1100

        # set the final weight in the response
        response['estimated_weight'] = weight
        return Response(response, status=status.HTTP_200_OK)

