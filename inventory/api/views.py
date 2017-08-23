from rest_framework import viewsets


from inventory.models import Host
from inventory.api.serializers import HostSerializer


class HostViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing assets.
    """
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    #permission_classes = [IsAccountAdminOrReadOnly]
