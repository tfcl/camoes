from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import Book
from .models import Publisher, Notification
from .models import Author
from .models import Requisition
from users.models import Profile
from django.core.mail import send_mail

from datetime import datetime
from datetime import timedelta  
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

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
from library.forms import RequisitionCreateForm,BookCreateForm,AuthorCreateForm,PublisherCreateForm
from functools import reduce
from copy import deepcopy
from .consumers import notificationConsumer

from .classLivro import livro,validateIsbn


logger = logging.getLogger('django')
flag_search=False


register = template.Library()
def seeAll(request):
    logger.debug("IS ON SEall")
    Notification.objects.filter(isRead=False).update(isRead=True)
    request.session['seeAll']=True
    
    return redirect('requisition-list')
def cancelRequisition(request):

    
    del request.session['books'][-1]
    request.session.modified = True 
    messages.warning(request, f'Livro descartado') 

    if len(request.session.get('books'))==0:
        return redirect('camoes-home')

    return redirect('requisition-confirm')

def insertIsbn(request):
    if request.GET.get('ISBN'):
        isbn=request.GET.get('ISBN')

    

        if validateIsbn(isbn)==True:
            book=livro()
            authors=[]
            book.getBookByIsbn(isbn)
            print("livro-----------")
            book=book.getBook()
            print(book['Autor'])
            for author in book['Autor']:
                str=author['firstName']+" "+author['lastName']
                print(str)
                if not Author.objects.filter(name=str):
                    
                    
                    
                    newAuthor=Author(name=str,deathYear=0,birthYear=author['birthDate'])
                    newAuthor.save()
                    authors.append(newAuthor.pk)
                    request.session['authors']=authors

                    print("nao existe autor")
                else:
                    authors.append(Author.objects.get(name=str).pk)
                    
                    request.session['authors']=authors

            if not Publisher.objects.filter(name=book['Editora']).exists():
                newPublisher=Publisher(name=book['Editora'])
                newPublisher.save()
                
                
                request.session['publisher']=newPublisher.pk
            else:
                request.session['publisher']=Publisher.objects.get(name=book['Editora']).pk
            request.session['title']=book['Titulo']
            request.session['year']=book['Ano']
            request.session['classification']=book['Etiqueta']
            request.session['colection']=book['Colecção']
            request.session['isbn']=isbn
            
            
            return redirect('create-book')
            messages.success(request,f'ISBN válido')
        else:
            messages.warning(request, f'ISBN inválido') 
    return render(request,'library/inserir.html')
def insertManual(request):
    request.session['insert-mode']=True
    return redirect('create-publisher')

class PublisherCreateView(CreateView):
    model=Publisher
    form_class=PublisherCreateForm
    def form_valid(self, form):
    
        
        print("form_valid-----------Publisher")
        #logging.debug(Requisition.objects.get(pk=1).state)
        if Publisher.objects.filter(name=form.cleaned_data['name']):


            self.request.session['publisher']=Publisher.objects.filter(name=form.cleaned_data['name']).first().pk
            
            return redirect('create-author')


        self.object = form.save()
        if self.request.session.get('insert-mode')!=None:

            self.request.session['publisher']=self.object.pk
            print(self.object.pk)
            print("pk----------------------")
            return redirect('create-author')
        return redirect('camoes-home')    
class AuthorCreateView(CreateView):
    model=Author
    form_class=AuthorCreateForm
    def form_valid(self, form):
        authors=[]
        if 'authors' in self.request.session:
            print("dfdf")
            for author in self.request.session['authors']:
                tempAuthor=deepcopy(author)
                authors.append(tempAuthor)  

        print("form_valid-----------Author")
        print(self.request.POST.get('insertMore'))

        #logging.debug(Requisition.objects.get(pk=1).state)
        
        if Author.objects.filter(name=form.cleaned_data['name']):
            authors.append(Author.objects.filter(name=form.cleaned_data['name']).first().pk)

            if self.request.POST.get('insertMore') == "True":
                self.request.session['authors']=authors
                return redirect('create-author')
            elif self.request.session.get('insert-mode')!=None:
                self.request.session['authors']=authors
                return redirect('create-book')
            else:
                return redirect('camoes-home')


        self.object = form.save()

       

        if self.request.session.get('insert-mode')!=None:


            authors.append(self.object.pk)
            self.request.session['authors']=authors
            if self.request.POST.get('insertMore') == "True":
                return redirect('create-author')

            return redirect('create-book')

        
        

        return redirect('camoes-home')

class InsertIsbnView(TemplateView):
    template_name = 'library/inserir.html'

    # isbn=self.request.Get.get('ISBN')
    # print('ISBN-----------------------------------')
    # print(isbn)
class BookCreateView(CreateView):
    model=Book
    form_class=BookCreateForm
    def get_context_data(self, **kwargs):
        print('----------------------autores')
        print(self.request.session.get('authors'))
        context = super(BookCreateView, self).get_context_data(**kwargs)
        context['form']=BookCreateForm
        context['form']= BookCreateForm(initial={'title': self.request.session.get('title'),
                                                'year': self.request.session.get('year'),
                                                'classification': self.request.session.get('classification'),
                                                'isbn': self.request.session.get('isbn'),
                                                'publisher': self.request.session.get('publisher'),
                                                'authors': self.request.session.get('authors')

        })  
        print(self.request.session.get('authors'))
        return context
    
    def form_valid(self, form):
        print("form_valid-----------Book")
        #logging.debug(Requisition.objects.get(pk=1).state)
        
        
        

        self.object = form.save()
        #print(self.request.session['insert-mode'])
        if 'insert-mode' not in self.request.session:
            del self.request.session['title']
            del self.request.session['year']
            del self.request.session['classification']
            del self.request.session['colection']
            del self.request.session['isbn']
        else:   
            del self.request.session['insert-mode']
        del self.request.session['publisher']
        del self.request.session['authors']
        return redirect('camoes-home')
    
class RequisitionUpdateView(UpdateView):
    model = Requisition
    fields = ['state']
    template_name_suffix = '/requisition-update'
    def form_valid(self, form):
        self.object = form.save()
        Book.objects.filter(pk=self.object.book.pk).update(status='Available')
        messages.success(self.request, f'Livro Entregue')

        return redirect('requisition-list')
    def get_initial(self):
        initial = super().get_initial()
        
        initial['state']="Delivered"
        return initial

class RequisitionListView(ListView):
    model=Requisition
    template_name='library/requisition-list.html'
    context_object_name='requisitions'
    
    paginate_by=5
    def get_queryset(self):
        self.request.GET._mutable = True
        queryset=Requisition.objects.all()
        search=self.request.GET.get('search')
        filter=self.request.GET.get('filter')
        self.request.session['filter']=filter
        if search:
            if User.objects.filter(username=search).exists():
                user=User.objects.get(username=search)
                queryset=Requisition.objects.filter(user=user)
                return queryset
                
            else:
                messages.warning(self.request , 'Não é um utilizador válido !')
                
        if 'seeAll' in self.request.session:
            self.request.GET['filter'] = 'Delayed'
            del self.request.session['seeAll']
            filter='Delayed'
            

  
        if filter=='All' or not filter:
            return queryset
        else:
            queryset=Requisition.objects.filter(state=filter)
            return queryset
    

        
        
            
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
        #logging.debug(Requisition.objects.get(pk=1).state)
        
        send_mail("Nova Requisição",self.create_email(form.cleaned_data['book'].title,self.add_days()),"tlourenco9l@gmail.com",[form.cleaned_data['user'].email],fail_silently= False)

        logger.warning("sdssaddsaasdd")
        #form.instance.end_date=self.add_days()
        logger.warning(form.cleaned_data['user'].pk)
        self.object = form.save()


        messages.success(self.request, f'Sucesso')
        if len(self.request.session.get('books'))>1:
            del self.request.session['books'][-1]
            self.request.session.modified = True
            
            #logging.debug(Requisition.objects.all().count())
            return redirect('requisition-confirm')
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
        

class RequisitionView(TemplateView):
    template_name='library/requisition.html'
    def dispatch(self, request, *args, **kwargs):
        query=self.request.GET.get('Confirm')

        if query:
            
            user=self.request.GET.get('id')
            books=self.request.GET.getlist('book')

            #logging.debug(user)
            #logging.debug(books)

            self.request.session['user']=user
            self.request.session['books']=books
            return redirect('requisition-confirm')

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
    
def requisition(request):
    users=User.objects.all()
    
    context={}
    query=request.GET.get('id')
    books=request.GET.getlist('books')
    

    if query:
        if User.objects.filter(username=query).exists():

            #logging.debug('oi')
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
        
        
        notifications=Notification.objects.all()
        booksdel=Book.objects.all()

        
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
        ##logging.debug(page1.object_list) 
        for i, page in enumerate(p.page_range, start=1):
            
            querysetBook.append(p.page(i).object_list)
        ##logging.debug(querysetBook) 

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
            #logging.debug(yearsAll)
            
            for books in querysetBook:
                for book in books:
                    pIds.append(book.publisher.pk)
                    #aIds.append(book.authors.pk)

                    authors=book.authors.all()

                    for author in authors:
                        aIds.append(author.pk)
                    years.append(book.year)
        years = list( dict.fromkeys(years) )


        
        #logging.debug("oiiiiiiiiiiiiii")

        querysetA= Author.objects.filter(id__in=aIds)
        ##logging.debug(books)

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
                filtersAuthordict={'authors__pk__in':[]}
                for filter in filtersAuthor:
                    filtersAuthordict['authors__pk__in'].append(filter)
                books=books.filter(**filtersAuthordict )
                #logging.debug(books)
            if filters:
                filterdict={'publisher__pk__in':[]}
                #logging.debug(books)
                for filter in filters:
                    filterdict['publisher__pk__in'].append(filter) 
                    #logging.debug("-------------------------")

                    #logging.debug(filterdict)

                books=books.filter(
                        **filterdict
                    )    
                #logging.debug(books)
            if filtersYear:
                filterYearsdict={'year__contains':[]}
                
                for filter in filtersYear:

                    filterYearsdict['year__contains'].append(str(filter)) 

                y=reduce(operator.or_, (Q(year__contains = item) for item in filtersYear))
                #logging.debug(y)
                books=books.filter(
                        #**filterYearsdict
                        y

                        )    
                
        return books
