define(['underscore', 'knockout', 'knockout-mapping', 'viewmodels/bchp-map-report', 'reports/bchp-map-header'], function(_, ko, koMapping, MapReportViewModel) {
    return ko.components.register('bchp-map-report', {
        viewModel: MapReportViewModel,
        template: { require: 'text!report-templates/bchp-map' }
    });
});
