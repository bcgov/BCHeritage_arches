define(['jquery',
        'knockout',
        'viewmodels/function',
        'bindings/chosen',
        'templates/views/components/functions/restricted-site-access.htm'],
    function ($, ko, FunctionViewModel, chosen, defaultSampleFunctionTemplate) {
        return ko.components.register('views/components/functions/restricted-site-access', {
            viewModel: function (params) {
                FunctionViewModel.apply(this, arguments);
            },
            template: defaultSampleFunctionTemplate
        });
    });
