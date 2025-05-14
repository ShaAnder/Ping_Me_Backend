"""
URL configuration for ping_me_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from account.views import (AccountViewSet, CookieTokenObtainPairView,
                           CookieTokenRefreshView)
from server.views import ServerCategoryViewSet, ServerListViewSet
from webchat.views import MessageViewSet

router = DefaultRouter()
router.register("api/server_list/select", ServerListViewSet)


router.register(r"api/servers", ServerListViewSet, basename="servers")
router.register(r"api/categories", ServerCategoryViewSet, basename="categories")
router.register(r"api/messages", MessageViewSet, basename="messages")
router.register(r"api/account", AccountViewSet, basename="account") 
# router.register(r"servers/(?P<server_pk>[^/.]+)/last-channel", LastChannelViewSet, basename="last-channel")

urlpatterns = [
    path("admin/", admin.site.urls),
    # view the docs
    path("api/docs/schema/", SpectacularAPIView.as_view(), name="schema"),
    # view the ui
    path("api/docs/schema/ui/", SpectacularSwaggerView.as_view()),
    # jwt paths
    path('api/token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("api/token/refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
    path("", include("account.urls")),
] + router.urls


