from django.urls import path
from .views import MeasureObjectView

urlpatterns = [
    path('measure/', MeasureObjectView.as_view(), name='measure-object')
]