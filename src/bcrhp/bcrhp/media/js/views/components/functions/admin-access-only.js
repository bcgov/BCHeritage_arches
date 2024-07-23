define(['jquery',
        'knockout',
        'viewmodels/function',
        'bindings/chosen',
        'templates/views/components/functions/admin-access-only.htm'],
    function ($, ko, FunctionViewModel, chosen, defaultSampleFunctionTemplate) {
        return ko.components.register('views/components/functions/admin-access-only', {
            viewModel: function (params) {
                FunctionViewModel.apply(this, arguments);
            },
            template: defaultSampleFunctionTemplate
        });
    });
