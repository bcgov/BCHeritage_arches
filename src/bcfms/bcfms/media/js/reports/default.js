define([
        'knockout',
        'viewmodels/bcfms-report',
        'templates/views/report-templates/bcfms_default.htm',
], function (ko, ReportViewModel, defaultTemplate) {
    const viewModel = function(params) {
        params.configKeys = [];


        ReportViewModel.apply(this, [params]);
    };

    return ko.components.register('default-report', {
        viewModel: viewModel,
        template: defaultTemplate
    });
});