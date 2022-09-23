define(['knockout', 'underscore', 'viewmodels/widget'], function (ko, _, WidgetViewModel) {
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
                    return widget.label() === widgetName;
                });
                return namedWidget;
            };

            this.streetNumber = ko.computed(function()
            {
                let widget = self.getWidgetWithLabel(self.card(), "Street Number");
                return widget;
            });

            this.streetName = ko.computed(function()
            {
                return self.getWidgetWithLabel(self.card(), "Street Name");
            });

            this.city = ko.computed(function()
            {
                return self.getWidgetWithLabel(self.card(), "City");
            });

            this.province = ko.computed(function()
            {
                return self.getWidgetWithLabel(self.card(), "Province");
            });

        },
        template: { require: 'text!templates/views/components/widgets/civic-address-widget.htm' }
    });
});