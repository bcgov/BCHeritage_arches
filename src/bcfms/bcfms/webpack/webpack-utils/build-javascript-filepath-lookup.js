const Path = require('path');
const fs = require('fs');

function buildJavascriptFilepathLookup(path, extension) {
    if (!fs.existsSync(path)) {
        return;
    }

    let prefix = path.replace(/\/.*$/,'');

    let getFileList = function (dirPath) {
        return fs.readdirSync(dirPath, { withFileTypes: true }).reduce((fileList,entries) => {
            const childPath = Path.join(dirPath, entries.name)
            if (entries.isDirectory()) {
                fileList.push(...getFileList(childPath, fileList));
            } else
            {
                fileList.push(childPath);
            }
            return fileList;
            }, [])
        };
    // Should we only add files that end in .js?
    return getFileList(path).reduce((lookup, file) => {
        lookup[file.replace(path,'').replace(/\\/g, '/').replace(/\.js$/,'').replace(/^\//,'')] = {"import": file, "filename": `${prefix}/[name].${extension}`};
        return lookup;
    }, {});

    // // Should we only add files that end in .js?
    // let allFiles2 = myfiles.reduce((lookup, file) => {
    //     lookup[file.replace(path,'').replace(/\\/g, '/').replace(/\.js$/,'').replace(/^\//,'')] = {"import": file, "filename": "js/[name].js"};
    //     return lookup;
    // }, {});
    //
    // // console.log("allFiles2");
    // console.log(allFiles2);
    // // console.log("ENDallFiles2");
    // return allFiles2;

    // allFiles.forEach(function(file) {
    //             console.log(file);
    //             outerAcc[file.replace(path,'').replace(/\\/g, '/').replace(/\.js$/,'').replace(/^\//,'')] = {"import": file, "filename": "js/[name].js"};
    //         });
    //
    // return outerAcc;


    // return fs.readdirSync(path).reduce((acc, name) => {
    //     const outerPath = javascriptDirectoryPath || path;   // original `path` arg is persisted through recursion
    //
    //     if (fs.lstatSync(Path.join(path, name)).isDirectory() ) {
    //         return buildJavascriptFilepathLookup(
    //             Path.join(path, name),
    //             acc,
    //             outerPath
    //         );
    //     }
    //     else {
    //         let subPath = Path.join(path, name).split(/js(.*)/s)[1];  // splits only on first occurance
    //         subPath = subPath.substring(1);
    //         const parsedPath = Path.parse(subPath);
    //
    //         let pathName = parsedPath['name'];
    //
    //         if (parsedPath['dir']) {
    //             pathName = Path.join(parsedPath['dir'], parsedPath['name']);
    //         }
    //
    //         if (pathName.includes('.DS_Store')) {
    //             return acc;
    //         }
    //         else {
    //             return {
    //                 ...acc,
    //                 [pathName.replace(/\\/g, '/')]: { 'import': Path.join(outerPath, subPath), 'filename': Path.join('js', '[name].js') }
    //             };
    //         }
    //     }
    // }, outerAcc);
}

module.exports = { buildJavascriptFilepathLookup };