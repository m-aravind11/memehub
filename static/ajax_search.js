$(document).ready(function(){
    $("button#search_button").on("click", function(){
      var search_term=$("input#search_query").val().toLowerCase();
      $.ajax({
        type: "GET",
        url: "/search",
        data: {"search_query" : search_term },
        success: function(response){
          $("div#searched_query_content").empty();
          $("div#searched_query_content").text=response.result;

          $.each(response.result, function(index, template){
            console.log(template.template_filename);
            $("div#searched_query_content").append(' <a href=' + template.onClickURL + '> <img class="p-3" src=uploads/'+ template.template_filename +' width=360px height=270px/> </a> </div>');
          });
        }
      });
  });
});