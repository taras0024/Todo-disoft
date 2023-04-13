from django.urls import include, path

urlpatterns = [
    path('users/', include('api.users.urls')),
    path('todo/', include('api.todo.urls')),
]
