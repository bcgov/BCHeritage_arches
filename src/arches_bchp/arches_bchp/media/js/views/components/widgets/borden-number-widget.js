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
    return ko.components.register('borden-number-widget', {
        viewModel: function(params) {
            params.configKeys = ['placeholder', 'width', 'maxLength', 'defaultValue', 'uneditable'];
            WidgetViewModel.apply(this, [params]);
            /*
            var self = this;
            if (this.value()) {
                this.latitudeLocator = ko.observable(this.value().substring(0,2));
                this.longitudeLocator = ko.observable(this.value().substring(2,4));
                this.sequence = ko.observable(this.value().substring(5));
            } else {
                this.latitudeLocator = ko.observable();
                this.longitudeLocator = ko.observable();
                this.sequence = ko.observable();
            };

            this.preview = ko.pureComputed(function() {
                var res = this.latitudeLocator() + this.longitudeLocator() + "-" + this.sequence();
                this.value(res);
                return res;
            }, this);
             */
        },
        template: { require: 'text!templates/views/components/widgets/borden-number-widget.htm' }
    });
});
