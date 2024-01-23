define([
    'jquery',
    'knockout',
    'arches',
], function ($, ko , arches) {
    var mapFilterUtils = {
        WFS_URL: arches.urls.root+"bctileserver/geo/ows?service=WFS&version=1.0.0&request=GetFeature&typeNames={layer}"+
            "&maxFeatures=100&outputFormat=application%2Fjson&srsName=EPSG%3A4326&cql_filter=OBJECTID%3D{object_id}",
        isArchesGeometry: function(feature)
        {
            return feature.properties && ko.unwrap(feature.properties.resourceinstanceid);
        },
        getWfsUrl: function(objectId, layer)
        {
            return this.WFS_URL.replace("{layer}", layer).replace("{object_id}", objectId);
        },
        getFeatureFromWFS: function(feature, layer) {
            let geometry;
            let wmfUrl = this.getWfsUrl(feature.properties.OBJECTID, layer);
            $.ajax(wmfUrl,
                {
                    async: false,
                    dataType: "json"
                }).done(function(data)
                {
                    console.log("Got response: "+JSON.stringify(data));
                    geometry = data.features[0];
                    geometry.url = wmfUrl;
                    console.log("Got geometry: "+JSON.stringify(geometry));
                }
            ).fail(function(jqXHR, textStatus, errorThrown){
                console.log("Unable to get geometry: "+textStatus);
            });
            return geometry;
        },
        getGeometryFromResource: function(feature, getFeaturesCallback)
        {
            var resourceGeometry;
            this.updateRequest = $.ajax({
                async: false,
                type: "GET",
                url: arches.urls.api_resources(feature.properties.resourceinstanceid),
                data: "format=json",
                context: this,
                success: function(response) {
                    // var resourceFeatures =
                    //     JSON.parse(response.resource["Area Boundary"]["Spatial Coordinates Geometry"]["@value"].replaceAll("'","\""))
                    // resourceGeometry = resourceFeatures.features;
                    resourceGeometry = getFeaturesCallback(response.resource);
                },
                error: function(response, status, error) {
                    console.log(response);
                    console.log(status);
                    console.log(error);
                },
                complete: function(request, status) {
                    /*
                    this.updateRequest = undefined;
                    window.history.pushState({}, '', '?' + $.param(queryString).split('+').join('%20'));

                     */
                }
            });
            return resourceGeometry;
        },

    }
    return mapFilterUtils;
});