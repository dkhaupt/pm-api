from rest_framework import serializers

from .models import Animal, AnimalWeight

class AnimalWeightSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnimalWeight
        fields = ('id', 'weight', 'weigh_date')

    def create(self, validated_data):
        animal = self.context['animal']
        weight = validated_data.pop('weight')
        weigh_date = validated_data.pop('weigh_date')
        weight_record = AnimalWeight.objects.create(animal=animal, weight=weight, weigh_date=weigh_date)
        return weight_record

class AnimalSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    external_id = serializers.IntegerField(required=False)
    weights = AnimalWeightSerializer(source='animalweight_set', many=True, required=False)

    class Meta:
        model = Animal
        fields = ('id', 'external_id', 'weights')

    def get_id(self, args, **kwargs):
        return args.external_id

    def validate_id(self, attrs):
        id = attrs
        if id is None:
            raise serializers.ValidationError('The ID field is required.')
        if Animal.objects.filter(id=id).exists():
            raise serializers.ValidationError('An animal with this ID already exists in the herd.')
        return attrs

    def create(self, validated_data):
        external_id = validated_data.pop('id')
        id = external_id
        animal = Animal.objects.create(id=id, external_id=external_id)
        return animal