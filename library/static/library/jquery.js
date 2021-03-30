<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>

  $(".categories-drop").change(function () {
    var url = $("#bookForm").attr("data-categories-url");  // get the url of the `load_cities` view
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


