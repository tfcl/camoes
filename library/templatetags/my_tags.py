
# templatetags/my_tags.py
import logging
from urllib.parse import urlencode
from django import template
from datetime import datetime
from datetime import timedelta  


register = template.Library()

@register.simple_tag
def requisition_info(date1, date2):
    print("My tag!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    message=None
    #test
    deadlineTest= date2 + timedelta(days=-15) 
    
    
    sub= date1-date2
    print(sub)

    if sub==timedelta(days=1):

        message="A requisição expira amanhã"
    elif sub==timedelta(days=-1):
        message="A requisição expirou ontem"

    elif sub>timedelta(days=0) :

        message="A requisição expira em "+str(sub.days)+" dias"
    elif sub<timedelta(days=0):
        message="A requisição expirou à "+str(sub.days*-1)+" dias"

    elif sub==timedelta(days=0):
        message="A requisição expira hoje"
    
    return message





































@register.simple_tag(takes_context=True)
def add5(context, **kwargs):
    seeAuthors=5
    if 'seeAuthors' in context:
        print(context['seeAuthors'])
        seeAuthors=int(context['seeAuthors'])+5
    return seeAuthors



@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):

    query = context['request'].GET.copy()
    
    
    #logging.debug(context)
    
    #query.update(kwargs)

    #del query['page']
    query.pop('page', None)
    
    logging.debug(query)

    return query.urlencode()
@register.simple_tag(takes_context=True)
def get_pubs(context, **kwargs):
    for book in context['books']:
    
        pub=[]
        pub.append(book.publisher)

        return pub


@register.simple_tag(takes_context=True)
def get_search(context, **kwargs):
    #query = self.request.POST.get('q', False);
    query = context['request'].GET.copy()
    query=query.get('q',False) 
    

    if query != False:
        
        logging.debug(query)
        
        return query
    else:
        return False
def get_search_url(context, **kwargs):
    #query = self.request.POST.get('q', False);
    query = context['request'].GET.copy()
    query=query.get('q',False) 
    
    logging.debug(query)

    if query != False:
        
        logging.debug(query)
        
        return query
    else:
        logging.debug(query)
        return False