from django.urls import path
from blog_app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path('search/', views.search, name='search'),
    path("<int:pk>/", views.blog_detail, name="blog_detail"),
    path("category/<int:pk>/", views.category, name="category"),
    path("<int:pk>/add_comment/", views.add_comment, name="add_comment"),
]
