define([
    'jquery',
    'underscore',
    'knockout',
    'knockout-mapping',
    'arches',
    'viewmodels/map-report',
    'bindings/chosen'
], function($, _, ko, koMapping, arches, MapReportViewModel) {
    return function(params) {
        MapReportViewModel.apply(this, [params]);
        var self = this;

        var getAllWidgets = function(card) {
            return _.flatten([ko.unwrap(card.tiles).length === 0 ? [] : ko.unwrap(card.widgets),
                _.map(card.cards(), subcard => {return getAllWidgets(subcard); })]);
        }
        var getAllTiles = function(card) {
            return _.flatten([ko.unwrap(card.tiles),
                _.map(card.cards(), subcard => {return getAllTiles(subcard); })]);
        }
        var widgets = _.flatten(_.map(params.report.cards, card => {return getAllWidgets(card)}));

        var tiles = _.flatten(_.map(params.report.cards, card => {return getAllTiles(card)}));

        var getWidgetForAlias = function(node_alias){
            var widget = _.find(widgets, widget => {
                return ko.unwrap(widget.node.alias) === node_alias;
            })
            return widget;
        };

        // Used by template to get widgets for config
        this.getWidgetForAlias = function(node_alias) {
            return getWidgetForAlias(node_alias);
        }
        
        var getValueFromTile = function(tile, widget)
        {
            return (!tile || !widget) ? null : ko.unwrap(tile.data[widget.node.nodeid]);
        }

        var getNodeValues = function(node_alias) {
            var widget = getWidgetForAlias(node_alias);
            if (widget === null)
            {
                console.log(`Node with alias ${node_alias} does not exist.`)
                return [];
            }

            var values = [];
            _.each(ko.unwrap(tiles), tile => {
                var value = getValueFromTile(tile, widget)
                if (!!value)
                    values.push(value);
            });
            return values;
        }

        this.nodesHaveData = function(aliases, requireAll = false)
        {
            let values =  [];
            _.each(aliases, alias => {
                values.push(getNodeValues(alias));
            });
            return !!_.find(_.flatten(values), value => {
                return ko.unwrap(value) != null
            });
        }

        this.getFirstNodeValue = function(alias) {
            return ko.observable(getNodeValues(alias)[0]);
        };

        this.clickUrl = function(data, event) {
            let url = event.currentTarget.getElementsByTagName('a')[0]['href'];
            let filename = event.currentTarget.getElementsByTagName('a')[0].text.trim();
            window.open(url, filename);
        }

        this.getFirstBooleanValueLabel = function(alias) {
            var widget = getWidgetForAlias(alias);
            // If we don't have a widget the node doesn't exist
            if (!widget) return "";

            var value = getNodeValues(alias)[0];

            return ko.unwrap(!!value ? widget.node.config.trueLabel : widget.node.config.trueLabel);
        };

        this.scientificNames = ko.computed(function() {
            let sciNameWidget = getWidgetForAlias('scientific_name'),
                connWidget = getWidgetForAlias('open_nomanclature_term'),
                otherNameWidget = getWidgetForAlias('other_scientific_name');

            var values = [];
            _.each(ko.unwrap(tiles), tile => {
                var sciVal = getValueFromTile(tile, sciNameWidget),
                    connVal = getValueFromTile(tile, connWidget),
                    otherNameVal = getValueFromTile(tile, otherNameWidget);
                if (!!sciVal || !!connVal || !!otherNameVal)
                    values.push({'scientific_name': ko.observable(sciVal),
                        'open_nomanclature_term': ko.observable(connVal),
                        'other_scientific_name': ko.observable(otherNameVal)});

            });
            return values;
        });

        this.commonNames = ko.computed(function() {
            let commonNameWidget = getWidgetForAlias('fossil_common_name'),
                 uncertainWidget = getWidgetForAlias('common_name_uncertain');

            var values = [];
            _.each(ko.unwrap(tiles), tile => {
                var commonVal = getValueFromTile(tile, commonNameWidget),
                uncertainVal = getValueFromTile(tile, uncertainWidget);
                if (!!commonVal)
                    values.push({'fossil_common_name': ko.observable(commonVal),
                    'common_name_uncertain': ko.observable(uncertainVal)});
            });
            return values;
        })

    };

});