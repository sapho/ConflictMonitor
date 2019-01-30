var polygonString;
 var polygonLayer = L.featureGroup([])
var previewStyle = {
    "color": "red",
    "weight": 5
};

//collecting necessary metadata to generate a footprint to display on the map

function addPreview(res) {
  if(map.hasLayer(polygonLayer)){
    map.removeLayer(polygonLayer)
  }
    for(var i = 0; i < res.length; i++) {
        if (res[i] !== undefined){

            polygonString = res[i].footprint;


        var previewCoords = [];
        polygonString = polygonString.replace('POLYGON((', '');
        polygonString = polygonString.replace('))', '');
        polygonString = polygonString.replace(/,/g, '');
        polygonStringArray = polygonString.split(" ");
        for (var n = 0; n < polygonStringArray.length; n++) {
            var previewCorrdsPair = [];
            previewCorrdsPair.push(parseFloat(polygonStringArray[n]));
            previewCorrdsPair.push(parseFloat(polygonStringArray[n + 1]));
            previewCoords.push(previewCorrdsPair);
            n++
        }
        var polygon = L.polygon(previewCoords, {color: 'red'})
      polygonLayer.addLayer(polygon);
    }}
};
