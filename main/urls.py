from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.main, name="index"),
    path('<int:blog_id>', views.blog, name="blog_by_id"),
    path('login', views.log_in, name="login"),
    path('logout', views.log_out, name="logout"),
    path('signup', views.sign_up, name="signup"),
    path('blog', views.get_blog_list, name="blog"),
    path('delete/<int:post_id>/', views.delete_post, name="delete"),
    path('news', views.get_info, name="news"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)