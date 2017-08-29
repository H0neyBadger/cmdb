from rest_framework import viewsets


from inventory.models import Host, Interface, IPAddress
from inventory.api.serializers import HostSerializer, InterfaceSerializer, IPAddressSerializer


class IPAddressViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing IPAddress
    """
    queryset = IPAddress.objects.all()
    serializer_class = IPAddressSerializer

class InterfaceViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Interface
    """
    queryset = Interface.objects.all()
    serializer_class = InterfaceSerializer
 
class HostViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing assets.
    """
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]
