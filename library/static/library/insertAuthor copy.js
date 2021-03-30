
//global vars

var flagSearchPublisher=false;
var searchPublisher="";

//verify year format
function verifyYear(year){
//   {% comment %} &&  year.length!=4 && parseInt(year)<1000 && parseInt(year)>3000 {% endcomment %}
  console.log("função ano");
  
  console.log(year);
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
    console.log("load manual")
    $("#publisher-overlay-inside").empty();
    
    
  
    $("#publisher-overlay-inside").append(   '<div class="form-group row">      <label for="" class="pr-0 mr-0 col-sm-3 col-form-label">Nome Completo: </label>      <div class="col-sm-9 ml-0">        <input type="text" id="publisher-input-manual" name="name" class="publisher-form form-control"  placeholder="">                </div>    </div>       <div class="form-group row">      <label for="" id=""class="pr-0 mr-0 col-sm-3 col-form-label">Data de Nascimento: </label>      <div class="col-sm-9 ml-0">        <input type="text" name="birthyear" class="publisher-form form-control"  placeholder="">                </div>    </div>      <div class="form-group row">      <label for="" id=""class="pr-0 mr-0 col-sm-3 col-form-label">Data de Óbito: </label>      <div class="col-sm-9 ml-0">        <input type="text" name="deathyear"class="publisher-form form-control"  placeholder="">                </div>    </div>   <div id="publisher-overlay-buttons"style="display: flex; justify-content: center; margin-top:25px">    <a  class="btn  btn-normal ml-1" id="btn-publisher-manual-confirm" style="width:132px" >Confirmar</a>  </div></div>');
    $("#publisher-input-manual").val(search);
  
  }

//restar div and global vars to initial state 
  function restart(){
    $("#publisher-overlay-inside").empty();
    $("#publisher-overlay-inside").append('<div id="publisher-overlay-inside">\        <div class="form-group row">\          <label for="" id="dropdown-publishers-label"class="pr-0 mr-0 col-sm-3 col-form-label">Pesquisar Autor: </label>\          <div class="col-sm-9 ml-0">\              <div style="display: flex;">\                <input type="text" class="form-control" id="inputPublisher" placeholder="">\                          <div class=""style=" background-color:#b30000; margin: auto; width: 40px; height: 38px; vertical-align: middle;text-align: center;display: table-cell;">\                    <a class="btn-normal" id="btn-publisher-add" ><i style="font-size: 20px;padding-top: 9px;" class="fas fa-search"></i></a>\                  </div>\              </div>\          </div>\        </div>\      <div class="form-group row">        <label for="" id="dropdown-publishers-label"class="ml-0 col-sm-3 col-form-label"></label>\        <div id="dropdown-publishers" class="col-sm-9 ml-0">\        </div>\      </div>\      <div id="publisher-overlay-buttons"style="display: flex; justify-content: center; margin-top:25px">\              </div>\    </div>');
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
    var birthyear=form.eq(1).val();
    var deathyear=form.eq(2).val();
  
    // // {% comment %} console.log("verificação teste");
  
    // console.log(form.eq(1).val());
    // console.log(verifyYear(birthyear));
    // console.log(verifyYear(deathyear)); {% endcomment %}
  
    if(name===""){
       $('#publisher-overlay-inside').prepend('<div class="warning-display form-control m-0" ><p>O campo nome é obrigatório</p></div>');
      
  
    }
    else{
      
  
      if((verifyYear(birthyear)||birthyear==="") && (verifyYear(deathyear)||deathyear==="") ){
        
        if(verifybirthanddeath(birthyear,deathyear)){
          form.each(function(){
            tempName=$(this).attr("name");
            tempValue=$(this).val().replace(/ +(?= )/g,'');
  
            formData[tempName]=tempValue
  
  
          });
          var formPublisherJson=JSON.stringify(formData);
          console.log(formPublisherJson);
          console.log("manual insert");
  
  
  
          ajaxPOSTpublisher(formPublisherJson);
  
  
  
        }
        else{
          $('#publisher-overlay-inside').prepend('<div class="warning-display form-control m-0" ><p>Confira os anos</p></div>');
          
  
        }  
  
  
  
  
      }
      else{
        console.log("verifique os anos");
        $('#publisher-overlay-inside').prepend('<div class="warning-display form-control m-0" ><p>Confira os anos</p></div>');
  
      }
  
  
    }
  
  
  });

$(document).on('click', '.btn-publisher-delete', function(){


    console.log("delete");
    $(this).parent('div').remove();


});
  

$(document).on('click', '#btn-publisher-confirm', function(){
    
    var selected=$('#select-publisher').find(":selected").val();
    var selectedText=$('#select-publisher').find(":selected").text();
    var htmlString='<div style="display: flex;" ><a href="#"class="b-r mr-2 btn-publisher-delete" style="padding-top: 5px;font-size: 20px;"><i class="far fa-trash-alt"></i></a><input type="text" readonly class="d-inline form-control-plaintext"  value='+selectedText+'><input type="hidden" name="publishers" value='+selected+'/></div>';
    
  
    
    $("#form-publishers").append(htmlString);
    restart();




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
    console.log("forçar manual");
    loadPublisherManual();
  
    
  });
  
  
  
  $(document).on('click', "#btn-publisher-cancel", function(){
    restart();
    $("#publisher-overlay").css("display", "none");
  
  
  });
  
  $('#inputPublisher').click(function(e) {
    $("#publisher-overlay").css("display", "block");
    flag=true;
    console.log(flag);
  });
  
  $(document).on('change','.categories-drop', function(e){
    var url = $("#publisherForm").attr("data-categories-url");  // get the url of the `load_cities` view
    console.log("aqui")
    var categoryId = $(this).val();  // get the selected country ID from the HTML input
  
    $.ajax({                       // initialize an AJAX request
      url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
      data: {
      'category': categoryId       // add the country id to the GET parameters
      },
      success: function (data) {   // `data` is the return of the `load_cities` view function
        $("#teste").html(data);  // replace the contents of the city input with the data that came from the server
        $('#id_category').attr("value", $('#var').val());
        console.log($('#id_category').val());
  
        console.log($('.categories-drop'));
      }
    });
  
  });





