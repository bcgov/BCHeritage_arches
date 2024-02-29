define(['underscore',
        'knockout',
        'knockout-mapping',
        'viewmodels/map-report',
        'reports/map-header',
        'templates/views/report-templates/bcrhp_default.htm'],
    function(_, ko, koMapping, MapReportViewModel, MapHeader, defaultBchpSiteTemplate) {
    return ko.components.register('bcrhp-site-report', {
        viewModel: MapReportViewModel,
        template: defaultBchpSiteTemplate
    });
});
