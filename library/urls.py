from django.urls import path
from. import views
from .views import BookListView



from users import views as user_views
urlpatterns = [
    path('',BookListView.as_view() , name='camoes-home'),
    path('about/', views.about, name='camoes-about'),
 
    path('notFound/',views.notFound, name='camoes-notFound'),
  

    path('insertBook', views.insertIsbn, name='insert-isbn'),
    path('createBook', views.BookCreateView.as_view(), name='create-book'),
    path('createAuthor', views.AuthorCreateView.as_view(), name='create-author'),
    path('createPublisher', views.PublisherCreateView.as_view(), name='create-publisher'),
    path('insertManualBook', views.insertManual, name='insert-manual'),
    path('menu', views.menu, name='menu')

    


]
