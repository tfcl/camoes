
import copy
from django.db.models.deletion import SET_NULL
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import Book
from .models import Publisher
from .models import Author
from .models import Category, Type, Item_type, Magazine

from requisition.models import Requisition,Notification

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
from library.forms import BookCreateForm,AuthorCreateForm,PublisherCreateForm
import json

from functools import reduce
from copy import deepcopy
from .consumers import notificationConsumer

from django.contrib.postgres.search import TrigramSimilarity

from .classLivro import livro,validateIsbn

from django.http import JsonResponse
from django.core import serializers
logger = logging.getLogger('django')
flag_search=False


register = template.Library()



def test(request):
    user=User.objects.get(id=1)
    book=Book.objects.get(id=5)
    magazine=Magazine.objects.get(id=1)

    tDoados=Type.objects.get(id=1)
    tMagazines=Type.objects.get(id=2)

    i1=Item_type(content_object=book,identifier=1, type=tDoados)
    i2=Item_type(content_object=magazine,identifier=1, type=tMagazines)
    i3=Item_type(content_object=user,identifier=2, type=tMagazines)


    # print(i1.object_id)
    # print(i1.content_type)

    

    print(magazine.item_type.get().type)

def menu(request):
    
    if Requisition.objects.filter(state='Delayed').exists():
          
        context= {'requisitions':True}
    else:
       context= {'requisitions':False} 

    print(context)
    return render(request,'library/menu.html',context)



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
        PublisherCreateView.as_view()(self.request)
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




#ajax


def load_categories(request):
    
    print("load categories")



    categoriesHtml=[]
    categoriesAll=[]
    category_id = request.GET.get('category')
    
    
    category=Category.objects.get(id=category_id)
    
    categories=Category.objects.filter(parentPk=category)


    print(categories)

    return JsonResponse(serializers.serialize('python', categories),safe=False)




def insertIsbn(request):

    if request.method=='GET':
        categories=Category.objects.filter(depth=0)

        isbn=request.GET.get('ISBN')
        if isbn=="-1":
            return render(request, 'library/book_form.html', {'categories':categories})


    

        if validateIsbn(isbn)==True:
            book=livro()
            authors=[]
            print(book.getBookByIsbn(isbn))


            book.getBookByIsbn(isbn)
            if book.getBookByIsbn(isbn)==-1:
                return render(request, 'library/book_form.html', {'categories':categories, 'error':'Livro não encontrado, insira manualmente'})


            print("livro-----------")

            book=book.getBook()

            for author in book['Autor']:
                str=author['firstName']+" "+author['lastName']
                str=str.lstrip()
                queryset=Author.objects.annotate(similarity=TrigramSimilarity('name', str),).filter(similarity__gt=0.4).order_by('-similarity')
                
                print(queryset)
                
                
                if not queryset:
                    birthYear=author['birthDate']
                    deathYear=author['deathDate']
                    if birthYear=="":
                        birthYear=None
                    if deathYear=="":
                        deathYear=None

        
                    newAuthor=Author.create(str,birthYear,deathYear)
                    
                    newAuthor.save()

                    print("Guardou")
                    print(str)
                    print(newAuthor)
                    authors.append(newAuthor)
                    

                    print("nao existe autor")
                else:
                    print("existe autor")

                    authors.append(queryset[0])
                    print(authors)
                    
            
            querysetP=Publisher.objects.annotate(similarity=TrigramSimilarity('name', book['Editora']),).filter(similarity__gt=0.4).order_by('-similarity')

            if not querysetP:
                
                #falta implementar o endereço
                address=""
                newPublisher=Publisher.create(book['Editora'],address)
                newPublisher.save()
                
                print(newPublisher)
                
            else:
                publisher=querysetP[0]

            
            context={
                'categories':categories,
                'title':book['Titulo'],
                'year':book['Ano'],
                'authors':authors,
                'publisher': publisher 

            }

            #Classification=book['Etiqueta']
            #falta implementar conversor de classificação
            #falta implementar ISBN

            #request.session['colection']=book['Colecção']
            #request.session['isbn']=isbn
            

            return render(request, 'library/book_form.html', context)
   
        else:
            return HttpResponse(-1)    
    #         return redirect('create-book')
    #         messages.success(request,f'ISBN válido')
    #     else:
    #         messages.warning(request, f'ISBN inválido') 
    # return render(request,'library/inserir.html')



def insertAuthor(request):



    if request.method=='GET':
        
        inputName=request.GET.get("name")
        
        print("Sarch----------------------------------------------------------------------------------------")
        queryset=Author.objects.annotate(similarity=TrigramSimilarity('name', inputName),).filter(similarity__gt=0.3).order_by('-similarity')
        if queryset:
            data=[]
            dataDict={} 
            pk=None
            name=None
            for elem in queryset:
                tempPk=elem.pk
                tempName=elem.__str__()
                dataDict={
                    "pk":tempPk,
                    "name":tempName
                }
                data.append(dataDict.copy())

            dataJson1=json.dumps(data)

            return JsonResponse(dataJson1,safe=False)
        else:


            return HttpResponse(-1)

    if request.method == 'POST':
        form=request.POST.get('form')
        print(form)
        form=json.loads(form)
        name=form['name']
        birthyear=form['birthyear']
        deathyear=form['deathyear']
       
        print(name)
        print(birthyear)
        print(deathyear)
        if birthyear=="":
            birthyear=None
        if deathyear=="":
            deathyear=None

        new=Author.create(name,birthyear,deathyear)
        new.save()
        

        data={"pk":str(new.pk),"name":new.__str__()}

        dataJson=json.dumps(data)

        print("view!!!")
        print(data)
        return JsonResponse(dataJson,safe=False)






def insertPublisher(request):
    if request.method=='GET':
        inputName=request.GET.get("name")
        queryset=Publisher.objects.annotate(similarity=TrigramSimilarity('name', inputName),).filter(similarity__gt=0.3).order_by('-similarity')
        if queryset:
 
            
            print(queryset)
            dataJson1=list(queryset)
            return JsonResponse(serializers.serialize('python', dataJson1),safe=False)
            
        else:


            return HttpResponse(-1)



    if request.method == 'POST':
        form=request.POST.get('form')
        print(form)
        form=json.loads(form)
        name=form['name']
        address=form['address']
       
        print(name)
       
        # if address=="":
        #     address=None
    
        new=Publisher.create(name,address)
        new.save()
        

        data={"pk":str(new.pk),"name":new.name}

        dataJson=json.dumps(data)

        print("view!!!")
        print(data)
        return JsonResponse(dataJson,safe=False)


class BookInsertView(View):
    def get(self, request, *args, **kwargs):



        return render(request, 'library/inserir.html')
    def post(self, request, *args, **kwargs):
        authors=[]
        author=None
        
        category=None

        categories=Category.objects.filter(depth=0)
        print("from POST Insert book")
        print(request.POST)
        form=request    
        
        
        title= request.POST.get('title', None) 
        authorsPk= request.POST.getlist('authors', [1]) 
        publisherPk= request.POST.get('publisher', 1) 
        year= request.POST.get('year') 
        categoryPk= request.POST.get('category', None) 
     
        print(year)
        #get publisher
        publisher=Publisher.objects.get(id=publisherPk)

        #get authors
        authors=Author.objects.filter(id__in=authorsPk)
        print(authors)
        #get category
        if categoryPk != "":
            category=Category.objects.get(pk=categoryPk)
        else:
            category=None

        #year
        if year =="":
            year=None

        new=Book.create(title,publisher,category,year,"sddsa")
        new.save()           
        new.authors.set(authors)
        print(new.authors)

        messages.success(request,f'Livro '+str(new.pk)+' Inserido com exito')
        return redirect('camoes-home')
        
        

class BookCreateView(CreateView):
    model=Book
    form_class=BookCreateForm
    
    # def dispatch(self, request, *args, **kwargs):
    #     print("dispash----------")
    #     form=self.form_class(self.request.POST)
    #     print(form)
    #     return self.form_valid(form)


    
    def get_context_data(self, **kwargs):
        print('----------------------autores')
        #print(self.form_class(self.request.POST))
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
        context['categories']=Category.objects.filter(depth=0)
        return context
    def form_invalid(self, form):

        print(form)
        return self.render_to_response(self.get_context_data(form=form))


    def form_valid(self, form):
        print("form_valid-----------Book")
        #logging.debug(Requisition.objects.get(pk=1).state)
        print(form)
        
        
        

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
    

            


def notFound(request):
    return render(request,'library/notFound.html')
def about(request):
    return HttpResponse('<h1>about</h1>')

class BookListView(ListView):
    
    model=Book
    template_name='library/index.html'
    context_object_name='books'
    
    paginate_by=5

    queryset=None
    search=None
    selectAuthors=None

    selectPublishers=None


    def get_queryset(self): # new
        filters=self.request.GET.getlist('checkEditora')
        filtersAuthor=self.request.GET.getlist('checkAuthor')
        query=self.request.GET.get('q')
        filtersYear=self.request.GET.getlist('checkYear')
        
        if query:
            books=Book.objects.filter(Q(title__icontains=query))
            self.search=books

            
                  

        else:
            books= Book.objects.all()

        if filters or filtersAuthor or filtersYear :
            if filtersAuthor:
                filtersAuthordict={'authors__pk__in':[]}
                selectAuthorsdict={'pk__in':[]}
                for filter in filtersAuthor:
                    selectAuthorsdict['pk__in'].append(filter)
                    
                    filtersAuthordict['authors__pk__in'].append(filter)
                books=books.filter(**filtersAuthordict )
                       

                self.selectAuthors=Author.objects.filter(**selectAuthorsdict)
                #print(self.selectAuthors)
                #logging.debug(books)
            if filters:

                selectPublishersdict={'pk__in':[]}
                filterdict={'publisher__pk__in':[]}
                #logging.debug(books)
                for filter in filters:
                    filterdict['publisher__pk__in'].append(filter) 
                    selectPublishersdict['pk__in'].append(filter)

                    #logging.debug("-------------------------")

                    #logging.debug(filterdict)

                books=books.filter(
                        **filterdict
                    )    
                self.selectPublishers=Publisher.objects.filter(**selectPublishersdict)
                print("----------------------------book")
                print(books)

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
        
        self.queryset=books       

        return books
    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        books=self.queryset
        print("editora-------------------")
        print(self.selectPublishers)
        #publisher filter variables
        
        querysetPublisher=Publisher.objects.all()
        

        publishersIds=[]
        publishersSelectedIds=[]
        publishersRelatedIds=[]
        
        #author filter variables
        showAuthors = 5
        seeAuthors=self.request.GET.get('seeAuthor')
        querysetAuthor=Author.objects.all()
        

        authorsIds=[]
        authorsSelectedIds=[]
        authorsRelatedIds=[]


        if self.search:
            for book in self.search:
                authors=book.authors.all()

                for author in authors:
                    authorsIds.append(author.pk) 
                publishersIds.append(book.publisher.pk)               
            querysetAuthor=querysetAuthor.filter(id__in=authorsIds)  
            querysetPublisher=querysetPublisher.filter(id__in=publishersIds)

        #authors filter logic
        
        if seeAuthors:
            showAuthors=int(seeAuthors)


        if self.selectAuthors:


            context.update({'selectedAuthors':self.selectAuthors})

            # for book in self.queryset:

            #     for author in authors:
            #         authorsRelatedIds.append(author.pk)                
            # querysetRelatedAuthors=querysetAuthor.filter(id__in=authorsRelatedIds)

            for author in self.selectAuthors:
                authorsSelectedIds.append(author.pk)

            querysetAuthor=querysetAuthor.exclude(pk__in=authorsSelectedIds)
            #.exclude(pk__in=authorsRelatedIds)

            #querysetRelatedAuthors=querysetRelatedAuthors.exclude(pk__in=authorsSelectedIds)
            
            # print(querysetAuthor)
        # querysetAuthor=querysetAuthor[:showAuthors]
        
        
        #publishers filter logic 

        if self.selectPublishers:
            
            for publisher in self.selectPublishers:
                publishersSelectedIds.append(publisher.pk)
            
            querysetPublisher=querysetPublisher.exclude(pk__in=publishersSelectedIds)
            context.update({'selectedPublishers':self.selectPublishers})
        
        if self.selectAuthors or self.selectPublishers:
            for book in self.queryset:
                #authors
                authors=book.authors.all()

                for author in authors:
                    authorsRelatedIds.append(author.pk)                
                #publishers
                publishersRelatedIds.append(book.publisher.pk)
            
            
            
            querysetRelatedAuthors=Author.objects.filter(id__in=authorsRelatedIds).exclude(pk__in=authorsSelectedIds)
            querysetAuthor=querysetAuthor.exclude(pk__in=authorsRelatedIds)
            context.update({'relatedAuthors':querysetRelatedAuthors})

            querysetRelatedPublishers=Publisher.objects.filter(id__in=publishersRelatedIds).exclude(pk__in=publishersSelectedIds)
            querysetPublisher=querysetPublisher.exclude(pk__in=publishersRelatedIds)
            context.update({'relatedPublishers':querysetRelatedPublishers})

        else:
            # context.update({'relatedAuthors':Author.objects.all})
            # context.update({'relatedPublishers':querysetRelatedAuthors})
            pass

        context.update({'publishers':querysetPublisher})
        print(querysetAuthor)

        context.update({'authors':querysetAuthor,'seeAuthors':showAuthors})
        return context