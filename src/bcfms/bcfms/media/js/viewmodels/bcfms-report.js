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
        self.urls = arches.urls;

        this.projectDetailsVisible =  ko.observable(true);
        this.projectSiteVisible =  ko.observable(true);
        this.initialProjectReviewVisible = ko.observable(true);
        this.psrVisible = ko.observable(true);
        this.fiaVisible = ko.observable(true);
        this.cfpVisible = ko.observable(true);
        this.impVisible = ko.observable(true);
        this.sapVisible = ko.observable(true);

        this.getAllTiles = function(card) {
            return _.flatten([ko.unwrap(card.tiles),
                _.map(card.cards(), subcard => {return self.getAllTiles(subcard); })]);
        }

        var nodeid_to_widget_lookup = _.object(_.map(params.report.attributes.widgets, function (widget) {
            return widget.node_id
        }), params.report.attributes.widgets);
        var node_alias_to_node_lookup = _.object(_.map(params.report.attributes.nodes, function (node) {
            return node.alias
        }), params.report.attributes.nodes);

        var tiles = _.flatten(_.map(params.report.cards, card => {return self.getAllTiles(card)}));

        var getWidgetForAlias = function(node_alias){
            if (node_alias in node_alias_to_node_lookup)
            {
                return _.extend(nodeid_to_widget_lookup[node_alias_to_node_lookup[node_alias].nodeid],
                    {"node": node_alias_to_node_lookup[node_alias]});
            }
            return null;
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
                if (value === false || !!value)
                    values.push(value);
            });
            return values;
        }

        this.nodesHaveData = function(aliases, requireAll = false)
        {
            const aliases_array = Array.isArray(aliases) ? aliases : [aliases];
            let values =  [];
            _.each(aliases_array, alias => {
                values.push(getNodeValues(alias)[0]);
            });
            const foundValue =  !!_.some(_.flatten(values), value => {
                return typeof(value) === "object" && "en" in value ? !!ko.unwrap(value["en"].value) :
                    ko.unwrap(value) === false || !!ko.unwrap(value);
            });
            return foundValue;
        }

        this.getFirstNodeValue = function(alias) {
            return ko.observable(getNodeValues(alias)[0]);
        };

        /**
         * Returns the first point of the first geometry held in the alias node in a
         * <Latitude>, <Longitude> format
         * @param alias Alias of the geometry Node
         * @returns {null|string} Geometry point text
         */
        this.getPoint = function(alias) {
            let geometries = ko.unwrap(self.getFirstNodeValue(alias))?.features();
            if (!!geometries && geometries.length > 0)
            {
                return `${geometries[0].geometry.coordinates()[1]}\u00BA, ${geometries[0].geometry.coordinates()[0]}\u00BA`;
            }
            return null;
        }

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


            return typeof value === "undefined" ? "" :
                ko.unwrap(!!value ? widget.node.config.trueLabel : widget.node.config.falseLabel);
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
        });

        this.getFossilNamesForCollectionEvent = ko.computed(function () {
            let names = ko.observableArray([]);
            if (self.report.graph.slug === "collection_event" && self.tiles().length > 0) {
                let url = `${self.urls.root}collection_event_fossil_names/${self.tiles()[0].resourceinstance_id}`;
                console.log(`Get fossil names from ${url}...`)
                $.ajax({
                    url: url
                }).done(function(data){
                    // console.log(data);
                    names(data);
                });
            }
            return names;
        });
        this.fossilNamesForCollectionEvent = self.getFossilNamesForCollectionEvent();
    };

});