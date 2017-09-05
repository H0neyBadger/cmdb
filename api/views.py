
from rest_framework.routers import APIRootView as DRFRootView, DefaultRouter

class APIRootView(DRFRootView):
    """
    Root view
    """

    _api_root_dict = {
            "inventory":"inventory-root"
    }

    @property
    def api_root_dict(self):
        return self._api_root_dict

    @api_root_dict.setter
    def api_root_dict(self, *args, **kwargs):
        pass


class InventoryRootView(DRFRootView):
    """
    Root Inventory  view
    """

