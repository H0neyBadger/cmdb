from rest_framework import viewsets


from inventory.models import Host, NetInterface, NetIPAddress
from inventory.api.serializers import HostSerializer, NetInterfaceSerializer, NetIPAddressSerializer


class NetIPAddressViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing NetIPAddress
    """
    queryset = NetIPAddress.objects.all()
    serializer_class = NetIPAddressSerializer

class NetInterfaceViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing NetInterface
    """
    queryset = NetInterface.objects.all()
    serializer_class = NetInterfaceSerializer
 
class HostViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing assets.
    """
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]
