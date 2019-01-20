let {PythonShell} = require('python-shell');
let R = require('r-script');

module.exports = {
    callScripts: () => {
        R("../getSpatialData.R");

        PythonShell.run('../pre_processing/apply_sen2cor.py', null, function (err) {
            if (err) {
                throw err;
            }
        })

        //add other scripts here

    }
};