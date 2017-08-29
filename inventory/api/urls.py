from django.conf.urls import url, include

from rest_framework import routers

from inventory.api.views import HostViewSet, InterfaceViewSet, IPAddressViewSet

router = routers.DefaultRouter()
router.register(r'hosts', HostViewSet)
router.register(r'interfaces', InterfaceViewSet)
router.register(r'ip_address', IPAddressViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]

