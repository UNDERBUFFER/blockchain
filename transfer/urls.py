
from .views import Transfer as TransferView
from django.urls import path


urlpatterns = [
    path('', TransferView.as_view()),
]
