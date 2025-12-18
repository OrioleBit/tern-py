from django.urls import path

from .views import CreateListOrderView

urlpatterns = [
    path("", CreateListOrderView.as_view(), name="create_list_order"),
]
