var map = L.map('map');

map.setView([51.2, 7], 9);


var whiteAndBlack =     //adding black and white background map
        L.tileLayer('//{s}.tile.stamen.com/toner-lite/{z}/{x}/{y}.png', {
            attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
            subdomains: 'abcd',
            maxZoom: 20,
            minZoom: 0,
            label: 'White and Black'  // optional label used for tooltip
        }),
    osm =           //adding osm background map
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            label: 'Street Map',
            maxZoom: 18,
            attribution: 'Map data &copy; OpenStreetMap contributors'
        }).addTo(map);


/**var varl  = 'http://gis-bigdata.uni-muenster.de:13014/layer/S2A_MSIL1C_20161212T082332_N0204_R121_T34KGD_20161212T084403.SAFE/T34KGD_20161212T082332_B01/{z}/{x}/{y}.png'

 var lyr = L.tileLayer(varl, {tms: true, opacity: 0.7, attribution: ""});
 console.log(lyr);**/

//basemap and layer toggle
var baseMaps = {
    'Street Map': osm,
    'White and Black': whiteAndBlack
};

var overlaymaps = {
    //"Layer": lyr
}

L.control.layers(baseMaps, overlaymaps).addTo(map);


var sidebar = L.control.sidebar('sidebar').addTo(map);
sidebar.open('home');

// FeatureGroup is to store editable layers

let loadLayer = (layer, method) => {
    let pathBefore = layer; //+ pathname before

    let layerBefore = L.tileLayer(pathBefore + '/{z}/{x}/{y}.png',
        {
            attribution: 'Layer before change',
            tms: true
        }).addTo(map);

    if (method === nbr) {
        //add nbr Layer here
    } else if (method === change) {
        //add change layer here
    } else {
        alert("No Change Detection Layer will be displayed")
    }


    let pathAfter = layer; //+ pathname after

    let layerAfter = L.tileLayer(pathAfter + '/{z}/{x}/{y}.png',
        {
            attribution: 'Layer after change',
            tms: true
        }).addTo(map);

    L.control.sideBySide(layerBefore, layerAfter).addTo(map);
};

