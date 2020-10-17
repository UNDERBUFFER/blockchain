
from .views import Transaction as TransactionView
from django.urls import path


urlpatterns = [
    path('<hash>/', TransactionView.as_view()),
    # path('check/', lambda request: None), # + ?name= ?hash=
]
