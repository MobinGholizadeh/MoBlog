from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include,path
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/' , user_views.register , name='register'),
    path('profile/' , user_views.profile , name='profile'),
    path('login/' , auth_views.LoginView.as_view(template_name = 'users/login.html') , name='login'),
    path('logout/' , auth_views.LogoutView.as_view(template_name = 'users/logout.html') , name='logout'),
    path('' , include('blog.urls')),

]

# this if says that if we are in DEBUG mode add this to our url patterns
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

