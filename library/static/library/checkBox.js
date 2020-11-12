

function authorsCheck(){
    var form=document.getElementById('filterAuthors');
    var form1=document.getElementById('filter');
    form.submit();
 


}
function myFunction(){
    var checkbox=document.getElementsByClassName('checkbox');
    var checkAuthors=document.getElementsByName('checkAuthors');
    var checkPublisher=document.getElementsByName('checkEditora');
     
    var text;
    var count=0;
    var form=document.getElementById('filter');
    
    
    
    var checked=getUrlVars();
    

    for (i=0 ; i<checkPublisher.length;i++ ){
       if(checkPublisher[i]==checked['checkEditora']){
            checkPublisher[i].checked=true;
       }
        
        if(checkPublisher[i].checked==true){
            count++;
            text += checkPublisher[i].value;
        }
    }

    
    
    form.submit();
}

function insertMore(){
    var input = document.createElement("input");

    input.setAttribute("type", "hidden");

    input.setAttribute("name", "insertMore");

    input.setAttribute("value", "True");

    //append to form element that you want .
    document.getElementById('form-author').appendChild(input);
    document.getElementById('form-author').submit();

}
function deleteBook(){

    
}

function filterRequisitions(){
    var checkboxs = document.getElementsByClassName('checkbox');
    var form=document.getElementById('filter');

    form.submit();


}
function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}


document.addEventListener("DOMContentLoaded", function() {
    var start;
    var end;
    
    var paramsFilter=[];
    var checkboxs=document.getElementsByClassName('checkbox');
    var checked=getUrlVars();
    url_string=window.location.search;
    console.log(url_string);
    while(url_string.search("filter=")!=-1){
        start=url_string.indexOf("filter");
        if(url_string.search("&")==-1){
            
            end=url_string.length;
        }
        else{
            end=url_string.indexOf("&");
        }
        paramsFilter.push(url_string.slice(start+7,end));
        url_string=url_string.slice(end+1);
        console.log(paramsFilter);
    }

    for (i=0 ; i<checkboxs.length;i++ ){
        for(j=0;j<paramsFilter.length;j++){
            if(checkboxs[i].value==paramsFilter[j]){
                checkboxs[i].checked=true;
           }    
        }
    }


});

function clearCheckboxs() {
    var checkboxs=document.getElementsByClassName('checkbox');
    var form=document.getElementById('filter');

    for (i=0 ; i<checkboxs.length;i++ ){
        checkboxs[i].checked=false;
        
    
    }
    form.submit();

}
document.addEventListener("DOMContentLoaded", function() {
    var button=document.getElementById('requisitionButton');
    var nav=document.getElementById('mainNavbar');
    var warning=document.getElementById('warning');
    var start= nav.offsetTop+ nav.offsetHeight;
    var left=button.offsetLeft+button.offsetWidth-15;
    var top=(button.offsetTop-start)-18;
    // console.log(left)
    // console.log(top)
    warning.style.marginTop=top.toString()+"px"
    // console.log(top.toString()+"px")
    warning.style.marginLeft=left.toString()+"px"



});

document.addEventListener("DOMContentLoaded", function() {
    var checkbox=document.getElementsByClassName('checkbox');
    var checkAuthors=document.getElementsByName('checkAuthor');
    var checkPublisher=document.getElementsByName('checkEditora');
    var checkYear=document.getElementsByName('checkYear');

    var checked=getUrlVars();
    var edit=window.location.href;
    var url_string =window.location.search;
    //console.log(url_string);
    flag=true;
    var params=[];
    var paramsAuthor=[];
    var paramsYear=[];
    while(url_string.search("checkAuthor=")!=-1){
        var start=url_string.indexOf("checkAuthor");
        var end
        if(url_string.search("&")==-1){
            
            end=url_string.length;
        }
        else{
            end=url_string.indexOf("&");
        }
        
        
        temp=url_string;
        tempparamsAuthor=temp.slice(start+12,end)
        if(tempparamsAuthor.search("[\\[\\]?*+|{}\\\\()@.\n\r]")!=-1){
            tempparamsAuthor=tempparamsAuthor.replaceAll("+"," ")
            paramsAuthor.push(tempparamsAuthor);
            
            

        }
        else{
            paramsAuthor.push(tempparamsAuthor);
        }
        paramsAuthor.push(temp.slice(start+12,end));
        url_string=url_string.slice(end+1);
        console.debug(paramsAuthor)
    

    }
    
    
    while(url_string.search("checkEditora=")!=-1){

            var start=url_string.indexOf("checkEditora=");
            
            var end
            if(url_string.search("&")==-1){
                
                end=url_string.length;
            }
            else{
                end=url_string.indexOf("&");
            }
            
            
            temp=url_string;
            tempParams=temp.slice(start+13,end)
            if(tempParams.search("[\\[\\]?*+|{}\\\\()@.\n\r]")!=-1){
                tempParams=tempParams.replaceAll("+"," ")
                params.push(tempParams);
                
                

            }
            else{
                params.push(tempParams);
            }
            params.push(temp.slice(start+13,end));
            url_string=url_string.slice(end+1);

        }
    while(url_string.search("checkYear=")!=-1){

        var start=url_string.indexOf("checkYear=");
        
        var end
        if(url_string.search("&")==-1){
            
            end=url_string.length;
        }
        else{
            end=url_string.indexOf("&");
        }
        
        
        temp=url_string;
        tempparamsYear=temp.slice(start+10,end)
        if(tempparamsYear.search("[\\[\\]?*+|{}\\\\()@.\n\r]")!=-1){
            tempparamsYear=tempparamsYear.replaceAll("+"," ")
            paramsYear.push(tempparamsYear);
            
            

        }
        else{
            paramsYear.push(tempparamsYear);
        }
        paramsYear.push(temp.slice(start+10,end));
        url_string=url_string.slice(end+1);

    }
    
    console.log(paramsYear)
    for (i=0 ; i<checkAuthors.length;i++ ){
        for(j=0;j<paramsAuthor.length;j++){
            if(checkAuthors[i].value==paramsAuthor[j]){
                checkAuthors[i].checked=true;
           }

        }
        



    }
    for (i=0 ; i<checkPublisher.length;i++ ){
        for(j=0;j<params.length;j++){
            if(checkPublisher[i].value==params[j]){
                checkPublisher[i].checked=true;
           }

        }
        



    }
    for (i=0 ; i<checkYear.length;i++ ){
        for(j=0;j<paramsYear.length;j++){
            if(checkYear[i].value==paramsYear[j]){
                checkYear[i].checked=true;
           }

        }
        



    }
  });