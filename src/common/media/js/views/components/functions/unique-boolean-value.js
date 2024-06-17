define(['jquery',
    'underscore',
    'arches',
    'knockout',
    'knockout-mapping',
    'viewmodels/function',
    'bindings/chosen',
    'views/components/simple-switch',
    'templates/views/components/functions/unique-boolean-value.htm'],
function($, _, arches, ko, koMapping, FunctionViewModel, chosen, simpleSwitch, template) {
    return ko.components.register('views/components/functions/unique-boolean-value', {
        viewModel: function(params) {
            FunctionViewModel.apply(this, arguments);
            var nodegroups = {};
            var sortedCards = [];
            this.triggering_nodegroups = params.config.triggering_nodegroups;
            this.loading = ko.observable(false);

            this.graph.nodes.forEach(function(card){
                if (card.datatype === 'boolean')
                {
                    sortedCards.push(card);
                    nodegroups[card.nodeid] = true;
                }
            }, this);

            sortedCards.sort(function(a, b){ if ( a.name === b.name) return 0; return a.name > b.name ? 1 : -1 })
            this.cards = ko.observableArray(sortedCards);

            this.unique_value = params.config.unique_value
            this.node_id = params.config.node_id
            this.node_id.subscribe(function(newValue) {
                this.node_id(newValue);
                console.log("New value: "+newValue);
                this.graph.nodes.forEach(function(node) {
                    if (node.nodeid == newValue)
                    {
                        this.triggering_nodegroups([node.nodegroup_id]);
                    }
                }, this)
            }, this);

            window.setTimeout(function(){$("select[data-bind^=chosen]").trigger("chosen:updated");}, 300);
        },
        template: template
    });
});
