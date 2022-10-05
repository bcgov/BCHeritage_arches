define(['underscore', 'knockout', 'knockout-mapping', 'viewmodels/map-report', 'reports/map-header'], function(_, ko, koMapping, MapReportViewModel) {
    return ko.components.register('bcrhp-site-report', {
        viewModel: MapReportViewModel,
        template: { require: 'text!report-templates/bcrhp_site' }
    });
});
