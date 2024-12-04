define([
    'jquery',
    'underscore',
    'slick',
    'knockout',
    'knockout-mapping',
    'arches',
    'viewmodels/map-report',
    'bindings/chosen',
], function($, _, slick, ko, koMapping, arches, MapReportViewModel) {
    $.ready(function() {
        $(".data-carousel").slick({});
    });
    return function(params) {
        var self = this;
        self.urls = arches.urls;
        MapReportViewModel.apply(this, [params]);

        this.helpenable = ko.observable(false);
        this.siteNamesVisible = ko.observable(true);
        this.siteLocationVisible = ko.observable(false);
        this.bordenNumberVisible = ko.observable(true);
        this.recognitionInformationVisible = ko.observable(true);
        this.recognitionDetailsVisible = ko.observable(true);
        this.chronologyVisible = ko.observable(true);
        this.sosVisible = ko.observable(true);
        this.heritageClassVisible = ko.observable(true);
        this.heritageFunctionVisible = ko.observable(true);
        this.heritageThemeVisible = ko.observable(true);
        this.externalUrlsVisible = ko.observable(true);
        this.showAllFields= ko.observable(false);

        var getAllWidgets = function(card) {
            return _.flatten([ko.unwrap(card.tiles).length === 0 ? [] : ko.unwrap(card.widgets),
                _.map(card.cards(), subcard => {return getAllWidgets(subcard); })]);
        }
        var getAllTiles = function(card) {
            return _.flatten([ko.unwrap(card.tiles),
                _.map(card.cards(), subcard => {return getAllTiles(subcard); })]);
        }

        // var widgets = _.flatten(_.map(params.report.cards, card => {return getAllWidgets(card)}));

        var tiles = _.flatten(_.map(params.report.cards, card => {return getAllTiles(card)}));

        var nodeid_to_widget_lookup = _.object(_.map(params.report.attributes.widgets, function (widget) {
            return widget.node_id
        }), params.report.attributes.widgets);
        var node_alias_to_node_lookup = _.object(_.map(params.report.attributes.nodes, function (node) {
            return node.alias
        }), params.report.attributes.nodes);


        this.helpactive = function(state) { this.helpenable(state) };

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

        this.getCardForAlias = function(node_alias)
        {
            const widget = getWidgetForAlias(node_alias);
            return widget ? _.find(self.report.cards, (card) => {return card.nodegroupid === widget.node.nodegroup_id}) : null;
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

        this.getValuesFromTiles = function(node_aliases) {
            let widgets = {};
            node_aliases.map(alias => {
                widgets[alias] = getWidgetForAlias(alias);
            });

            var values_list = [];
            _.each(ko.unwrap(tiles), tile => {
                let tileValues = {};
                _.keys(widgets).map( key => {
                    tileValues[key] = getValueFromTile(tile, widgets[key]);
                });
                if (_.some(_.values(tileValues)))
                {
                    _.each(_.keys(tileValues), k => { tileValues[k] = ko.observable(tileValues[k])});
                    values_list.push(tileValues);
                }
            });
            return values_list;
        };

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

        this.textHasValue = function(textValue, languages = ['en'])
        {
            let textObject = ko.unwrap(textValue);
            return !! languages.find((language) => !!ko.unwrap(ko.unwrap(textObject) ? textObject[language].value : null));
        };

        this.getFirstNodeValue = function(alias) {
            return ko.observable(getNodeValues(alias)[0]);
        };

        this.getFirstBooleanValueLabel = function(alias) {
            var widget = getWidgetForAlias(alias);
            // If we don't have a widget the node doesn't exist
            if (!widget) return "";

            var value = getNodeValues(alias)[0];

            return ko.unwrap(!!value ? widget.node.config.trueLabel : widget.node.config.trueLabel);
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

        this.getFileUrl = function(urltoclean) {
            const url = ko.unwrap(urltoclean);
            const httpRegex = /^https?:\/\//;
            // test whether the url is fully qualified or already starts with url_subpath
            return !url || httpRegex.test(url) || url.startsWith(arches.urls.url_subpath) ? url :
                (arches.urls.url_subpath + url).replace('//', '/');
        };

        this.clickUrl = function(data, event) {
            let url = event.currentTarget.getElementsByTagName('a')[0]['href'];
            let filename = event.currentTarget.getElementsByTagName('a')[0].text.trim();
            window.open(url, filename);
        }

        this.actAuthorities = {};

        this.getUser = function() {
            let user = ko.mapping.fromJS({"username":"","first_name":"","last_name":"","groups":[]});
            $.ajax({
                url: `${self.urls.root}user_profile`
            }).done(function (data) {
                if (data)
                {
                    ko.mapping.fromJS(data, user);
                }
            });
            return user;
        };
        this.user = this.getUser();

        this.fullView = ko.pureComputed(function () {
            return self.showAllFields() || ko.unwrap(self.isAnonymous);
        });

        this.fullViewText = ko.pureComputed(function () {
            return self.fullView() ? 'Hide fields' : 'Show all fields';
        });

        this.isAnonymous = ko.computed( function() {
            return ko.unwrap(this.user.groups).length === 0 || this.user.groups().includes("Guest");
        }, this);

        this.getLegislativeAct = function (relatedActObject) {
            let actId = ko.unwrap(ko.unwrap(relatedActObject)[0].resourceId);
            if (!!actId && this.actAuthorities[actId])
            {
                return this.actAuthorities[actId];
            }

            let authority = {
                display_value: ko.observable(""),
                definition: ko.observable("")
            };
            this.actAuthorities[actId] = authority;

            if (self.report.graph.slug === "heritage_site" && self.tiles().length > 0) {
                let url = `${self.urls.root}legislative_act/${actId}`;
                $.ajax({
                    url: url
                }).done(function (data) {
                    if (!!data && data.length > 0)
                    {
                        authority.display_value(`${data[0].authority}, ${data[0].recognition_type}`);
                        if (data[0].recognition_type_definition)
                        {
                            authority.definition(data[0].recognition_type_definition.value);
                        }
                    }
                });
            }
            return authority;
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
        this.initCarousel = function(parent)
        {
            // $(parent).slick();
            $(parent).slick({
                // accessibility: true,
                // slidesToShow: 2,
                // slidesToScroll: 1,
                // arrowsPlacement: 'split',
                centerMode: true,
                dots: true,
                variableWidth: true,
                infinite: false,
                // autoplay: true,
                // autoplaySpeed: 6000,
                prevArrow:"<button type='button' class='slick-prev pull-left'><i class='fa fa-chevron-left' aria-hidden='false'></i></button>",
                nextArrow:"<button type='button' class='slick-next pull-right'><i class='fa fa-chevron-right' aria-hidden='false'></i></button>"
            });
        };
    };
});
