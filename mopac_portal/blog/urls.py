from django.urls import path
from .views import (
    BlogListView,
    BlogDetailView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView, 
    CIRconvert_Views,
    CIRconvert_Views_Reaction,
    Calculate,
    BlogCalculateView,
)
#umozliwia polaczenie pomiedzy funkcjami na stronie a funkcjami serwera, aby mozna je bylo wyswietlic

urlpatterns = [

    path("post/new/", BlogCreateView.as_view(), name="post_new"),
    path("post/<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
    path("post/suma/", CIRconvert_Views, name="post_suma"),    
    path("post/<int:pk>/edit/", BlogUpdateView.as_view(), name="post_edit"),
    path("post/<int:pk>/delete/", BlogDeleteView.as_view(), name="post_delete"),  # new
    path("post/<int:pk>/calculate/", Calculate, name="post_calculate"),  # new
    path("post/<int:pk>/calculate/calculations", BlogCalculateView.as_view(), name="post_calculations"),  # new
    path("post/<int:pk>/show/", BlogDeleteView.as_view(), name="post_show"),  # new
    path("post/suma2/", CIRconvert_Views_Reaction, name="post_suma2"),    
    

    path("", BlogListView.as_view(), name="home"),   				# views.py 321
]
