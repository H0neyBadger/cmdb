from rest_framework import serializers

from inventory.models import Host, Interface, IPAddress


class IPAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPAddress
        fields = '__all__'

class InterfaceSerializer(serializers.ModelSerializer):
    ip_address = IPAddressSerializer(many=True, read_only=True)
    class Meta:
        model = Interface
        fields = '__all__'

class HostSerializer(serializers.ModelSerializer):
    interfaces = InterfaceSerializer(many=True, read_only=True)
    class Meta:
        model = Host
        #depth = 2
        fields = '__all__'
