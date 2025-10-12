from django.urls import path
from .views import StartFocusSessionView, EndFocusSessionView, FocusSessionListView

urlpatterns = [
    path('start/', StartFocusSessionView.as_view(), name='start_focus'),
    path('end/', EndFocusSessionView.as_view(), name='end_focus'), 
    path('history/', FocusSessionListView.as_view(), name='focus_history'),
]
