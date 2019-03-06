let map = L.map('map', {
    center: [38.93793, -9.32756],
    zoom: 12,
    minZoom: 8,
    maxZoom: 13,
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
let layerBefore;
let changeLayer;
let nbrLayer;
let layerAfter;
let loadLayer = (method) => {
    debugger;

    if(map.hasLayer(layerBefore)){
        map.removeLayer(layerBefore)
    }
    if(map.hasLayer(layerAfter)){
        map.removeLayer(layerAfter)
    }
    if(map.hasLayer(nbrLayer)){
        map.removeLayer(nbrLayer)
    }
    if(map.hasLayer(changeLayer)){
        map.removeLayer(changeLayer)
    }
    let pathBefore = '/before/T29SMD_20180826T113309_TCI.tif'; //+ pathname before

    layerBefore = L.tileLayer(pathBefore + '/{z}/{x}/{y}.png',
        {
            tms: true, opacity: 0.85,
            attribution: 'Layer before change'
        }).addTo(map);
    overlaymaps = {
        "Layer before Incident": layerBefore
    };

    if (method === 'nbr') {
        let nbrPath = "/nbr/T29SMD_20180826T113309_T29SMD_20180925T113309_result_NBR";
        nbrLayer = L.tileLayer(nbrPath + '/{z}/{x}/{y}.png',
            {
                tms: true, opacity: 0.85,
                attribution: 'changeLayer'
            }).addTo(map);
        overlaymaps = {
            "NBRLayer": nbrLayer
        };
        //add nbr Layer here
    } else if (method === 'change') {
        let changePath = "/change/B08_RESULT_T_6clusters (1)";
        changeLayer = L.tileLayer(changePath + '/{z}/{x}/{y}.png',
            {
                tms: true, opacity: 0.85,
                attribution: 'changeLayer'
            }).addTo(map);
        overlaymaps = {
            "changeLayer": changeLayer
        };
    } else if(method=== 'slider') {

        let pathAfter = '/after/T29SMD_20180925T113309_TCI.tif'; //+ pathname after
        layerAfter = L.tileLayer(pathAfter + '/{z}/{x}/{y}.png',
            {
                attribution: 'Layer after change',
                tms: true
            }).addTo(map);

        L.control.sideBySide(layerBefore, layerAfter).addTo(map);
    } else{
        alert("No Change Detection Layer will be displayed")
    };




};

