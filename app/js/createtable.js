var searchdata;

function tableButton(res) {


    $('#example').DataTable({ //Initializing DataTable (framework)
        searching: false,
        scrollX: true,      // enable List scorolling to fit the sidebar
        data: res,          // searching through given data (res) by column and strings
        destroy: true,      // delete initialized table to enable reinitialization for a new search query
        columns: [
            {data: 'date'},
            {data: 'name'},
            {data: 'location'}
        ],
        "order": [[1, "desc"]]      // Ordering by date
    });
    addPreview(res);        //Adding the footprint of all search results to the map


    $('#example').on('click', 'tr', function () {
        var table = $('#example').DataTable();
        var datastring = this.children[1].innerText;
        if ( $(this).hasClass('selected') ) {   //Selection highlighting of one dataset in the table
            $(this).removeClass('selected');
        }
        else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }

        var pathbase = '/home/s_lech05/JamaSato/IMG/' + datastring;
        $('#dir')[0].value = pathbase;
    });
}


function layertomap(res) {
    var layerpath = res;

    var varl  = 'http://gis-bigdata.uni-muenster.de:13014' +layerpath+ '/{z}/{x}/{y}.png'
    var lyr = L.tileLayer(varl, {tms: true, opacity: 0.7, attribution: ""});

    if (overlaymaps === {}){
      overlaymaps.push(lyr);
    }
     overlaymaps.pop();
     overlaymaps.push(lyr);

}

function createGrayscale(){
  var bandId = document.getElementById('gray');
  var pathBase = $('#dir')[0].value;
  //adding grayscale Image here
}
