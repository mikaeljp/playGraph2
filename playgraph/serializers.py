from rest_framework import serializers

from playgraph.models import BggUser


class BggUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BggUser

    def to_internal_value(self, data):
        if not self.instance:
            # Map bgg data names to internal data names
            data['first_name'] = data.pop('firstname', None)
            data['last_name'] = data.pop('lastname', None)
            data['avatar_link'] = data.pop('avatarlink', None)
            data['year_registered'] = data.pop('yearregistered', None)

        return super().to_internal_value(data)