from rest_framework import serializers

from inventory.models import Host, Interface, IPAddress


class IPAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPAddress
        fields = '__all__'

class InterfaceSerializer(serializers.ModelSerializer):
    ip_address = IPAddressSerializer(many=True)

    def create(self, validated_data):
        ip_data = validated_data.pop('ip_address')
        interface = Interface.objects.create(**validated_data)
        for ip in ip_data:
            ip.update({"interface":interface.pk})
            # force nested serializer control
            serializer = IPAddressSerializer(data=ip)
            serializer.is_valid()
            ip_obj = serializer.save()
        return interface

    class Meta:
        model = Interface
        fields = '__all__'

class HostSerializer(serializers.ModelSerializer):
    interfaces = InterfaceSerializer(many=True)

    def create(self, validated_data):
        interfaces_data = validated_data.pop('interfaces')
        host = Host.objects.create(**validated_data)
        for inter in interfaces_data:
            inter.update({"host":host.pk})
            # force nested serializer control
            print(inter)
            serializer = InterfaceSerializer(data=inter)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        return host

    class Meta:
        model = Host
        #depth = 2
        fields = '__all__'
