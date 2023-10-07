define(['knockout', 'underscore', 'viewmodels/widget', 'templates/views/components/widgets/civic-address-widget.htm'],
    function (ko, _, WidgetViewModel, defaultCivicAddressWidgetTemplate) {
    /**
    * registers a text-widget component for use in forms
    * @function external:"ko.components".text-widget
    * @param {object} params
    * @param {string} params.value - the value being managed
    * @param {function} params.config - observable containing config object
    * @param {string} params.config().label - label to use alongside the text input
    * @param {string} params.config().placeholder - default text to show in the text input
    */
    return ko.components.register('civic-address-widget', {
        viewModel: function(params) {
            params.configKeys = ['x_placeholder','y_placeholder'];
            WidgetViewModel.apply(this, [params]);
            var self = this;
            this.card = ko.observable(params.card);
            this.tile = ko.observable(params.tile);

            this.getWidgetWithLabel = function(card, widgetName) {
                let namedWidget = _.find(card.widgets(), function(widget) {
                    return widget.node.attributes.source['alias'] === widgetName;
                });
                return namedWidget;
            };

            this.streetAddress = ko.computed(function()
            {
                let widget = self.getWidgetWithLabel(self.card(), "street_address");
                return widget;
            });

            this.city = ko.computed(function()
            {
                return self.getWidgetWithLabel(self.card(), "city");
            });

            this.province = ko.computed(function()
            {
                return self.getWidgetWithLabel(self.card(), "province");
            });

        },
        template: defaultCivicAddressWidgetTemplate
    });
});
