from django.urls import path
from. import views
from .views import BookListView,seeAll
from .views import RequisitionView
from .views import RequisitionCreateView



from users import views as user_views
urlpatterns = [
    path('',BookListView.as_view() , name='camoes-home'),
    path('about/', views.about, name='camoes-about'),
    path('requisition/', RequisitionView.as_view(), name='requisition-create'),
    
    # path('requisition/', views.requisition, name='requisition-create'),
    path('notFound/',views.notFound, name='camoes-notFound'),
    path('requisition/confirm', RequisitionCreateView.as_view(), name='requisition-confirm'),
    path('cancelRequisition', views.cancelRequisition , name='requisition-cancel'),
    path('requisition/list', views.RequisitionListView.as_view(), name='requisition-list'),
    path('requisition/<pk>/', views.RequisitionUpdateView.as_view(), name='requisition-update'),
    path('seeAll/',views.seeAll, name='see-all'),
    path('insertBook', views.insertIsbn, name='insert-isbn'),
    path('createBook', views.BookCreateView.as_view(), name='create-book'),
    path('createAuthor', views.AuthorCreateView.as_view(), name='create-author'),
    path('createPublisher', views.PublisherCreateView.as_view(), name='create-publisher'),
    path('insertManualBook', views.insertManual, name='insert-manual')
    


]
