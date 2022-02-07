define([
    'jquery',
    'underscore',
    'arches',
    'knockout',
    'knockout-mapping',
    'mapbox-gl',
    'mapbox-gl-geocoder',
    'viewmodels/map',
    'text!templates/views/components/bchp-map-popup.htm',
    'text!templates/views/components/bchp-cadastral-map-popup.htm'
], function( $, _, arches, ko, koMapping, mapboxgl, MapboxGeocoder, baseModel, popupTemplate, cadastralPopupTemplate) {

    var viewModel = function(params) {
        //ko.applyBindings(baseModel);
        var parentModel = baseModel.apply(this, arguments);
        var self = this;

        this.featurePopupTemplate = this.popupTemplate;
        this.cadastralPopupTemplate = cadastralPopupTemplate;

        /*
        baseModel.isFeatureClickable = function(feature) {
            console.log("bchp-map isFeatureClickable?");
            return feature.properties.resourceinstanceid ||  self.isCadastral(feature);
        };
        this.isFeatureClickable = baseModel.isFeatureClickable;
         */
        this.isFeatureClickable = function(feature) {
            console.log("bchp-map isFeatureClickable?");
            return feature.properties.resourceinstanceid ||  self.isCadastral(feature);
        };

        this.isCadastral = function(feature) {
            return feature.sourceLayer === "WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW";
        };

        this.onFeatureClick = function(feature, lngLat) {
            console.log("bchp-map onFeatureClick");
            self.popupTemplate = self.isCadastral(feature)? self.cadastralPopupTemplate : self.featurePopupTemplate;
            var map = self.map();
            self.popup = new mapboxgl.Popup()
                .setLngLat(lngLat)
                .setHTML(self.popupTemplate)
                .addTo(map);
            ko.applyBindingsToDescendants(
                self.getPopupData(feature),
                self.popup._content
            );
            if (map.getStyle() && feature.id) map.setFeatureState(feature, { selected: true });
            self.popup.on('close', function() {
                if (map.getStyle() && feature.id) map.setFeatureState(feature, { selected: false });
                self.popup = undefined;
            });
        };
    };

    return viewModel;
});
