from library.models import Type
from datetime import datetime, timezone
from datetime import timedelta  
import json

from django.core.mail import send_mail


from django.shortcuts import render
from. models import Requisition,Notification
from django.contrib import messages
from django.views.generic import ListView,TemplateView,CreateView,UpdateView,DetailView
from users.models import Profile
from library.models import Book,Item

from django.contrib.auth.models import User
from django.shortcuts import redirect
from .forms import RequisitionCreateForm

import logging
from django.db.models import Q
from functools import reduce
import operator
from django.http import HttpResponse
logger = logging.getLogger('django')
from django.http import JsonResponse
from django.core import serializers

from .constants import days_limit,max_requisitions



class RequisitionListView(ListView):
    searchUser=""
    model=Requisition
    template_name='requisition/requisition_list.html'
    context_object_name='requisitions'
    
    paginate_by=5
    



    def get_queryset(self):
        
        self.request.GET._mutable = True
        queryset=Requisition.objects.all()
        search=self.request.GET.get('search')
        filters=self.request.GET.getlist('filter')
        filtersDict={'state__contains':[]}
        filtersReq=[]
        
        
        orderBy= self.request.GET.get("orderby")
        
        
        if orderBy == 'recent':

            

            queryset=queryset.order_by('-date')

        elif orderBy =='old':
            queryset=queryset.order_by('date')
            print(orderBy)

        else:   
            queryset=queryset.order_by('date')

        if 'search' in self.request.GET:
            if search.isnumeric():
                if Profile.objects.filter(number=search).exists():
                    user=Profile.objects.get(number=search).user
                    queryset=queryset.filter(user=user)
                    self.searchUser=Profile.objects.get(number=search)
                else:
                    messages.warning(self.request, f'Utilizador não existe')

        if 'filter' in self.request.GET:
            for filter in filters:
                #delayed
                if filter=='d':
                    filtersReq.append('Delayed')
                   
                #on going
                elif filter=='og':

                    filtersReq.append('Not Delivered')
                    
                #finished
                elif filter=='f':
                    filtersReq.append('Delivered')
            y=reduce(operator.or_, (Q(state__contains = item) for item in filtersReq))
            queryset=queryset.filter(y)
                      
        return queryset   
    

    def get_context_data(self, **kwargs):
        


        context = super(RequisitionListView, self).get_context_data(**kwargs)
        
        orderBy= self.request.GET.get("orderby")
        
        if self.searchUser!="":
            context.update({'searchUser':self.searchUser})
        if 'orderby' in self.request.GET:
            context.update({'orderBy':orderBy})
        else:  
            context.update({'orderBy':'recent'})
            
        return context

class  RequisitionDetailView(DetailView): 
    model = Requisition
    template_name="requisition/requisition_details.html"



class RequisitionUpdateView(UpdateView):
    model = Requisition
    fields = ['state','deliverDate']
    template_name = 'requisition/requisition_update.html'

    def get_context_data(self, **kwargs):

        context = super(RequisitionUpdateView, self).get_context_data(**kwargs)


        requisition=self.object
        user=self.object.user
        profile=Profile.objects.get(pk=self.object.user.pk)

        context.update({
            
            'profile':profile,
            'requsition':requisition

        })
        print(context)
        return context



    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, f'Livro Entregue')

        return redirect('requisition-home')
    def get_initial(self):
        initial = super().get_initial()
        
        initial['state']="D"
        initial['deliverDate']=datetime.now()
        return initial

def seeAll(request):
    logger.debug("IS ON SEall")
    Notification.objects.filter(isRead=False).update(isRead=True)
    request.session['seeAll']=True
    
    return redirect('requisition-home')




def requisitionEntry(request):
    if request.method=='GET':
        return render(request,'requisition/requisition.html')

    if request.method == 'POST':
        
        user=User.objects.get(id=request.POST['user'])
        
        print("POSTTTTTTTT")
        print(request.POST['user'])
        books=request.POST.getlist('book')
        for book in books:
            itemObject=Item.objects.get(id=book)
            new=Requisition.create(user,itemObject)
            new.save()
            
        return redirect('requisition-home')


def add_days():

    day=datetime.now() + timedelta(days=days_limit) 
    day=day.strftime('%d-%m-%Y')

    return day
#ajax



def checkUser(request):
    
    inputUser= request.GET.get("user")
   #verificar também se está bloqueado
    if User.objects.filter(username=inputUser).exists():
        
        user=User.objects.get(username=inputUser)
        allowedRequisitions=max_requisitions-user.profile.active_requisitions
        if user.profile.state=='A':
            if allowedRequisitions>0:
                print('allowed requisitions')
                
                print(allowedRequisitions)
                
                return render(request, 'requisition/ajax/add_books.html', {'user1':user,'allowedRequisitions':allowedRequisitions,'deadline':add_days()})
            else:
                return HttpResponse(0)
        else:
            return HttpResponse(1)

    else:
        return HttpResponse(-1)


def addBookCopy(request):
    inputBook=request.GET.get("book")
    print(inputBook)

    if Book.objects.filter(id=inputBook).exists():
        if Book.objects.get(id=inputBook).state!='U':   
        
            book=Book.objects.get(id=inputBook)
        
        
        
            return JsonResponse(serializers.serialize('python', [book,]),safe=False)
        else:
            return HttpResponse(0)
    else:
        return HttpResponse(-1)

def seeNotification(request, pk):
    print("from seeNotification")
    
    print(pk)

    notification=Notification.objects.get(pk=pk)

    notification.isRead=True
    notification.save(update_fields=["isRead"])
    return redirect('detail-requisition', notification.requisition.pk)

def addBook(request):
    inputBook=request.GET.get("book")
    inputType=request.GET.get("type")
    typeFilter=None
    print("view, addBook")
    print(inputType)

    if inputType =="b1":
        typeFilter=1
    elif inputType=="b2":
        typeFilter=2

    elif inputType=="m1":
        typeFilter=3

    elif inputType=="m2":
        typeFilter=4


    if  Item.objects.filter(identifier=inputBook).filter(type=typeFilter).exists():
           
        
        book=Item.objects.filter(identifier=inputBook).get(type=typeFilter)
        
        print("teste")
        if book.content_object.state!="U":

            data={
                "identifier":book.__str__(),
                "book":book.content_object.title,
                "item_pk":book.pk

            }
            
            dataJson = json.dumps(data)

            return JsonResponse(dataJson,safe=False)
        else:
            return HttpResponse(0)
    else:
        return HttpResponse(-1)
        



def confirmRequisition(request):

    return render(request, 'requisition/ajax/confirm.html', {})

        