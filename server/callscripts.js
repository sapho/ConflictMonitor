let {PythonShell} = require('python-shell');
let R = require('r-script');
const { exec } = require('child_process');

module.exports = {
    callScripts: () => {
        R("../getSpatialData.R");

        exec('../pre_processing/composites/apply_sen2cor.bat');
        PythonShell.run('../postprocessing/NBR_BOA_Images.py', null, function (err) {
            if (err) {
                throw err;
            }
        });
        PythonShell.run('../postprocessing/subset.py', null, function (err) {
            if (err) {
                throw err;
            }
        });
        //add other scripts here
        R("../bfast.R");
    }
};