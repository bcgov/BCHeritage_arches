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
        var self = this;

        MapReportViewModel.apply(this, [params]);
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

        this.siteNamesVisible = ko.observable(true);
        this.siteLocationVisible = ko.observable(true);
        this.bordenNumberVisible = ko.observable(true);
        this.recognitionInformationVisible = ko.observable(true);
        this.recognitionDetailsVisible = ko.observable(true);
        this.chronologyVisible = ko.observable(true);
        this.sosVisible = ko.observable(true);
        this.heritageClassVisible = ko.observable(true);
        this.heritageFunctionVisible = ko.observable(true);
        this.heritageThemeVisible = ko.observable(true);

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

        var getTilesForAlias = function(node_alias)
        {
            let widget = getWidgetForAlias(node_alias);

            let tiles = !widget ? [] : _.filter(ko.unwrap(self.tiles), tile=>{
                return widget.node.nodeid in tile.data;
            });
            tiles = _.map(tiles, tile => {
                return ko.observable(tile);
            })
            return tiles;
        }

        this.getTilesForAlias = function(node_alias)
        {
            return getTilesForAlias(node_alias);
        };

        var getValueFromTile = function(tile, widget)
        {
            return (!tile || !ko.unwrap(tile) || !widget) ? null : ko.unwrap(ko.unwrap(tile).data[widget.node.nodeid]);
        }

        var getNodeValues = function(node_alias, make_observable = false) {
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
                    values.push(make_observable ? ko.observable(value) : value);
            });
            return values;
        }

        this.getNodeValues = function(node_alias)
        {
            return getNodeValues(node_alias, true);
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

        this.getResourceInstanceValues = function(aliases)
        {
            if (!Array.isArray(aliases))
            {
                aliases = [aliases]
            }
            let widgets = _.map(aliases, alias=> {
                return {"alias": alias, "widget": getWidgetForAlias(alias)}
            });

            let resourceValues = [];
            _.each(ko.unwrap(tiles), tile => {
                _.each(widgets, widget => {
                    let value = getValueFromTile(tile, widget.widget);
                    if (!!value)
                    {
                        resourceValues.push({[widget.alias]: ko.observable(value)});
                    }
                })
            });
            return resourceValues;
        }

        this.clickUrl = function(data, event) {
            let url = event.currentTarget.getElementsByTagName('a')[0]['href'];
            let filename = event.currentTarget.getElementsByTagName('a')[0].text.trim();
            window.open(url, filename);
        }


        /* Old config ... to remove */
        this.getCardWithName = function(cardName) {
            if (_.isArray(cardName))
            {
                return self.getCardWithHierNames(null, cardName);
            }
            let namedCard = _.find(self.report.cards, function(card) {
                return card.model.name() === cardName;
            });
            return namedCard;
        };

        this.getCardWithHierNames = function(parentCard, cardNames) {
            if (parentCard && (!cardNames || cardNames.length === 0))
            {
                return parentCard;
            }
            let cardList = !parentCard ? self.report.cards : parentCard.cards();
            let cardName = _.first(cardNames);

            let namedCard = _.find(cardList, function(card) {
                return card.model.name() === cardName;
            });
            return self.getCardWithHierNames(namedCard, _.last(cardNames, cardNames.length-1));
        };

        this.getWidgetWithLabel = function(card, widgetName) {
            if (!!card)
            {
                let namedWidget = _.find(card.widgets(), function(widget) {
                    return widget.label() === widgetName;
                });
                return namedWidget;
            }
            return null;
        };
    };
});