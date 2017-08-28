from django.conf.urls import url, include

from rest_framework import routers

from inventory.api.views import HostViewSet, NetInterfaceViewSet, NetIPAddressViewSet

router = routers.DefaultRouter()
router.register(r'hosts', HostViewSet)
router.register(r'interfaces', NetInterfaceViewSet)
router.register(r'ipaddress', NetIPAddressViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]

