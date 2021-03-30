
import copy
from django.contrib.postgres import search
from django.db.models.deletion import SET_NULL
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import Book
from .models import Publisher
from .models import Author
from .models import Category, Type, Item, Magazine
from django.db.models import Max, query
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

from django.db.models import Q

logger = logging.getLogger('django')
flag_search=False


register = template.Library()



def test(request):
    
    # book1=Book.objects.get(id=1)
    # book2=Book.objects.get(id=2)
    book1=Book.objects.get(id=2)
    book2=Book.objects.get(id=3)
    book3=Book.objects.get(id=4)
    book4=Book.objects.get(id=5)
    book5=Book.objects.get(id=6)
    book6=Book.objects.get(id=7)
    book7=Book.objects.get(id=8)
    book8=Book.objects.get(id=9)
    book9=Book.objects.get(id=10)
    book10=Book.objects.get(id=11)
    

    # magazine1=Magazine.objects.get(id=1)

    tDoados=Type.objects.get(id=1)
    # tComprados=Type.objects.get(id=2)
    # tRevistas=Type.objects.get(id=3)

    # tMagazines=Type.objects.get(id=2)

    #i1=Item.objects.get(id=5)
    i1=Item(content_object=book2,identifier=2, type=tDoados)
    i2=Item(content_object=book3,identifier=3, type=tDoados)
    i3=Item(content_object=book4,identifier=4, type=tDoados)
    i4=Item(content_object=book5,identifier=5, type=tDoados)
    i5=Item(content_object=book6,identifier=6, type=tDoados)
    i6=Item(content_object=book7,identifier=7, type=tDoados)
    i7=Item(content_object=book8,identifier=8, type=tDoados)
    i8=Item(content_object=book9,identifier=9, type=tDoados)
    i9=Item(content_object=book10,identifier=11, type=tDoados)
    


    # i3=Item(content_object=magazine1,identifier=1, type=tRevistas)
    ##print(i1.content_object.title)

    # #print(i1.object_id)
    # #print(i1.content_type)

    

    i1.save()
    i2.save()
    i3.save()
    i4.save()

    i5.save()
    i6.save()
    i7.save()
    i8.save()
    i9.save()

    

def menu(request):
    
    if Requisition.objects.filter(state='Delayed').exists():
          
        context= {'requisitions':True}
    else:
       context= {'requisitions':False} 

    #print(context)
    return render(request,'library/menu.html',context)



def insertManual(request):
    request.session['insert-mode']=True
    return redirect('create-publisher')



class InsertIsbnView(TemplateView):
    template_name = 'library/inserir.html'

    # isbn=self.request.Get.get('ISBN')
    # #print('ISBN-----------------------------------')
    # #print(isbn)




#ajax

def getNotifications(request):
    print("from get notifications")

    notifications=Notification.objects.filter(isRead=False)

    return JsonResponse(serializers.serialize('python', notifications),safe=False)

def incrementIdentifier(typeFilter, queryset,isRecursive=False):
    #print("def increment")

    
    
    identifier=queryset.aggregate(Max('identifier'))
    tempIdentifier=identifier['identifier__max']
    tempObject=None
    queryset=queryset.order_by('-identifier')
    tempArray=[]
    


    slice=-1
    flagViolated=False
   
    #queryset=queryset[::-5]
    #print(queryset)
    for object in queryset:
        #print(object.identifier)
        slice+=1
        if object.identifier!=tempIdentifier:
            
            flagViolated=True
        tempIdentifier-=1
        if flagViolated==True:
            
            #print("violated")
            queryset=queryset[slice:]
            for object1 in queryset:
                tempArray.append(object1.pk)
            #print(tempArray)
            return incrementIdentifier(typeFilter,Item.objects.filter(pk__in=tempArray),True)
            tempObject=object
            break
    #print(queryset[slice:])
    
    ##print(queryset)

    ##print(slice)

    return identifier['identifier__max']+1



def checkIdentifier(request):
    type=request.GET.get('item')
    identifier=request.GET.get('identifier')

    #print(type)
    #print(identifier)

    if type=="I":
        typeFilter=1
    elif type=="F":
        typeFilter=2  

    items=Item.objects.filter(type=typeFilter).filter(identifier=identifier)

    if Item.objects.filter(type=typeFilter).filter(identifier=identifier).exists():
        return HttpResponse(-1)
    else:
        return HttpResponse(0)

def checkItem(request):

    #print("checkItem")
    typeFilter=None
    type=request.GET.get('item')
    #print(type)

    if type=="I":
        typeFilter=1
    elif type=="F":
        typeFilter=2  

    
    items=Item.objects.filter(type=typeFilter)

    

    identifier=incrementIdentifier(typeFilter,items)
    return HttpResponse(identifier)

def load_categories(request):
    
    #print("load categories")



    categoriesHtml=[]
    categoriesAll=[]
    category_id = request.GET.get('category')
    
    
    category=Category.objects.get(id=category_id)
    
    categories=Category.objects.filter(parentPk=category)


    #print(categories)

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
            #print(book.getBookByIsbn(isbn))


            book.getBookByIsbn(isbn)
            if book.getBookByIsbn(isbn)==-1:
                return render(request, 'library/book_form.html', {'categories':categories, 'error':'Livro não encontrado, insira manualmente'})


            #print("livro-----------")

            book=book.getBook()

            for author in book['Autor']:
                str=author['firstName']+" "+author['lastName']
                str=str.lstrip()
                queryset=Author.objects.annotate(similarity=TrigramSimilarity('name', str),).filter(similarity__gt=0.4).order_by('-similarity')
                
                #print(queryset)
                
                
                if not queryset:
                    birthYear=author['birthDate']
                    deathYear=author['deathDate']
                    if birthYear=="":
                        birthYear=None
                    if deathYear=="":
                        deathYear=None

        
                    newAuthor=Author.create(str,birthYear,deathYear)
                    
                    newAuthor.save()

                    #print("Guardou")
                    #print(str)
                    #print(newAuthor)
                    authors.append(newAuthor)
                    

                    #print("nao existe autor")
                else:
                    #print("existe autor")

                    authors.append(queryset[0])
                    #print(authors)
                    
            
            querysetP=Publisher.objects.annotate(similarity=TrigramSimilarity('name', book['Editora']),).filter(similarity__gt=0.4).order_by('-similarity')

            if not querysetP:
                
                #falta implementar o endereço
                address=""
                newPublisher=Publisher.create(book['Editora'],address)
                newPublisher.save()
                
                #print(newPublisher)
                
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
        
        #print("Sarch----------------------------------------------------------------------------------------")
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
        #print(form)
        form=json.loads(form)
        name=form['name']
        birthyear=form['birthyear']
        deathyear=form['deathyear']
       
        #print(name)
        #print(birthyear)
        #print(deathyear)
        if birthyear=="":
            birthyear=None
        if deathyear=="":
            deathyear=None

        new=Author.create(name,birthyear,deathyear)
        new.save()
        

        data={"pk":str(new.pk),"name":new.__str__()}

        dataJson=json.dumps(data)

        #print("view!!!")
        #print(data)
        return JsonResponse(dataJson,safe=False)






def insertPublisher(request):
    if request.method=='GET':
        inputName=request.GET.get("name")
        queryset=Publisher.objects.annotate(similarity=TrigramSimilarity('name', inputName),).filter(similarity__gt=0.3).order_by('-similarity')
        if queryset:
 
            
            #print(queryset)
            dataJson1=list(queryset)
            return JsonResponse(serializers.serialize('python', dataJson1),safe=False)
            
        else:


            return HttpResponse(-1)



    if request.method == 'POST':
        form=request.POST.get('form')
        #print(form)
        form=json.loads(form)
        name=form['name']
        address=form['address']
       
        #print(name)
       
        # if address=="":
        #     address=None
    
        new=Publisher.create(name,address)
        new.save()
        

        data={"pk":str(new.pk),"name":new.name}

        dataJson=json.dumps(data)

        #print("view!!!")
        #print(data)
        return JsonResponse(dataJson,safe=False)


class BookInsertView(View):
    def get(self, request, *args, **kwargs):



        return render(request, 'library/inserir.html')
    def post(self, request, *args, **kwargs):
        authors=[]
        author=None
        typeFilter=None
        category=None

        categories=Category.objects.filter(depth=0)
        #print("from POST Insert book")
        #print(request.POST)
        form=request    
        
        
        title= request.POST.get('title', None) 
        authorsPk= request.POST.getlist('authors', [1]) 
        publisherPk= request.POST.get('publisher') 
        year= request.POST.get('year') 
        categoryPk= request.POST.get('category', None) 

        identifier=request.POST.get('identifier') 

        type=request.POST.get('inputType') 

        #print(year)
        #get publisher

        if not publisherPk:
            publisherPk=1




        publisher=Publisher.objects.get(id=publisherPk)

        #get authors
        authors=Author.objects.filter(id__in=authorsPk)
        #print(authors)
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

        if type=="I":
            typeFilter=Type.objects.get(pk=1)
        elif type=="F":
            typeFilter=Type.objects.get(pk=2)


        newItem=Item(content_object=new, identifier=identifier,type=typeFilter )
        
        newItem.save()
        new.authors.set(authors)
        #print(new.authors)

        messages.success(request,f'Livro '+newItem.__str__()+' Inserido com exito')
        return redirect('camoes-home')
        
        



            


def notFound(request):
    return render(request,'library/notFound.html')
def about(request):
    return HttpResponse('<h1>about</h1>')



class  BookListView(ListView):
    model=Book
    template_name='library/index.html'
    context_object_name='books'
    
    paginate_by=1

    queryset=Book.objects.all()

    includeAuthors=[]
    includePublishers=[]

    search=None

    filtersAuthor=[]
    selectedAuthors=[]

    filtersPublishers=[]
    selectedPublishers=[]

    querysetAll=queryset

    def dispatch(self, request, *args, **kwargs) :
        self.includeAuthors=[]
        self.includePublishers=[]

        #print("hello from dispatch")
        self.filtersAuthor=self.request.GET.getlist('checkAuthor')

        self.search=self.request.GET.get('search')
        
        self.selectedAuthors=Author.objects.filter(pk__in=self.filtersAuthor)

        self.filtersPublisher=self.request.GET.getlist('checkEditora')
        self.selectedPublishers=Publisher.objects.filter(pk__in=self.filtersPublisher)




        if self.filtersAuthor and not self.filtersPublisher:
            self.request.session['firstSelectedIndex']='A'
            
        elif not self.filtersAuthor and self.filtersPublisher:
            self.request.session['firstSelectedIndex']='P'

        # else:
        #     if self.request.session.get('firstSelectedIndex'):
        #         del self.request.session['firstSelectedIndex']
            


        if self.search:
            self.queryset=self.queryset.filter(Q(title__icontains=self.search))
            self.querysetAll=self.queryset

        #print(self.request.session.get('firstSelectedIndex'))    
        


        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self): # new


        # if self.search:
        #     self.queryset=Book.objects.filter(Q(title__icontains=self.search))


        if self.filtersAuthor or self.filtersPublisher :

            if self.filtersAuthor:
                self.queryset=self.queryset.filter(authors__pk__in=self.filtersAuthor)
            elif self.filtersPublisher:
                self.queryset=self.queryset.filter(publisher__pk__in=self.filtersPublisher)

            

            # self.exclude=Book.objects.filter(pk__in=self.queryset)

           
        # else:

        #     self.queryset=Book.objects.all()


        

        if self.request.session.get('firstSelectedIndex')=="A":
            for object in self.querysetAll:
        
                for author in object.authors.all():
                    #print(author)
                    tempObject=copy.deepcopy(author.pk)
                    self.includeAuthors.append(tempObject)
            for object in self.queryset:
                self.includePublishers.append(object.publisher.pk)


        elif self.request.session.get('firstSelectedIndex')=="P":
            for object in self.querysetAll:
            
            
                self.includePublishers.append(object.publisher.pk)
            for object in self.queryset:
            
                for author in object.authors.all():
                    #print(author)
                    tempObject=copy.deepcopy(author.pk)
                    self.includeAuthors.append(tempObject)
        
        else:
            

            for object in self.queryset:
                
                
                self.includePublishers.append(object.publisher.pk)
                for author in object.authors.all():
                    #print(author)
                    tempObject=copy.deepcopy(author.pk)
                    self.includeAuthors.append(tempObject)
        #print("--------------------------------------------------------")
        #print(self.includeAuthors)
        #print(self.queryset)
        #print("--------------------------------------------------------")

        return self.queryset
    def get_context_data(self, **kwargs):
        #print("hello from get_contect data")
        context = super(BookListView, self).get_context_data(**kwargs)

        #authors filtering logic

        seeAuthors=self.request.GET.get('seeAuthors')
        if seeAuthors:
            nShowAuthors=int(seeAuthors)
        else:
            nShowAuthors=5

       

        #authors=Author.objects.filter(authors__pk__in=self.queryset).exclude(pk__in=self.selectedAuthors)[:nShowAuthors]
        #print("authors!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        
        
        print("-----------------------")      
        print(nShowAuthors)

        if self.includeAuthors:

            authors=Author.objects.filter(pk__in=self.includeAuthors).exclude(pk__in=self.selectedAuthors)[:nShowAuthors]


        #print(nShowAuthors)


        context.update({'authors':authors,'nShowAuthors':nShowAuthors,'selectedAuthors':self.selectedAuthors})

        #publisher filtering logic

        seePublishers=self.request.GET.get('seePublishers')
        if seePublishers:
            nShowPublishers=int(seePublishers)
        else:
            nShowPublishers=5


        if self.includePublishers:
            publishers=Publisher.objects.filter(pk__in=self.includePublishers).exclude(pk__in=self.selectedPublishers)[:nShowPublishers]
        else:
            publishers=Publisher.objects.all().exclude(pk__in=self.selectedPublishers)[:nShowPublishers]

        context.update({'publishers':publishers,'nShowPublishers':nShowPublishers, 'selectedPublishers':self.selectedPublishers, 'search':self.search  })

        return context




class BookListView1(ListView):
    
    model=Book
    template_name='library/index.html'
    context_object_name='books'
    
    paginate_by=5

    queryset=None
    search=None
    selectAuthors=None

    selectPublishers=None

    selectCategories=None
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
                ##print(self.selectAuthors)
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
                #print("----------------------------book")
                #print(books)

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
        #print("editora-------------------")
        #print(self.selectPublishers)
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
            
            # #print(querysetAuthor)
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
        #print(querysetAuthor)

        context.update({'authors':querysetAuthor,'seeAuthors':showAuthors})
        return context