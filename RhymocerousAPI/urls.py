from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from rhymocerous.models import *
from rhymocerous.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'poems', Poems, 'poem')
router.register(r'poets', Poets, 'poet')

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]