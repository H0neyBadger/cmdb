from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from inventory.models import Host, Interface, IPAddress

class IPAddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = IPAddress
        fields = '__all__'

class InterfaceSerializer(WritableNestedModelSerializer):
    ip_address = IPAddressSerializer(many=True)

    class Meta:
        model = Interface
        fields = '__all__'

class HostSerializer(WritableNestedModelSerializer):
    interfaces = InterfaceSerializer(many=True)

    class Meta:
        model = Host
        #depth = 2
        fields = '__all__'

