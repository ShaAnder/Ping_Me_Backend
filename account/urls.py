from django.urls import path

from account import views

urlpatterns = [
    path("accounts/", views.AccountList.as_view()),
    path("account/<int:pk>/", views.AccountDetail.as_view()),
]
