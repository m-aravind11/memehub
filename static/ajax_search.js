$(document).ready(function(){  
 
  $("button#search_button").on("click", function(){
        var search_term=$("input#search_query").val().toLowerCase();
        $.ajax({
          type: "GET",
          url: "/search",
          data: {"search_query" : search_term },
          success: function(response){
            $("div#searched_query_content").text=response.result;
  
            $.each(response.result, function(index, template){
              console.log(template.template_filename);
              $("div#searched_query_content").empty();
              $("div#searched_query_content").append(' <a href=' + template.onClickURL + '> <img class="p-3" src='+ template.onClickURL +' width=360px height=270px/> </a> </div>');
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