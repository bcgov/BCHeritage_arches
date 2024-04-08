define(['underscore',
    'knockout',
    'knockout-mapping',
    'viewmodels/bcrhp-site',
    'reports/map-header',
    'templates/views/report-templates/map.htm',
    'templates/views/report-templates/details/heritage_site.htm'
], function(_, ko, koMapping, MapReportViewModel, MapHeader, defaultSiteTemplate) {
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
        template: defaultSiteTemplate
    });
});
