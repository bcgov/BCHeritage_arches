define(['underscore',
    'knockout',
    'knockout-mapping',
    'viewmodels/bcrhp-site',
    'reports/map-header'], function(_, ko, koMapping, MapReportViewModel) {
    var siteViewModel = MapReportViewModel;
    /*
    siteViewModel.extend({
            var self = this;
            self.hi = ko.observable("hi");
            ko.utils.extend(self, new (params));
        }
    }
     */
    return ko.components.register('bcrhp-site-report', {
        viewModel: siteViewModel,
        template: {require: 'text!report-templates/bcrhp_site'}
    });
});
