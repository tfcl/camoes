
//global vars

var flagSearch=false;
var search="";

//verify year format
function verifyYear(year){
//   {% comment %} &&  year.length!=4 && parseInt(year)<1000 && parseInt(year)>3000 {% endcomment %}
  //console.log("função ano");
  
  //console.log(year);
  if((!isNaN(year)  &&  year.length == 4 && parseInt(year)>1000 && parseInt(year)<3000) )  {
    return true;

  }
  else{
    return false;
  }


}
//verify if birthyear is not bigger than the deathdate

function verifybirthanddeath(b,d){

    if(b===""||d===""){
      return true;
  
  
  
    }
  
    else{
  
      b=parseInt(b);
      d=parseInt(d);
      if(b<d){
        return true;
  
      }
      else{
        return false;
      }
  
    }
    
  }
  
  
//load manual insert html
function loadAuthorManual(){
    //console.log("load manual")
    $("#author-overlay-inside").empty();
    
    
  
    $("#author-overlay-inside").append(   '<div class="form-group row">      <label for="" class="pr-0 mr-0 col-sm-3 col-form-label">Nome Completo: </label>      <div class="col-sm-9 ml-0">        <input type="text" id="author-input-manual" name="name" class="author-form form-control"  placeholder="">                </div>    </div>       <div class="form-group row">      <label for="" id=""class="pr-0 mr-0 col-sm-3 col-form-label">Data de Nascimento: </label>      <div class="col-sm-9 ml-0">        <input type="text" name="birthyear" class="author-form form-control"  placeholder="">                </div>    </div>      <div class="form-group row">      <label for="" id=""class="pr-0 mr-0 col-sm-3 col-form-label">Data de Óbito: </label>      <div class="col-sm-9 ml-0">        <input type="text" name="deathyear"class="author-form form-control"  placeholder="">                </div>    </div>   <div id="author-overlay-buttons"style="display: flex; justify-content: center; margin-top:25px">    <a  class="btn  btn-normal ml-1" id="btn-book-manual-confirm" style="width:132px" >Confirmar</a>  </div></div>');
    $("#author-input-manual").val(search);
  
  }

//restar div and global vars to initial state 
  function restart(){
    $("#author-overlay-inside").empty();
    $("#author-overlay-inside").append('<div id="author-overlay-inside">\        <div class="form-group row">\          <label for="" id="dropdown-authors-label"class="pr-0 mr-0 col-sm-3 col-form-label">Pesquisar Autor: </label>\          <div class="col-sm-9 ml-0">\              <div style="display: flex;">\                <input type="text" class="form-control" id="inputAuthor" placeholder="">\                          <div class=""style=" background-color:#b30000; margin: auto; width: 40px; height: 38px; vertical-align: middle;text-align: center;display: table-cell;">\                    <a class="btn-normal" id="btn-book-add" ><i style="font-size: 20px;padding-top: 9px;" class="fas fa-search"></i></a>\                  </div>\              </div>\          </div>\        </div>\      <div class="form-group row">        <label for="" id="dropdown-authors-label"class="ml-0 col-sm-3 col-form-label"></label>\        <div id="dropdown-authors" class="col-sm-9 ml-0">\        </div>\      </div>\      <div id="author-overlay-buttons"style="display: flex; justify-content: center; margin-top:25px">\              </div>\    </div>');
    $("#author-overlay").css("display", "none");
    search="";
    flagSearch=false;
  }

//
$(document).on('click', '#btn-book-manual-confirm', function(){
  
    $("div").remove(".warning-display");
    var form = $(".author-form");
    var formData={};
    var tempName;
    var tempValue;
    var name=form.eq(0).val()
    var birthyear=form.eq(1).val();
    var deathyear=form.eq(2).val();
  
    // // {% comment %} //console.log("verificação teste");
  
    // //console.log(form.eq(1).val());
    // //console.log(verifyYear(birthyear));
    // //console.log(verifyYear(deathyear)); {% endcomment %}
  
    if(name===""){
       $('#author-overlay-inside').prepend('<div class="warning-display form-control m-0" ><p>O campo nome é obrigatório</p></div>');
      
  
    }
    else{
      
  
      if((verifyYear(birthyear)||birthyear==="") && (verifyYear(deathyear)||deathyear==="") ){
        
        if(verifybirthanddeath(birthyear,deathyear)){
          form.each(function(){
            tempName=$(this).attr("name");
            tempValue=$(this).val().replace(/ +(?= )/g,'');
  
            formData[tempName]=tempValue
  
  
          });
          var formAuthorJson=JSON.stringify(formData);
          //console.log(formAuthorJson);
          //console.log("manual insert");
  
  
  
          ajaxPOSTauthor(formAuthorJson);
  
  
  
        }
        else{
          $('#author-overlay-inside').prepend('<div class="warning-display form-control m-0" ><p>Confira os anos</p></div>');
          
  
        }  
  
  
  
  
      }
      else{
        //console.log("verifique os anos");
        $('#author-overlay-inside').prepend('<div class="warning-display form-control m-0" ><p>Confira os anos</p></div>');
  
      }
  
  
    }
  
  
  });

$(document).on('click', '.btn-author-delete', function(){


    //console.log("delete");
    $(this).parent('div').remove();


});
  

$(document).on('click', '#btn-book-confirm', function(){
    
    var selected=$('#select-author').find(":selected").val();
    var selectedText=$('#select-author').find(":selected").text();
    console.log(selected)
    var htmlString='<div style="display: flex;" ><a href="#"class="b-r mr-2 btn-author-delete" style="padding-top: 5px;font-size: 20px;"><i class="far fa-trash-alt"></i></a><input type="text" readonly class="d-inline form-control-plaintext"  value='+selectedText+'><input type="hidden" name="authors" value="'+selected+'"/></div>';
    
  
    
    $("#form-authors").append(htmlString);
    restart();




});

$(document).on('click', "#btn-book-add", function(){

    $("div").remove(".warning-display");
    var name= $("#inputAuthor").val();
    search=name;
  if(name!=""){

    if(flagSearch==false){

      flagSearch=true;

      
      ajaxGETauthor(name);  
     

    }

    else{
          $('#author-overlay-inside').prepend('<div class="warning-display form-control m-0" ><p>Para pesquisar de novo feche esta janela e volte a abrir</p></div>');



    }



  }
  else{
      $('#author-overlay-inside').prepend('<div class="warning-display form-control m-0" ><p>O campo é obrigatório</p></div>');

  }


});

$(document).on('click', "#btn-author-manual", function(){
    //console.log("forçar manual");
    loadAuthorManual();
  
    
  });
  
  
  
  $(document).on('click', "#btn-book-cancel", function(){
    restart();
    $("#author-overlay").css("display", "none");
  
  
  });
  
  $('#inputBook').click(function(e) {
    $("#author-overlay").css("display", "block");
    flag=true;
    //console.log(flag);
  });
  
 


