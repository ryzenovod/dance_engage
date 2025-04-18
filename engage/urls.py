from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('dances/', views.dance_list, name='dance_list'),
    path('dances/<int:dance_id>/', views.partner_list, name='partner_list'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('engage/<int:partner_id>/<int:dance_id>/', views.engage, name='engage'),
    path('engagements/', views.engagement_list, name='engagement_list'),
    path('engagements/<int:engagement_id>/confirm/', views.confirm_engagement, name='confirm_engagement'),
    path('engagements/<int:engagement_id>/decline/', views.decline_engagement, name='decline_engagement'),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('skills/', views.select_skills, name='select_skills'),
    path('wants/', views.select_engagements, name='select_engagements'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)