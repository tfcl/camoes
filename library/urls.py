from django.urls import path
from. import views
from .views import BookListView
from .views import RequisitionView
from .views import RequisitionCreateView



from users import views as user_views
urlpatterns = [
    path('',BookListView.as_view() , name='camoes-home'),
    path('about/', views.about, name='camoes-about'),
    path('requisition/', RequisitionView.as_view(), name='requisition-create'),
    
    # path('requisition/', views.requisition, name='requisition-create'),
    path('notFound/',views.notFound, name='camoes-notFound'),
    path('register/', user_views.register, name='register'),
    path('requisition/confirm', RequisitionCreateView.as_view(), name='requisition-confirm'),
    path('cancelRequisition', views.cancelRequisition , name='requisition-cancel'),
    path('requisition/list', views.RequisitionListView.as_view(), name='requisition-list'),
    path('requisition/<pk>/', views.RequisitionUpdateView.as_view(), name='requisition-update')




]
