let { PythonShell } = require('python-shell');
let R = require('r-script');
let async = require('async');
let dockerCmdJs = require('docker-cmd-js');
let cmd = new dockerCmdJs.Cmd();

exports.request = function (req, res) {
    async.waterfall([
        function (callback) {
            R("../getSpatialData.R")
            .call(function(err, d) {
                if (err) {
                    console.log(err);
                    callback(new Error("getSpatialData.R failed"));
                } else {
                    console.log("Success getSpatialData.R")
                    callback(null);
                }
            });   
        },
        function (callback) {
            cmd.debug().run('docker run basti_ac')
                .then(function(){
                    callback(null)
                })
                .catch((err) => { callback(new Error("preprocessing failed with message: " + err)) });
        },
            function (callback) {
                cmd.debug().run('docker run basti_c')
                    .then(function(){
                        callback(null)
                    })
                    .catch((err) => { callback(new Error("preprocessing failed with message: " + err)) });
            },
        function (callback) {
            PythonShell.run('../postprocessing/NBR_BOA_Images.py', null, function (err) {
                if (err) {
                    console.log(err);
                    callback(new Error("NBR_BOA_Images failed"));
                } else {
                    console.log("Success NBR_BOA_Images.py");
                    callback(null);
                }
            });
        },
        function (callback) {
            PythonShell.run('../postprocessing/subset.py', null, function (err) {
                if (err) {
                    console.log(err);
                    callback(new Error("subset.py failed"));
                } else {
                    console.log("Success subset.py");
                    callback(null);
                }
            });
        },
        function (callback) {
            R("../bfast.R")
            .call(function(err, d) {
                if (err) {
                    console.log(err);
                    callback(new Error("getSpatialData.R failed"));
                } else {
                    console.log("Success getSpatialData.R")
                    callback(null);
                }
            });
        } /*,
        function (callback) { // Dummy
            PythonShell.run('../dummy/dummy', null, function (err) {
                if (err) {
                    console.log(err);
                    callback(new Error("dummy failed"));
                } else {
                    console.log("Success dummy");
                    callback(null);
                }
            });
        }
*/
    ], function (err, code, result) {
        if (err) {
            if (!err.message) {
                err.message = JSON.stringify(err);
            }
            console.error(colors.red(err.message));
            res.status(code).send(err.message);
        } else {
            res.status(code).send(result);
        }
    }
    );
};