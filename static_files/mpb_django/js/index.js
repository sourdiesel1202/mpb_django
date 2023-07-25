$(window).on('load', function () {

//    $("body").addClass("loading");
var url = '/get_mpb_django_health/'
//    var toolId= document.getElementById("tool_id").value;
//    $("#mpb_django_health_message").hide()
    build_tabulator_table(url,"mpb_django_health_table")

     //insert all your ajax callback code here.
//     //Which will run only after page is fully loaded in background.
//     if ($("#mpb_django_health_table tr").length === 0){
//        console.log("no health violators")
////        $("#mpb_django_health_message").text("No health violators")
////        $("#mpb_django_health_table").hide()
////        $("#download_csv_mpb_django_health_table").hide()
////        $("#mpb_django_health_message").show()
//
//    }else{
////    $("#mpb_django_health_message").show()
//    }




});