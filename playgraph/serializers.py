from rest_framework import serializers

from playgraph.models import BggUser, BggPlay, BggThing

from lib.bggapi import get_bgg_thing


class BggThingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BggThing


class BggPlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = BggPlay

    thing = BggThingSerializer(read_only=True)

    def object_id_to_thing(self, validated_data):
        object_id = validated_data.pop('object_id')
        try:
            return BggThing.objects.get(pk=object_id)
        except BggThing.DoesNotExist:
            # the Thing hasn't been loaded yet
            thing_data = get_bgg_thing(object_id)
            thing_data['name'] = validated_data['name']
            serializer = BggThingSerializer(data=thing_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return serializer.instance

    def create(self, validated_data):
        thing = self.object_id_to_thing(validated_data)
        return BggPlay.objects.create(thing=thing, **validated_data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        del ret['id']
        return ret


class BggUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BggUser

    plays = BggPlaySerializer(many=True, read_only=True)

    def to_internal_value(self, data):
        if not self.instance:
            # Map bgg data names to internal data names
            data['first_name'] = data.pop('firstname', None)
            data['last_name'] = data.pop('lastname', None)
            data['avatar_link'] = data.pop('avatarlink', None)
            data['year_registered'] = data.pop('yearregistered', None)

        return super().to_internal_value(data)
