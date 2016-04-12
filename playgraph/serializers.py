from rest_framework import serializers

from playgraph.models import BggUser, BggPlay


class BggPlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = BggPlay

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
