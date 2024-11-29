define([
    'underscore',
        'knockout',
        'viewmodels/report',
        'templates/views/report-templates/bcrhp_default.htm',
], function (_, ko, ReportViewModel, defaultTemplate) {
    const viewModel = function(params) {
        params.configKeys = [];
        ReportViewModel.apply(this, [params]);
        var getAllWidgets = function(card) {
            return _.flatten([ko.unwrap(card.tiles).length === 0 ? [] : ko.unwrap(card.widgets),
                _.map(card.cards(), subcard => {return getAllWidgets(subcard); })]);
        }
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

        var tiles = _.flatten(_.map(params.report.cards, card => {return getAllTiles(card)}));

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
                return typeof(value) === "object" && "en" in value ? !!ko.unwrap(value["en"].value) : !!ko.unwrap(value);
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

        this.submittedSites = ko.computed(function() {
            let opWidget = getWidgetForAlias('requested_operation'),
                infoWidget = getWidgetForAlias('information_provided'),
                siteWidget = getWidgetForAlias('heritage_site');

            var values = [];
            _.each(ko.unwrap(tiles), tile => {
                var opVal = getValueFromTile(tile, opWidget),
                    infoVal = getValueFromTile(tile, infoWidget),
                    siteVal = getValueFromTile(tile, siteWidget);
                if (!!opVal || !!infoVal || !!siteVal)
                    values.push({'requested_operation': ko.observable(opVal),
                        'information_provided': ko.observable(infoVal),
                        'heritage_site': ko.observable(siteVal)});

            });
            return values;
        });
    };

    return ko.components.register('default-report', {
        viewModel: viewModel,
        template: defaultTemplate
    });
});