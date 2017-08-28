from rest_framework import serializers

from inventory.models import Host, NetInterface, NetIPAddress


class NetIPAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetIPAddress
        fields = '__all__'

class NetInterfaceSerializer(serializers.ModelSerializer):
    netipaddress_set = NetIPAddressSerializer(many=True, read_only=True)
    class Meta:
        model = NetInterface
        fields = '__all__'

class HostSerializer(serializers.ModelSerializer):
    netinterface_set = NetInterfaceSerializer(many=True, read_only=True)
    class Meta:
        model = Host
        #depth = 2
        fields = '__all__'
