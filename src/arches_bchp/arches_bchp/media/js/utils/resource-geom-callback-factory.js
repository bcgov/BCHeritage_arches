define(['jquery','underscore' ], function($, _) {
    let resourceGeomCallbackFactory = {
        // This isn't currently used in BCRHP. Look at Fossils implementation for working example
        getCallbackForFeature: function(feature) {
            return null;
        }
    };
    return resourceGeomCallbackFactory;
});