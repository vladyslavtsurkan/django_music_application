from django.urls import path, include

app_name = 'music_app'
urlpatterns = [
    path('api/v1/', include('music_app.api.urls'))
]
