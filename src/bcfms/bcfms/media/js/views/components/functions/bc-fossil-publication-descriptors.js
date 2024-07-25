define(['jquery',
    'underscore',
    'arches',
    'knockout',
    'knockout-mapping',
    'viewmodels/function',
    'bindings/chosen',
    'views/components/simple-switch',
    'templates/views/components/functions/bc-fossil-publication-descriptors.htm'],
function($, _, arches, ko, koMapping, FunctionViewModel, chosen, simpleSwitch, defaultFossilsDescriptorsTemplate) {
    return ko.components.register('views/components/functions/bc-fossil-publication-descriptors', {
        viewModel: function(params) {
            FunctionViewModel.apply(this, arguments);
            console.log("params2"+JSON.stringify(params))
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

            _.each([this.name, this.description, this.map_popup], function(property){
                if (property.nodegroup_id) {
                    property.nodegroup_id.subscribe(function(nodegroup_id){
                        console.log('Hi');
                        property.string_template(nodegroup_id);

                        var nodes = _.filter(this.graph.nodes, function(node){
                            return node.nodegroup_id === nodegroup_id;
                        }, this);
                        var templateFragments = [];
                        _.each(nodes, function(node){
                            templateFragments.push('<' + node.name + '>');
                        }, this);

                        var template = templateFragments.join(', ');
                        property.string_template(template);
                    }, this);

                }
                // if (property.card_names) {
                //     property.card_names.subscribe(function(card_names){
                //         var templateFragments = [];
                //         //property.string_template(card_names);
                //         _.each(card_names, function(card_name){
                //             console.log(card_name);
                //             var node = _.filter(this.graph.nodes, function(node){
                //                 return node.name === card_name;
                //             }, this);
                //             templateFragments.push('<' + node.name + '>');
                //         }, this);
                //
                //         /*
                //         var nodes = _.filter(this.graph.nodes, function(node){
                //             return node.nodegroup_id === nodegroup_id;
                //         }, this);
                //         _.each(nodes, function(node){
                //             templateFragments.push('<' + node.name + '>');
                //         }, this);
                //
                //         var template = templateFragments.join(', ');
                //         property.string_template(template);
                //          */
                //     }, this);
                // }
            }, this);

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
        template:  defaultFossilsDescriptorsTemplate
    });
});
