from django.shortcuts import render, get_object_or_404
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
        queryset = Animal.objects.all()
        animal = get_object_or_404(queryset, pk=id)
        serializer = AnimalWeightSerializer(data=request.data, context={'request': request, 'animal': animal})
        if serializer.is_valid():
            instance = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def retrieve(self, request, id=None):
    #     queryset = Animal.objects.all()
    #     animal = get_object_or_404(queryset, external_id=id)
    #     serializer = AnimalSerializer(animal)
    #     return Response(serializer.data)

    # def animal(self, request, format=None):
    #     if request.method == 'POST':
    #         # create an animal
    #         serializer = AnimalSerializer(data=request.data)
    #         if serializer.is_valid():
    #             instance = serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     elif request.method == 'GET':
    #         # get all animals
    #         queryset = Animal.objects.all()
    #         serializer = AnimalSerializer(queryset, many=True)
    #         return Response(serializer.data)
    #     else:
    #         # disallowed method
    #         return Response(status.HTTP_403_FORBIDDEN)

