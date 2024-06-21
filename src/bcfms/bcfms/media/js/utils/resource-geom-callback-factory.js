define([ ], function($, _, arches, ko, BaseFilter, MapComponentViewModel, binFeatureCollection, mapStyles, turf, geohash, geojsonExtent, uuid, geojsonhint, popupDataProvider, mapFilterUtils) {
    let resourceGeomCallbackFactory = {
        fossilSiteCallback: function(resource) {
            return JSON.parse(resource["BC Fossil Site Location"]["Area Boundary"]["@value"].replaceAll("'", "\"")).features;
        },
        importantFossilAreaCallback: function(resource) {
            return JSON.parse(resource["Area Boundary"].replaceAll("'", "\"")).features;
        },
        sandboxCallback: function(resource) {
            return JSON.parse(resource["Sandbox Project"]["Project Location"]["Study Area"][0]["@value"].replaceAll("'", "\"")).features;
        },
        getCallbackForFeature: function(feature) {
            console.log(`Feature: ${feature}`);
            if (feature.sourceLayer === "2336968c-1035-11ec-a3aa-5254008afee6") // BC Fossil Site
            {
                return this.fossilSiteCallback;
            } else if (feature.sourceLayer === "c6651266-10c6-11ec-adef-5254008afee6") // Important fossil area
            {
                return this.importantFossilAreaCallback;
            } else if (feature.sourceLayer === "9f2c9e28-dedb-11ed-ac5a-5254004d77d3") // BC Fossil Project Sandbox
            {
                return this.sandboxCallback;
            }
        }
    };
    return resourceGeomCallbackFactory;
});