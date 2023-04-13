from rest_framework.routers import DefaultRouter

from api.todo.views import TodoViewSet

router = DefaultRouter()
router.register(r'', TodoViewSet, basename='todo')

urlpatterns = router.urls
