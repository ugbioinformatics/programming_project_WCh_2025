from django.urls import path
from .views import (
    BlogListView,
    BlogDetailView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView,
    BlogDeleteAllView, 
    CIRconvert_Views,
    CIRconvert_Views_Reaction,
    Calculate,
)
#umozliwia polaczenie pomiedzy funkcjami na stronie a funkcjami serwera, aby mozna je bylo wyswietlic

urlpatterns = [
    path("post/new/", BlogCreateView.as_view(), name="post_new"),  		#views.py 337
    path("post/<int:pk>/", BlogDetailView.as_view(), name="post_detail"),  	#views.py 332
    path("post/suma/", CIRconvert_Views, name="post_suma"),  			#views.py 134  
    path("post/<int:pk>/edit/", BlogUpdateView.as_view(), name="post_edit"),  	#views.py 343
    path("post/<int:pk>/delete/", BlogDeleteView.as_view(), name="post_delete"),#views.py 349
    path("post/<int:pk>/calculate/", Calculate, name="post_calculate"),  	#views.py 349
    path("post/<int:pk>/show/", BlogDeleteView.as_view(), name="post_show"),  	#views.py 349  #zmenic nazwe "post_show"? na "post_delete_mol"
    path("post/delete-all/", BlogDeleteAllView.as_view(), name="delete_all_posts"),
    path("post/suma2/", CIRconvert_Views_Reaction, name="post_suma2"),     	#views.py 183
    

    path("", BlogListView.as_view(), name="home"),   				# views.py 321
]
