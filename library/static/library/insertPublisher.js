



//publisher aqui




function clearPublisherInput(){

  $('#hidden-publisher').remove();

}

$(document).on('click', "#btn-publisher-cancel", function(e){

restartPublisher();

$("#publisher-overlay").css("display", "none");


});

//global vars


var flagSearchPublisher=false;
var searchPublisher="";

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
function loadPublisherManual(){
    //console.log("load manual")
    $("#publisher-overlay-inside").empty();
    
    
  
    $("#publisher-overlay-inside").append(   '<div class="form-group row">      <label for="" class="pr-0 mr-0 col-sm-3 col-form-label">Nome: </label>      <div class="col-sm-9 ml-0">        <input type="text" id="publisher-input-manual" name="name" class="publisher-form form-control"  placeholder="">                </div>    </div>       <div class="form-group row">      <label for="" id=""class="pr-0 mr-0 col-sm-3 col-form-label">Endereço: </label>      <div class="col-sm-9 ml-0">        <input type="text" name="address" class="publisher-form form-control"  placeholder="">                </div>    </div>          </div>   <div id="publisher-overlay-buttons"style="display: flex; justify-content: center; margin-top:25px">    <a  class="btn  btn-normal ml-1" id="btn-publisher-manual-confirm" style="width:132px" >Confirmar</a>  </div></div>');
    $("#publisher-input-manual").val(searchPublisher);
  
  }

//restar div and global vars to initial state 
  function restartPublisher(){
    $("#publisher-overlay-inside").empty();
    $("#publisher-overlay-inside").append('<div id="publisher-overlay-inside">\        <div class="form-group row">\          <label for="" id="dropdown-publishers-label"class="pr-0 mr-0 col-sm-3 col-form-label">Pesquisar Editora: </label>\          <div class="col-sm-9 ml-0">\              <div style="display: flex;">\                <input type="text" class="form-control" id="inputPublisher" placeholder="">\                          <div class=""style=" background-color:#b30000; margin: auto; width: 40px; height: 38px; vertical-align: middle;text-align: center;display: table-cell;">\                    <a class="btn-normal" id="btn-publisher-add" ><i style="font-size: 20px;padding-top: 9px;" class="fas fa-search"></i></a>\                  </div>\              </div>\          </div>\        </div>\      <div class="form-group row">        <label for="" id="dropdown-publishers-label"class="ml-0 col-sm-3 col-form-label"></label>\        <div id="dropdown-publishers" class="col-sm-9 ml-0">\        </div>\      </div>\      <div id="publisher-overlay-buttons"style="display: flex; justify-content: center; margin-top:25px">\              </div>\    </div>');
    $("#publisher-overlay").css("display", "none");
    searchPublisher="";
    flagSearchPublisher=false;
  }

//
$(document).on('click', '#btn-publisher-manual-confirm', function(){
  
    $("div").remove(".warning-display");
    var form = $(".publisher-form");
    var formData={};
    var tempName;
    var tempValue;
    var name=form.eq(0).val()
    var address=form.eq(1).val();
    
  
    // // {% comment %} //console.log("verificação teste");
  
    // //console.log(form.eq(1).val());
    // //console.log(verifyYear(birthyear));
    // //console.log(verifyYear(deathyear)); {% endcomment %}
  
    if(name===""){
       $('#publisher-overlay-inside').prepend('<div class="warning-display form-control m-0" ><p>O campo nome é obrigatório</p></div>');
      
  
    }
    else{
      
  
      
        
       
          form.each(function(){
            tempName=$(this).attr("name");
            tempValue=$(this).val().replace(/ +(?= )/g,'');
  
            formData[tempName]=tempValue
  
  
          });
          var formPublisherJson=JSON.stringify(formData);
          //console.log(formPublisherJson);
          //console.log("manual insert");
  
  
  
          ajaxPOSTpublisher(formPublisherJson);
  
          
  
        }
        
  
  
  
  
     
  
  
    
  
  
  });

$(document).on('click', '.btn-publisher-delete', function(){


    //console.log("delete");
    $(this).parent('div').remove();


});
  

$(document).on('click', '#btn-publisher-confirm', function(){
  inputPublisher1
    var selected=$('#select-publisher').find(":selected").val();
    var selectedText=$('#select-publisher').find(":selected").text();
    var htmlString=('<input type="hidden" id="hidden-publisher" name="publisher" value="'+selected+'"/></div>');
    
  
    clearPublisherInput();
    $("#inputPublisher1").val(selectedText);
    $("#form-publishers").append(htmlString);
    restartPublisher();




});

$(document).on('click', "#btn-publisher-add", function(){

    $("div").remove(".warning-display");
    var name= $("#inputPublisher").val();
    searchPublisher=name;
  if(name!=""){

    if(flagSearchPublisher==false){

      flagSearchPublisher=true;

      
      ajaxGETpublisher(name);  
     

    }

    else{
          $('#publisher-overlay-inside').prepend('<div class="warning-display form-control m-0" ><p>Para pesquisar de novo feche esta janela e volte a abrir</p></div>');



    }



  }
  else{
      $('#publisher-overlay-inside').prepend('<div class="warning-display form-control m-0" ><p>O campo é obrigatório</p></div>');

  }


});

$(document).on('click', "#btn-publisher-manual", function(){
    //console.log("forçar manual");
    loadPublisherManual();
  
    
  });
  
  
  
  
  $('#inputPublisher1').click(function(e) {
    $("#publisher-overlay").css("display", "block");
    flag=true;
    //console.log(flag);
  });
