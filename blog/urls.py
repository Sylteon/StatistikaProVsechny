from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [    
    path('article/<int:id>/', views.article, name='article'),
    path('category/<int:id>/', views.category, name='category'),
    path('plot_graph/<int:id>/', views.plot_graph, name='plot_graph'),
]