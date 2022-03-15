define(['jquery',
    'underscore',
    'arches',
    'knockout',
    'knockout-mapping',
    'viewmodels/function',
    'bindings/chosen'],
function($, _, arches, ko, koMapping, FunctionViewModel, chosen) {
    return ko.components.register('views/components/functions/bc-fossils-descriptors', {
        viewModel: function(params) {
            FunctionViewModel.apply(this, arguments);
            console.log("params"+JSON.stringify(params))
            var nodegroups = {};
            this.triggering_nodegroups = params.config.triggering_nodegroups;
            this.cards = ko.observableArray();
            this.loading = ko.observable(false);

            this.graph.cards.forEach(function(card){
                this.cards.push(card);
                nodegroups[card.nodegroup_id] = true;
            }, this);

            this.descriptor_types = params.config.descriptor_types.type;

            window.setTimeout(function(){$("select[data-bind^=chosen]").trigger("chosen:updated");}, 300);
        },
        template: {
            require: 'text!templates/views/components/functions/bc-fossils-descriptors.htm'
        }
    });
});
