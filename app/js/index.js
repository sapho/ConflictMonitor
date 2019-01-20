$(document).ready(function() {
    $("#layerform").submit(e => {
        e.preventDefault();
        let layer = e.target[1].value;
        let method  = e.target[0].value;
        console.log(e.target[0].value, e.target[1].value );
        loadLayer(layer, method);
    });
});

