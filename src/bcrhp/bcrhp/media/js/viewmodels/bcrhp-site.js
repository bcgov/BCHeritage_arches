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

    };
});