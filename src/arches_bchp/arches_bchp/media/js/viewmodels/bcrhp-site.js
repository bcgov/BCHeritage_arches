define([
    'jquery',
    'underscore',
    'knockout',
    'knockout-mapping',
    'arches',
    'viewmodels/map-report',
    'bindings/chosen',
], function($, _, ko, koMapping, arches, MapReportViewModel) {
    return function(params) {
        var self = this;
        var summaryCardNames = ["Site Names", "Borden Number" ];
        var summaryCardWidgets = {"Site Names": ["name"], "Borden Number": ["borden_number"] };

        MapReportViewModel.apply(this, [params]);
        this.isSummaryCard = function(cardName) {
            if (cardName === "Borden Number")
            {
                return true;
            }
            return false;
        };

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

        this.hi = ko.observable("hi");
        this.summaryCards = ko.computed(function(){
            let summaryCardList = [];
            let findFunction = this.getCardWithName;
            summaryCardNames.forEach(function(cardName)
            {
                let card = self.getCardWithName(cardName);
                if (!!card)
                {
                    summaryCardList.push(card);
                }
            });
            return summaryCardList;
            /*
            let allCards = this.report.cards;
            let summaryCards = _.filter(allCards, function(card) {
                return summaryCardNames.indexOf(card.model.name()) > 0;
            });
            return summaryCards;
             */
        }, this);
    };
});