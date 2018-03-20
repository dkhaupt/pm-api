from rest_framework import serializers

from .models import Animal, AnimalWeight

class AnimalWeightSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnimalWeight
        fields = ('id', 'weight', 'weigh_date')

    def create(self, validated_data):
        # get the 3 important parameters
        animal = self.context['animal']
        weight = validated_data.pop('weight')
        weigh_date = validated_data.pop('weigh_date')
        # create the new weight record
        weight_record = AnimalWeight.objects.create(animal=animal, weight=weight, weigh_date=weigh_date)
        return weight_record

class AnimalSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    weights = AnimalWeightSerializer(source='animalweight_set', many=True, required=False)

    class Meta:
        model = Animal
        fields = ('id', 'weights')

    def validate_id(self, attrs):
        # validate the id is present & unique
        id = attrs
        if id is None:
            raise serializers.ValidationError('The ID field is required.')
        if Animal.objects.filter(id=id).exists():
            raise serializers.ValidationError('An animal with this ID already exists in the herd.')
        return attrs

    def create(self, validated_data):
        # after validation, create the new animal
        external_id = validated_data.pop('id')
        id = external_id
        animal = Animal.objects.create(id=id, external_id=external_id)
        return animal