let map = L.map('map', {
    center: [21.2022347759, 92.3855338861],
    zoom: 12
});


let osm =           //adding osm background map
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            label: 'Street Map',
            maxZoom: 18,
            attribution: 'Map data &copy; OpenStreetMap contributors'
        }).addTo(map);


/**var varl  = 'http://gis-bigdata.uni-muenster.de:13014/layer/S2A_MSIL1C_20161212T082332_N0204_R121_T34KGD_20161212T084403.SAFE/T34KGD_20161212T082332_B01/{z}/{x}/{y}.png'

 var lyr = L.tileLayer(varl, {tms: true, opacity: 0.7, attribution: ""});
 console.log(lyr);**/

//basemap and layer toggle
let baseMaps = {
    'Street Map': osm
};

let overlaymaps = {
};

L.control.layers(baseMaps, overlaymaps).addTo(map);


let sidebar = L.control.sidebar('sidebar').addTo(map);
sidebar.open('home');

// FeatureGroup is to store editable layers
let loadLayer = (layer, method) => {
    debugger;
    let pathBefore = 'T46QDJ_20171215T042151_TCI_20m'; //+ pathname before

    let layerBefore = L.tileLayer(pathBefore + '/{z}/{x}/{y}.png',
        {
            tms: true, opacity: 0.85,
            attribution: 'Layer before change'
        }).addTo(map);
    overlaymaps = {
        "Layer before Incident": layerBefore
    };

    if (method === 'nbr') {
        //add nbr Layer here
    } else if (method === 'change') {
        //add change layer here
    } else if(method=== 'slider') {
        let pathAfter = layer; //+ pathname after
        let layerAfter = L.tileLayer(pathAfter + '/{z}/{x}/{y}.png',
            {
                attribution: 'Layer after change',
                tms: true
            }).addTo(map);

        //L.control.sideBySide(layerBefore, layerAfter).addTo(map);
    } else{
        alert("No Change Detection Layer will be displayed")
    };




};

