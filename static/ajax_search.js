$(document).ready(function(){  
 
$("button#search_button").on("click", function(){
      var search_term=$("input#search_query").val().toLowerCase();
      $.ajax({
        type: "GET",
        url: "/search",
        data: {"search_query" : search_term },
        success: function(response){
          $("div#searched_query_content").empty();

          $.each(response.result, function(index, template){
            var htmlcard='<div class="m-2 template-card-search border border-secondary rounded flex-wrap"> \
              <img class="template-card-search-image mx-auto" src="' +  template.onClickURL + '"alt="Card image"/> \
              <div class="card-body"> \
                <h4 class="card-title">' + template.dialogue + '</h4> \
                <div class="card-text"> <label class="font-weight-bold" for="movie_template_name">' + "Movie/Template Name:" + '</label> ' + template.movie_name + '</div> \
                <div class="card-text"> <label class="font-weight-bold" for="tags">' + "Tags:" + '</label> ' + template.tags + '</div> \
              </div> \
            </div>';
            
            $("div#searched_query_content").append(htmlcard);
          });
        }
      });
    });

    var search_suggestions = []

    function load_suggestions(){
      $.getJSON('/search-suggestions', function(query_suggestions,status,xhr){
        query_suggestions=query_suggestions["result"];
        for (var i=0;i<query_suggestions.length;i++){
            search_suggestions.push(query_suggestions[i]);
        }
      });
    };
    
    load_suggestions();
  
    $("input#search_query").autocomplete({
      source: search_suggestions,
      minLength:3
    });
  });