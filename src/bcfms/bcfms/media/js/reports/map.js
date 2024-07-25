define([
    'underscore', 
    'knockout', 
    'knockout-mapping', 
    'viewmodels/map-report',
    'viewmodels/bcfms-report',
    'templates/views/report-templates/map.htm',
], function(_, ko, koMapping, MapReportViewModel, BcfmsReportViewModel, mapReportTemplate) {
    const viewModel = function(params) {
        params.configKeys = [];
        MapReportViewModel.apply(this, [params]);
        BcfmsReportViewModel.apply(this, [params]);
    };

    return ko.components.register('map-report', {
        viewModel: viewModel,
        template: mapReportTemplate
    });
});
