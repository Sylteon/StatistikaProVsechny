from django.urls import path
from blog import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'blog'

urlpatterns = [    
    path('article/<int:id>/', views.article, name='article'),
    path('category/<int:id>/', views.category, name='category'),
    path('plot_graph/<int:id>/', views.plot_graph, name='plot_graph'),
    path('check_row_and_years/', views.check_row_and_years, name='check_row_and_years'),
]