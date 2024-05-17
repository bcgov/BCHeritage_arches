define(['jquery',
    'underscore',
    'arches',
    'knockout',
    'knockout-mapping',
    'viewmodels/function',
    'bindings/chosen',
    'views/components/simple-switch',
    'templates/views/components/functions/bc-fossil-sample-descriptors.htm'],
function($, _, arches, ko, koMapping, FunctionViewModel, chosen, simpleSwitch, defaultTemplate) {
    return ko.components.register('views/components/functions/bc-fossil-sample-descriptors', {
        viewModel: function(params) {
            FunctionViewModel.apply(this, arguments);
            console.log("HERE!!");
            var nodegroups = {};
            var sortedCards = [];
            this.triggering_nodegroups = params.config.triggering_nodegroups;
            //this.cards = ko.observableArray();
            this.loading = ko.observable(false);
            this.show_value = ko.observable(false);
            this.first_only = ko.observable(false);


            this.graph.nodes.forEach(function(card){
                //this.cards.push(card);
                if (card.datatype !== 'semantic')
                {
                    sortedCards.push(card);
                    nodegroups[card.nodeid] = true;
                }
            }, this);

            sortedCards.sort(function(a, b){ if ( a.name === b.name) return 0; return a.name > b.name ? 1 : -1 })
            this.cards = ko.observableArray(sortedCards);

            this.name = params.config.descriptor_types.name
            this.description = params.config.descriptor_types.description
            this.map_popup = params.config.descriptor_types.map_popup


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
        template:  defaultTemplate
    });
});
