define([ ], function($, _, arches, ko, BaseFilter, MapComponentViewModel, binFeatureCollection, mapStyles, turf, geohash, geojsonExtent, uuid, geojsonhint, popupDataProvider, mapFilterUtils) {
    let resourceGeomCallbackFactory = {
        sandboxGeometryCallback: function(resource) {
            return JSON.parse(resource["Sandcastle Project"]["Project Location"]["Project Boundary"][0]["@value"].replaceAll("'", "\"")).features;
        },
        getCallbackForFeature: function(feature) {
            console.log(`Feature: ${feature}`);
            if (feature.sourceLayer === "9f2c9e28-dedb-11ed-ac5a-5254004d77d3") // Project Sandbox
            {
                return this.sandboxGeometryCallback;
            }
        }
    };
    return resourceGeomCallbackFactory;
});