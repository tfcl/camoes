from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import Book
from .models import Publisher
from .models import Author
from .models import Requisition

from datetime import datetime
from datetime import timedelta  
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic import FormView
from django.views import View
from django.db.models import Q

from urllib.parse import urlencode
from django import template
from django.shortcuts import redirect
from collections import defaultdict
import logging
import operator
from django.contrib import messages
from library.forms import RequisitionCreateForm
from functools import reduce
logger = logging.getLogger('myLog')
flag_search=False


register = template.Library()

def cancelRequisition(request):


    del request.session['books'][-1]
    request.session.modified = True 
    messages.warning(request, f'Livro descartado') 

    if len(request.session.get('books'))==0:
        return redirect('camoes-home')

    return redirect('requisition-confirm')
    
class RequisitionCreateView(CreateView):
    model = Requisition
    
    form_class=RequisitionCreateForm
 
    def add_days(self):
        
        day=datetime.now() + timedelta(days=15) 
        day=day.strftime('%d-%m-%Y')

        return day

    def form_valid(self, form):
        logging.debug("form_valid")


        self.object = form.save()
        messages.success(self.request, f'Sucesso')
        if len(self.request.session.get('books'))>1:
            del self.request.session['books'][-1]
            self.request.session.modified = True
            
            logging.debug(Requisition.objects.all().count())
            return redirect('requisition-confirm')
        logging.debug(Requisition.objects.all().count())
        return redirect('/library')

        
    def get_initial(self):
        initial = super().get_initial()
        
        initial['book']=1
        return initial
    def get_context_data(self, **kwargs):
        
        context = super(RequisitionCreateView, self).get_context_data(**kwargs)
        user=self.request.session.get('user')
        

         
        book=self.request.session.get('books')[-1]
        selectedBook=Book.objects.get(title=book)
        selectedUser=User.objects.get(username=user)
        
        context={'book':selectedBook, 'user':selectedUser,'end':self.add_days()}
        context['form']=RequisitionCreateForm
        context['form']= RequisitionCreateForm(initial={'book': selectedBook.pk, 'user':selectedUser.pk,})

        #context['form'].fields['book'].initial = selectedBook.pk
        
        
        return context
        

class RequisitionView(TemplateView):
    template_name='library/requisition.html'
    def dispatch(self, request, *args, **kwargs):
        query=self.request.GET.get('Confirm')

        if query:
            
            user=self.request.GET.get('id')
            books=self.request.GET.getlist('book')

            logging.debug(user)
            logging.debug(books)

            self.request.session['user']=user
            self.request.session['books']=books
            return redirect('requisition-confirm')

            logging.debug("oii")
        return super(RequisitionView, self).dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        
        self.request.session['teste']='teste'

        
        context = super(RequisitionView, self).get_context_data(**kwargs)
        
       
        #checkedBooks=context['checkedBooks']
        logging.debug(context)
        checkedBooks=[]
        users=User.objects.all()
        
        
        query=self.request.GET.get('id')
        booksQuery=self.request.GET.getlist('book')
        lengh=len(booksQuery)

        for i, book in enumerate(booksQuery):
            if i != lengh-1:
                checkedBooks.append(book)
            
        logging.debug(checkedBooks)
        
        if query:
            if User.objects.filter(username=query).exists():
                if query and not booksQuery:
                    messages.success(self.request , f'{query} é um utilizador válido !')
                context.update({
                    'id':query
                })

            else:
                messages.warning(self.request, f'{query} não é um utilizador válido !') 
        if not query and booksQuery:
               messages.warning(self.request, f'Tem que indicar um utilizador')

        if 'id' in context:
            if booksQuery:
                if Book.objects.filter(title=booksQuery[-1]).exists():
                    checkedBooks.append(Book.objects.get(title=booksQuery[-1]))
                    logging.debug(checkedBooks)

                    context.update({
                        'checkedBooks':checkedBooks
                })
                    messages.success(self.request, f'Livro Válido')
                else:
                    messages.warning(self.request, f'Livro inválido')
                    
                    context.update({
                        'checkedBooks':checkedBooks
                    })
               
        # for book in context['checkedBooks']:
        #     logging.debug(book)
            
        return context
    
def requisition(request):
    users=User.objects.all()
    
    context={}
    query=request.GET.get('id')
    books=request.GET.getlist('books')
    

    if query:
        if User.objects.filter(username=query).exists():

            logging.debug('oi')
            messages.success(request, f'{query} é um utilizador válido !')
            context={
                'id':query
            }

            
        else:
            messages.warning(request, f'{query} não é um utilizador válido !')
    
        

    return render(request, 'library/requisition.html',context)

# def home(request):

#     context={
#         'books':Book.objects.all(),
#         'publishers':Publisher.objects.all(),
#         'authors':Author.objects.all()
        
#         }
    
  
   
#     return render (request,'library/index.html',context)

def notFound(request):
    return render(request,'library/notFound.html')
def about(request):
    return HttpResponse('<h1>about</h1>')

class BookListView(ListView):

    model=Book
    template_name='library/index.html'
    context_object_name='books'
    
    paginate_by=5
    def get_context_data(self, **kwargs):
        
        context = super(BookListView, self).get_context_data(**kwargs)
        query=self.request.GET.get('q')
        filters=self.request.GET.getlist('checkEditora')
        filtersAuthor=self.request.GET.getlist('checkAuthor')
        filtersYear=self.request.GET.getlist('checkYear')
        pIds=[]
        authors=[]
        aIds=[]
        p=context['paginator']
        
        querysetBook=[]
        years=[]
        yearsAll=[]
        #logging.debug(page1.object_list) 
        for i, page in enumerate(p.page_range, start=1):
            
            querysetBook.append(p.page(i).object_list)
        #logging.debug(querysetBook) 

        if query:
            books=Book.objects.filter(Q(title__icontains=query))
            for book in books:
                pIds.append(book.publisher.pk)
                #aIds.append(book.authors.pk)
                years.append(book.year)

                authors=book.authors.all()

                for author in authors:
                    aIds.append(author.pk)
                
                
        else:
            for book in Book.objects.all():
                yearsAll.append(book.year)
            yearsAll = list( dict.fromkeys(yearsAll) )
            logging.debug(yearsAll)
            
            for books in querysetBook:
                for book in books:
                    pIds.append(book.publisher.pk)
                    #aIds.append(book.authors.pk)

                    authors=book.authors.all()

                    for author in authors:
                        aIds.append(author.pk)
                    years.append(book.year)
        years = list( dict.fromkeys(years) )


        
        logging.debug("oiiiiiiiiiiiiii")

        querysetA= Author.objects.filter(id__in=aIds)
        #logging.debug(books)

        queryset = Publisher.objects.filter(id__in=pIds)
        
        # if query and not filters and not filtersAuthor:
        if query:
            context.update({
            'years':years,
            'publishers1':queryset,
            'authors':querysetA

         })
            return context
    
    
        
        
        if filters and not filtersAuthor and not filtersYear :
            queryset=Publisher.objects.all()
        elif filtersAuthor and not filters and not filtersYear:
            querysetA=Author.objects.all()
        elif filtersYear and not filtersAuthor and not filters:
            years=yearsAll
        elif filtersAuthor and filters:
            pass
        context.update({
            'years':years,

            'publishers1':queryset,
            'authors':querysetA

        })
        
    
    
        return context
    def get_queryset(self): # new
        filters=self.request.GET.getlist('checkEditora')
        filtersAuthor=self.request.GET.getlist('checkAuthor')
        query=self.request.GET.get('q')
        filtersYear=self.request.GET.getlist('checkYear')
        
        if query:
            books=Book.objects.filter(Q(title__icontains=query))

        else:
            books= Book.objects.all()

        if filters or filtersAuthor or filtersYear :
            if filtersAuthor:
                filtersAuthordict={'authors__name__in':[]}
                for filter in filtersAuthor:
                    filtersAuthordict['authors__name__in'].append(filter)
                books=books.filter(**filtersAuthordict )
                logging.debug(books)
            if filters:
                filterdict={'publisher__name__in':[]}
                logging.debug(books)
                for filter in filters:
                    filterdict['publisher__name__in'].append(filter) 
                    logging.debug("-------------------------")

                    logging.debug(filterdict)

                books=books.filter(
                        **filterdict
                    )    
                logging.debug(books)
            if filtersYear:
                filterYearsdict={'year__contains':[]}
                
                for filter in filtersYear:

                    filterYearsdict['year__contains'].append(str(filter)) 

                y=reduce(operator.or_, (Q(year__contains = item) for item in filtersYear))
                logging.debug(y)
                books=books.filter(
                        #**filterYearsdict
                        y

                        )    
                
        return books
