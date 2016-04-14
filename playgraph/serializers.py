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

    def to_internal_value(self, data):
        if not self.instance:
            try:
                thing = BggThing.objects.get(pk=data['object_id'])
                data['thing'] = thing.id
            except BggThing.DoesNotExist:
                # the Thing hasn't been loaded yet
                thing_data = get_bgg_thing(data['object_id'])
                thing_data['name'] = data['name']
                serializer = BggThingSerializer(data=thing_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                data['thing'] = serializer.data['id']

        return super().to_internal_value(data)

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
