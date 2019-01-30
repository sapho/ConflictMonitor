$(document).ready(function () {
    /**
     * @desc AJAX.GET to overwrite submit of the searchform.
     *       passes search parameters to the server
     *       find all searched items and and passes them to the tableButton function
     * @return searchdata  or error
     **/
    $('#aoi').submit(function (e) {
        e.preventDefault();
        let that = this;
        $.ajax({
            // catch custom response code.
            statusCode: {
                500: function () {
                    console.error("Object not found");
                }
            },
            data: $(that).serialize(),
            type: 'GET',
            contentType: "application/json",
            // Dynamically create Request URL by appending requested name to /api prefix
            url: '/aoi',
            error: function (xhr, status, err) {
                console.log(err);
            },
            success: function (res) {
                console.log("search answer received");
            }
        });
    });
});