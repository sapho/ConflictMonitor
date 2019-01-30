function changeOpacity(group){
   var value = document.getElementById("opacityslider").value;
   if(group===undefined){
      alert("Add a Layer first!")
   } else(group.eachLayer(function (layer) {
        layer.setOpacity(value);
    })
   )
}
