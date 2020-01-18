from django.urls import path
from sentencepairs import views

urlpatterns = [
    path('sentencepairs/', views.sentencepairs_list)
    # path('sentencepairs/<int:pk>/', views.snippet_detail),
]
