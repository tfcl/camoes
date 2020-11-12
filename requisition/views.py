from datetime import datetime
from datetime import timedelta  


from django.core.mail import send_mail


from django.shortcuts import render
from. models import Requisition,Notification
from django.contrib import messages
from django.views.generic import ListView,TemplateView,CreateView,UpdateView,DetailView
from users.models import Profile
from library.models import Book
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .forms import RequisitionCreateForm
import logging
from django.db.models import Q
from functools import reduce
import operator

logger = logging.getLogger('django')


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
class RequisitionView(TemplateView):
    template_name='requisition/requisition.html'
    def dispatch(self, request, *args, **kwargs):
        query=self.request.GET.get('Confirm')

        if query:
            
            user=self.request.GET.get('id')
            books=self.request.GET.getlist('book')

            #logging.debug(user)
            #logging.debug(books)

            self.request.session['user']=user
            self.request.session['books']=books
            return redirect('confirm-requisition')

            #logging.debug("oii")
        return super(RequisitionView, self).dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        
        self.request.session['teste']='teste'

        
        context = super(RequisitionView, self).get_context_data(**kwargs)
        control=False
       
        #checkedBooks=context['checkedBooks']
        #logging.debug(context)
        checkedBooks=[]
        users=User.objects.all()
        
        
        query=self.request.GET.get('id')
        booksQuery=self.request.GET.getlist('book')
        lengh=len(booksQuery)

        for i, book in enumerate(booksQuery):
            if i != lengh-1:
                checkedBooks.append(book)
            
        #logging.debug(checkedBooks)
        
        if query:
            userSelected=Profile.objects.get(number=query).user
            requisitionCount=Requisition.objects.filter(user=userSelected).count()
            print(requisitionCount)
            if Profile.objects.filter(number=query).exists() and requisitionCount<=3:
                if query and not booksQuery:
                    messages.success(self.request , f'{query} é um utilizador válido !')
                context.update({
                    'id':Profile.objects.get(number=query)
                })

            else:
                messages.warning(self.request, f'{query} não é um utilizador válido !') 
        if not query and booksQuery:
               messages.warning(self.request, f'Tem que indicar um utilizador')

        if 'id' in context:
            if booksQuery :
                if Book.objects.filter(title=booksQuery[-1]).exists():
                    if Book.objects.get(title=booksQuery[-1]).status!="Unavailable":
                        control=True
                    else:
                        control=False
                if Book.objects.filter(title=booksQuery[-1]).exists() and control and requisitionCount+lengh<=3:
                    
                    checkedBooks.append(Book.objects.get(title=booksQuery[-1]))
                    
                    

                    context.update({
                        'checkedBooks':checkedBooks
                })
                    messages.success(self.request, f'Livro Válido')
                else:

                    print(booksQuery)

                    if requisitionCount>=3:
                        messages.warning(self.request, f'Atingiu o numero máximo de requisições')
                    elif Book.objects.get(title=booksQuery[-1]).status=="Unavailable":
                        messages.warning(self.request, f'Livro indisponivel de momento')
                    else:
                        messages.warning(self.request, f'Livro inválido')
                    
                    context.update({
                        'checkedBooks':checkedBooks
                    })
               
        # for book in context['checkedBooks']:
        #     #logging.debug(book)
            
        return context
class  RequisitionDetailView(DetailView): 
    model = Requisition
    template_name="requisition/requisition_details.html"

class RequisitionCreateView(CreateView):
    model = Requisition
    
    form_class=RequisitionCreateForm
 
    def add_days(self):
        logging.warning("dsdsfdsfdsfdsfdsfdsfdsfdsfdsfgsgdfdsdsfadsdsfffffff")
        logger.error("dfssssssssssssssssssss")
        day=datetime.now() + timedelta(days=15) 
        day=day.strftime('%d-%m-%Y')

        return day
    def create_email(self,BookName,date):
        logger.warning(date)
        date=str(date)
        return "Acabou de requisitat o livro : "+BookName+"a data limite de entrega é "+date 
    def form_valid(self, form):
        logging.debug("form_valid")
        
        send_mail("Nova Requisição",self.create_email(form.cleaned_data['book'].title,self.add_days()),"tlourenco9l@gmail.com",[form.cleaned_data['user'].email],fail_silently= False)

        #form.instance.end_date=self.add_days()
        self.object = form.save()


        messages.success(self.request, f'Sucesso')
        if len(self.request.session.get('books'))>1:
            del self.request.session['books'][-1]
            self.request.session.modified = True
            
            #logging.debug(Requisition.objects.all().count())
            return redirect('confirm-requisition')
        #logging.debug(Requisition.objects.all().count())
        return redirect('/library')

        
    def get_initial(self):
        initial = super().get_initial()
        
        initial['book']=1
        return initial
    def get_context_data(self, **kwargs):
        
        context = super(RequisitionCreateView, self).get_context_data(**kwargs)
        user1=self.request.session.get('user')
        print("user........"+user1)

         
        book=self.request.session.get('books')[-1]

        print(Book.objects.filter(title=book))
        selectedBook=Book.objects.get(title=book)
        selectedUser=Profile.objects.get(number=user1)
        
        context={'book':selectedBook, 'user':selectedUser,'end':self.add_days()}
        context['form']=RequisitionCreateForm
        context['form']= RequisitionCreateForm(initial={'book': selectedBook.pk, 'user':selectedUser.user.pk})

        #context['form'].fields['book'].initial = selectedBook.pk
        
        
        return context

class RequisitionUpdateView(UpdateView):
    model = Requisition
    fields = ['state']
    template_name_suffix = '/requisition_update'
    def form_valid(self, form):
        self.object = form.save()
        Book.objects.filter(pk=self.object.book.pk).update(status='Available')
        messages.success(self.request, f'Livro Entregue')

        return redirect('requisition-home')
    def get_initial(self):
        initial = super().get_initial()
        
        initial['state']="Delivered"
        return initial

def seeAll(request):
    logger.debug("IS ON SEall")
    Notification.objects.filter(isRead=False).update(isRead=True)
    request.session['seeAll']=True
    
    return redirect('requisition-home')



def cancelRequisition(request):

    
    del request.session['books'][-1]
    request.session.modified = True 
    messages.warning(request, f'Livro descartado') 

    if len(request.session.get('books'))==0:
        return redirect('camoes-home')

    return redirect('confirm-requisition')