define(['jquery',
    'underscore',
    'arches',
    'knockout',
    'knockout-mapping',
    'viewmodels/function',
    'bindings/chosen',
    'views/components/simple-switch',
    'templates/views/components/functions/bc-fossil-type-descriptors.htm'],
function($, _, arches, ko, koMapping, FunctionViewModel, chosen, simpleSwitch, defaultFossilsDescriptorsTemplate) {
    return ko.components.register('views/components/functions/bc-fossil-type-descriptors', {
        viewModel: function(params) {
            FunctionViewModel.apply(this, arguments);

            this.reindexdb = function(){
                this.loading(true);
                $.ajax({
                    type: "POST",
                    url: arches.urls.reindex,
                    context: this,
                    data: JSON.stringify({'graphids': [this.graph.graphid]}),
                    error: function() {
                        console.log('error');
                    },
                    complete: function(){
                        this.loading(false);
                    }
                });
            };

            window.setTimeout(function(){$("select[data-bind^=chosen]").trigger("chosen:updated");}, 300);
        },
        template: defaultFossilsDescriptorsTemplate
    });
});
