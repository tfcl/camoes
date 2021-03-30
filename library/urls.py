
from django.urls import path
from. import views
from .views import BookListView, test



from users import views as user_views


urlpatterns = [
    path('',BookListView.as_view() , name='camoes-home'),
    path('about/', views.about, name='camoes-about'),
 
    path('notFound/',views.notFound, name='camoes-notFound'),
  

    path('insertBook', views.insertIsbn, name='insert-isbn'),
    

    path('bookForm', views.BookInsertView.as_view(), name='form-book'),


    
    path('insertManualBook', views.insertManual, name='insert-manual'),
    path('menu', views.menu, name='menu'),
    
    #ajax
    path('ajax/load-categories/', views.load_categories, name='ajax-load-categories'),

    path('ajax/insert-author/', views.insertAuthor, name='ajax-insert-author'),

    path('ajax/insert-publisher/', views.insertPublisher, name='ajax-insert-publisher'),
    path('ajax/check-item/', views.checkItem, name='ajax-check-item'),
    path('ajax/check-identifier/', views.checkIdentifier, name='ajax-check-identifier'),

    path('ajax/get-notifications/', views.getNotifications, name='ajax-get-notifications'),


    

    #teste
    path('test', views.test, name='test'),


]
