dashboard_template = """
    <title>{{report.name}}</title>
    <script type="text/javascript">

    function matchAnyFilter(headerValue,cellValue, rowData, filterParams){
    //headerValue - the value of the header filter element
    //cellValue- the value of the column in this row
    //rowData - the data for the row being filtered
    //filterParams - params object passed to the headerFilterFuncParams property

    var matched = false;
    var values = headerValue.split(","); //break header into list of options
//    console.log(values)
    values.forEach(function(val){
//    console.log(cellValue);
        if(cellValue.toString().toLowerCase().indexOf(val.toString().toLowerCase()) !== -1){
            matched = true;
//            console.log("match found")
        }
    });

    return matched;
}
$(document).ready(function(){
        var tableId='report_table';
        if (document.getElementById(tableId+"_rowcount") == null){
            $("#download_csv_"+tableId).before('<p id="'+tableId+'_rowcount">0 record(s)</p>')
        }
//                console.log(data);
//                if(data['response']=='error'){
//                    Swal.fire('Error', data['message'], 'error');
//                    return
//                }
                //replace_me_with_output
                //var tabledata=
                console.log(tabledata);
//                keys = []
                _columns = []
                for (var key in tabledata[0]){
                    _columns.push({title:key,formatter:"html",field:key,headerFilter:"input",sorter:"string",headerFilterPlaceholder:"enter multiple search queries separated by commas i.e. sma,dmi,adx",headerFilterFunc:matchAnyFilter})
//                    keys.push(key);
//                    console.log(key)

                }

                var table = new Tabulator("#"+tableId, {
                    layout: "fitDataStretch",
                    data: tabledata,
                    columns: _columns,
                    movableRows: true,
                    pagination: "local",
                    movableColumns: true,
                    paginationSize: 10,
                    paginationSizeSelector: [10, 20, 50, 100],
                    dataFiltered: function(filters, rows) {

                          var el = document.getElementById(tableId+"_rowcount");
                          el.innerHTML = rows.length+ " symbol(s) found";
                    },
                    dataLoaded: function(data) {

                          var el = document.getElementById(tableId+"_rowcount");
                          el.innerHTML = data.length+ " symbol(s) found";
                },
                });
                document.getElementById("download_csv_"+tableId).addEventListener("click", function () {
                    table.download("csv", "data.csv");
                });



                $("#"+tableId+"_loading").hide();
//                console.log(typeof data['message'])
//                console.log("Total rows: "+data['message'].length)
//                    if(typeof data['message'] != object){
                //if(data['message'].length <=1 ){

                  //  $("#download_csv_"+tableId).hide();
                //}


        //console.log(url)
});


    </script>

<div class="w3-center">

            <div id="report_div"><h3 class="">{{report.name}}</h3>
            <img src="https://thumbs.gfycat.com/OblongAntiqueAmurratsnake-size_restricted.gif" width="100" height="100"
             id="report_table_loading">
        <div class=" w3-center" id="report_table"></div>
        <div class=" w3-center" id="report_table_rowcount"></div>
        <button class="w3-blue w3-hover-black w3-round" id="download_csv_report_table">download as .csv
        </button>
    </div>
    </div>
"""