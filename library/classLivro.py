import requests 
from bs4 import BeautifulSoup
import csv
from urllib.request import urlopen
import re
import urllib.parse

import unicodedata
import sys

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

DEFAULT_TIMEOUT = 5 # seconds

class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)

retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)
def formatAuthor(author):

    if not bool(re.search(r'\d', author)):
        return author
    numberStart=0
    for i, letter in enumerate(author):
        if letter.isnumeric():
            
            numberStart=i
            break
        
    
    return author[:numberStart-1]+", "+author[numberStart:]
def decomposeUrl(url):
    
    url=urllib.parse.unquote(url)
    if url.find("find?")!=-1:
        url=url.split("find?",1)
        return url[1]
  
    else:
        return "|Url_Error|"
    
def getAuthors(urls):
    author=""
    urlsLen=len(urls)
    
    print(urlsLen)
    
    
    for index, url in enumerate(urls, start=1):
        url=decomposeUrl(url)
        
        
        page=http.get("http://www.worldcat.org/identities/find?"+url).text

    
        soup=BeautifulSoup(page,'xml')
        if soup.establishedForm:
            if index!=urlsLen:
                
                author+=formatAuthor(soup.establishedForm.text)+" | "
                
            else:
                author+=formatAuthor(soup.establishedForm.text)
        else:
            author+="|Error_Author| "

            
    return author
def splitYear(str):
    
    year=re.findall(r'\b\d{4}\b',str)
    print(str)
    str=str.replace(year[0],"")
    print(str)
    year.append(str)
    year.reverse()
    return year
def concatTitle(title,subtitule):
    return title+" : "+subtitule
def decomposeTitle(title):
    title=title.replace(":","")
    title=re.sub(' +', ' ', title)
    title=title.replace(" ","-")
    return title

def splitPublisher(publisher):	
    print(publisher)
    final=[]
    if publisher.find(",")==-1 and publisher.find(".")==-1:
        return splitYear(publisher)
    if publisher.find(",")==-1:
        results=publisher.rsplit('.',1)   
    else:
        results=publisher.rsplit(',',1)
    year=results[1]

    if results[0].find(":")==-1:        
        publisher=results[0]
            
    else:
        final=results[0].split(':',1) 
        publisher=final[1]
    final.clear()
    final.append(publisher)
    final.append(year)


    for index, result in enumerate(final):
        final[index]=result.strip()
            
    return final 
    
def webScraping(isbn):
    
    authorsList=[]
    
    
    page=http.get("https://www.worldcat.org/oclc/"+isbn+"&referer=brief_results").text
    soup = BeautifulSoup(page,'html.parser')
    

   
    
    if soup.find(id='authorSearchSelect'):

        values=soup.find(id='authorSearchSelect')
        
        for optionTag in values.find_all('option'):
            
            authorsList.append(optionTag.attrs.get("value"))
    
        authorsList=getAuthors(authorsList)
    else:
        if soup.find(id="bib-author-cell"):
            
            authorsList=(soup.find(id="bib-author-cell").text)
        else:
            authorsList=""
    publisherAndYear=splitPublisher(soup.find(id='bib-publisher-cell').text)
    
    if soup.find(id="bib-hotSeriesTitles-cell"):
        colection=soup.find(id="bib-hotSeriesTitles-cell").text
        colection=colection.replace("\n","")
        
    else:
        colection=""
    
    livro={
        "Autor":authorsList,
        "Editora":publisherAndYear[0],	
        "Ano":publisherAndYear[1],
        "Colecção":colection
    }
    return livro
def split(year):
    if not year.isnumeric():
        list=[char for char in year]
        
        for index, item in enumerate(list):
            if item.isnumeric():
                year=""
                indexOfFirstNumber=index
                i=0
                while i < 4:
                    year=year+list[indexOfFirstNumber]
                    indexOfFirstNumber+=1
                    i+=1
                return year   

    else:
        return year
def strip_accents(text):

    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass

    text = unicodedata.normalize('NFD', text)\
        .encode('ascii', 'ignore')\
        .decode("utf-8")

    return str(text)
def splitTitle(title):
    if title.find(':'):
        results=title.split(':')

        for index, result in enumerate(results):
            results[index]=result.strip()
            print(results[index])
    else :
        results=[title,""]	
    return results
def formatCdu(cdu):
    cdu=cdu.replace("BN por","")
    return cdu


def formatTitleColection(str):
    str=str.replace("<","")
    str=str.replace(">","")

    return str

def validateIsbn(isbn):  
    sum=0
    #Retirar os Hifens se introduzidos
    isbn=isbn.replace("-","")
    #Comprimento do ISBN
    lengh=len(isbn)
    #Se ISBN não tiver comprimento nem de 11 nem 13 então não é um ISBN válido
    if lengh!=10 and lengh!=13:
        return False
    #Se ISBN estiver no formato ISBN13
    if lengh==13:
        #Se ISBN nao for numero então não é um ISBN válido 
        if not isbn.isnumeric():
            return False
        #O multiplicador começa a 1 e alterna para 3 e assim sucessivamente, ou seja 
        #Multiplicar posições impares por 1 e pares por 3
        multiplier=1
        for i in range(12):
            #Somador da multiplicação da posição do digito com o multiplicador 
            sum+=int(isbn[i])*multiplier
            #Alternar de 1 para 3 ou de 3 para 1
            if multiplier==1:
                multiplier=3
            elif multiplier==3:
                multiplier=1
        #Resto da divisão do somador por 10
        sum=sum%10
        #Se o Resto for diferente de 0 então subtrair 10 ao Resto
        if sum!=0:
            sum=10-sum
        #Se Resto -10 ou Resto 0 for igual ao digito de controlo(ultimo digito) então é um ISBN válido
        #Senão o ISBN não está no formato válido
        if sum == int(isbn[12]):
            return True 
        else:
            return False
    #Se ISBN estiver no formato ISBN10
    if lengh==10:
        #Se os primeiros 9 Caracteres não forem numeros e o ultimo digito não é nem X nem Numero
        #Então iSBN não é válido
        if not isbn[0:9].isnumeric() and (isbn[9].capitalize()!="X" or not isbn[9].isnumeric()):
            return False
        #O multiplicador começa a 10 e decrementa-se uma unidade a cada itereção
        multiplier=10
        for i in range(9):
            #Somador da multiplicação da posição do digito com o multiplicador
            sum+=int(isbn[i])*multiplier
            #decrementar multiplicador
            multiplier-=1
        #Se a ultima posição for X somar 10 ao somador(X corresponde 10 e só o ultimo digito pode tomar este valor, 
        #   está capitalizado para não ter que comparar com x minusculo)
        #Senão somar ultimo digito
        if isbn[9].capitalize()=="X":
            sum+=10
        else:
            sum+=int(isbn[9])
        #Resto da divisão do somador por 11
        sum=sum%11
        #Se resto for igual a 0 então ISBN é válido senão não é 
        if sum==0:
            return True
        else:
            return False

def divideAuthors(str):
    tempAuthorFinal={}
    authorsBrute=[]
    years=[]
    authorsFinal=[]
    authorFinal={
        'lastName':"",
        'firstName':"",
        'deathDate':None,
        'birthDate':None
    }
    authorBrute=[]
    if '|' in str:
        authorsBrute=str.split('|')
    else:
        authorsBrute.append(str)
    for author in authorsBrute:
        print(author)
        counter=author.count(',')
        authorBrute=author.split(',')
        authorFinal['lastName']=authorBrute[0]
        authorFinal['firstName']=authorBrute[1]
        if counter>1:
            if '-' in authorBrute[2]:

                years=authorBrute[2].split('-')

                authorFinal['birthDate']=years[0]
                
                authorFinal['deathDate']=years[1]
            else:
                authorFinal['birthDate']=authorBrute[2]
        print(authorsFinal)
        tempAuthorFinal=authorFinal.copy()
        authorsFinal.append(tempAuthorFinal)
        
    return authorsFinal



class livro():
    
    
    
    
    book={
        "Nº Inventário":"",
        "Titulo":"",
        "Autor":"",
        "Editora":"",
        "Ano":"",
        "Etiqueta":"",
        "ISBN":"",
        "Colecção":"",
        "Status":""
        }
    

    def error(self):
        self.book["Titulo"]=""
        
        self.book["Autor"]=""
        self.book["Editora"]=""
        self.book["Ano"]=""
        self.book["Etiqueta"]=""
        self.book["ISBN"]=""
        self.book["Colecção"]=""
        self.book["Status"]="Error"

    def NotFound(self):
        self.book["Titulo"]=""
        
        self.book["Autor"]=""
        self.book["Editora"]=""
        self.book["Ano"]=""
        self.book["Etiqueta"]=""
        self.book["ISBN"]=""
        self.book["Colecção"]=""
        self.book["Status"]="Nao encontrado"
    def getBook(self):
        
        
        
        return self.book
    def createBook(self, title="", author="", publisher="", year="", classification="", isbn="", colection=""):
        
        self.book["Titulo"]=title
        
        self.book["Autor"]=author
        self.book["Editora"]=publisher
        self.book["Ano"]=year
        self.book["Etiqueta"]=classification
        self.book["ISBN"]=isbn
        self.book["Colecção"]=colection
        self.book["Status"]="Manualmente"

        
    def getBookByIsbn(self, isbn=""):
        
        if isbn:
            if self.search_bnp(isbn) == -1:
                
                if self.search_oclc(isbn)==-1:
                    return -1
        else:
            return -1     
        


    
    def search_bnp(self, isbn):
       
        payload = {'id':isbn}
        
        r= http.get(' http://urn.bn.pt/isbn/mods/xml', params=payload).text
        soup= BeautifulSoup(r,'lxml')
        
        error_message=soup.find('error')
        if error_message:
            
            return -1		
        if soup.title :
            title=soup.title.text
        else :
            title=''
        if soup.subtitle:
            
            
            subtitle=soup.subtitle.text	
            title=concatTitle(title,subtitle)
        

        if soup.namepart:
            author=""
            names=soup.find_all("namepart")
            namesLen=len(names)
            for index, name in enumerate(names, start=1):
                if index!=namesLen:
                    author+=name.text+" | "
                else :
                    author+=name.text
        else:
            author=''
                        
        if soup.publisher :
            publisher=soup.publisher.text
        else:
            publisher=''

        if soup.dateissued :	
            year=split(soup.dateissued.text)
        else:
            year=''
        if soup.classification :
            classification=soup.classification.classification.text 
        else :
            classification=''
        if soup.identifier:

            isbn=soup.identifier.text
        else :
            isbn=''
        if soup.relateditem:
            colection=soup.relateditem.relateditem.text
        
        else:
            colection=""
        
        self.book["Titulo"]=formatTitleColection(title)
        
        self.book["Autor"]=divideAuthors(formatTitleColection(author))
        self.book["Editora"]=publisher
        self.book["Ano"]=year
        self.book["Etiqueta"]=formatCdu(classification)
        self.book["ISBN"]=isbn
        self.book["Colecção"]=formatTitleColection(colection)
        self.book["Status"]="BNP"


        
        
    def search_oclc(self, isbn, loop=0,title=""):
       
        owi=""
        wi=""
        titleLoop=""
        
        if not loop==3:
            payload = {'stdnbr':isbn, 'summary': 'true'}
        else: 
            payload = {'title':title, 'summary': 'true'}
        r= http.get(' http://classify.oclc.org/classify2/Classify', params=payload).text
        soup= BeautifulSoup(r,'xml')
     
        if soup.response.attrs == {'code':'101'} or soup.response.attrs == {'code':'102'} or soup.response.attrs == {'code':'100'} :
            
            
            return -1
        
        if soup.response.attrs == {'code':'0'}:
            
            author = soup.work.attrs.get("author")
            cod=soup.work.text

            
            if bool(soup.ddc):
                ddc= soup.ddc.mostPopular.attrs.get('nsfa')
            elif bool(soup.lcc):
                ddc=soup.lcc.mostPopular.attrs.get('nsfa')
            else:
                ddc=""
            
            titleBook= soup.work.attrs.get('title')
            
            
            publisherYearAuthors=webScraping(cod)
            print(publisherYearAuthors)
            self.book["Titulo"]=titleBook
            self.book["Autor"]=divideAuthors(publisherYearAuthors["Autor"])
            self.book["Editora"]=publisherYearAuthors["Editora"]
            self.book["Ano"]=split(publisherYearAuthors["Ano"])
            self.book["Etiqueta"]=ddc
            self.book["Colecção"]=publisherYearAuthors["Colecção"]
            
            self.book["Status"]="OCLC"

            

        if soup.response.attrs == {'code':'4'}:
            
            
            teste=soup.findAll("work")
         
            
            indexWanted=""
            for index, item in enumerate(teste , start=1):
                
                
                if "DDC" in item.attrs.get("schemes") and not bool(indexWanted) and title==item.attrs.get("title"):
                    indexWanted=index
                    
            if bool(indexWanted):
                if loop==0:
                    titleLoop=teste[indexWanted-1].attrs.get("title")
                    owi=teste[indexWanted-1].attrs.get("owi")
                elif loop==1:
                    titleLoop=teste[indexWanted-1].attrs.get("title")
                    owi=teste[indexWanted-1].attrs.get("wi")
                elif loop==2:
                    titleLoop=teste[indexWanted-1].attrs.get("title")
                
            else :
                if loop==0:
                    owi=teste[0].attrs.get("owi")
                elif loop==1:
                    owi=teste[0].attrs.get("wi")
                elif loop==2:
                    titleLoop=teste[0].attrs.get("title")
                
            return self.search_oclc(owi,loop+1,titleLoop)
        

