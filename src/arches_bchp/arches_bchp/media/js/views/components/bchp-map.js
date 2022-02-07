define([
    'jquery',
    'underscore',
    'arches',
    'knockout',
    'viewmodels/bchp-map',
    'bindings/mapbox-gl',
    'bindings/sortable'
], function($, _, arches, ko, MapViewModel) {
    ko.components.register('bchp-arches-map', {
        viewModel: MapViewModel,
        template: {
            require: 'text!templates/views/components/bhcp-map.htm'
        }
    });
    return MapViewModel;
});
