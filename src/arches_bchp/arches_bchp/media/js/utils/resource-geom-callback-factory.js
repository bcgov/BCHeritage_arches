define([ ], function($, _, arches, ko, BaseFilter, MapComponentViewModel, binFeatureCollection, mapStyles, turf, geohash, geojsonExtent, uuid, geojsonhint, popupDataProvider, mapFilterUtils) {
    let resourceGeomCallbackFactory = {
        // This isn't currently used in BCRHP. Look at Fossils implementation for working example
        getCallbackForFeature: function(feature) {
            return null;
        }
    };
    return resourceGeomCallbackFactory;
});