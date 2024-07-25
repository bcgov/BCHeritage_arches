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
        ipaCallback: function(resource) {
            return JSON.parse(resource["Project Details"]["Project Site"][0]["Project Location"]["@value"].replaceAll("'", "\"")).features;
        },
        collectionEventCallback: function(resource) {
            return JSON.parse(resource["Collection Details"]["Collection Event Location"]["Collection Location"]["@value"].replaceAll("'", "\"")).features;
        },
        provinciallyProtectedSiteCallback: function(resource) {
            return JSON.parse(resource["BC Fossil Site Location"]["Area Boundary"][0]["@value"].replaceAll("'", "\"")).features;
        },
        getCallbackForFeature: function(feature) {
            // console.log(`Feature: ${feature}`);
            if (feature.sourceLayer === "2336968c-1035-11ec-a3aa-5254008afee6") // BC Fossil Site
            {
                return this.fossilSiteCallback;
            } else if (feature.sourceLayer === "c6651266-10c6-11ec-adef-5254008afee6") // Important fossil area
            {
                return this.importantFossilAreaCallback;
            } else if (feature.sourceLayer === "dd19c7c6-0202-11ed-a511-0050568377a0") // Provincially Protected Site
            {
                return this.provinciallyProtectedSiteCallback;
            } else if (feature.sourceLayer === "9f2c9e28-dedb-11ed-ac5a-5254004d77d3") // BC Fossil Project Sandbox
            {
                return this.sandboxCallback;
            } else if (feature.sourceLayer === "5bfa1354-b6e1-11ee-9438-080027b7463b") // Collection Event
            {
                return this.collectionEventCallback;
            } else if (feature.sourceLayer === "2bb08950-a880-11ed-95a4-5254004d77d3") // IPA
            {
                return this.ipaCallback;
            }
        }
    };
    return resourceGeomCallbackFactory;
});