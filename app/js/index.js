$(document).ready(function() {
    $("#layerform").submit(e => {
        e.preventDefault();
        let method  = e.target[0].value;
        console.log(e.target[0].value);
        loadLayer(method);
    });
});

