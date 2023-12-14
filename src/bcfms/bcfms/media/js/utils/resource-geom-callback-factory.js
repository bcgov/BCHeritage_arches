define([ ], function($, _, arches, ko, BaseFilter, MapComponentViewModel, binFeatureCollection, mapStyles, turf, geohash, geojsonExtent, uuid, geojsonhint, popupDataProvider, mapFilterUtils) {
    let resourceGeomCallbackFactory = {
        fossilSiteCallback: function(resource) {
            return JSON.parse(resource["BC Fossil Site Location"]["Spatial Coordinates Geometry"]["@value"].replaceAll("'", "\"")).features;
        },
        importantFossilAreaCallback: function(resource) {
            return JSON.parse(resource["Area Boundary"]["Spatial Coordinates Geometry"]["@value"].replaceAll("'", "\"")).features;
        },
        getCallbackForFeature: function(feature) {
            console.log(`Feature: ${feature}`);
            if (feature.sourceLayer === "2336968c-1035-11ec-a3aa-5254008afee6") // BC Fossil Site
            {
                return this.fossilSiteCallback;
            } else if (feature.sourceLayer === "c66518e2-10c6-11ec-adef-5254008afee6") // Important fossil area
            {
                return this.importantFossilAreaCallback;
            }
        }
    };
    return resourceGeomCallbackFactory;
});