
# templatetags/my_tags.py
import logging
from urllib.parse import urlencode
from django import template

register = template.Library()

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