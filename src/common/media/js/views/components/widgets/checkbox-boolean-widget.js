define([
    'knockout', 
    'underscore', 
    'viewmodels/checkbox-boolean-widget',
    'templates/views/components/widgets/checkbox-boolean.htm',
], function(ko, _, BooleanCheckboxWidgetViewModel, checkboxBooleanWidgetTemplate) {
    /**
    * knockout components namespace used in arches
    * @external "ko.components"
    * @see http://knockoutjs.com/documentation/component-binding.html
    */

    /**
    * registers a radio-boolean-widget component for use in forms
    * @function external:"ko.components".radio-boolean-widget
    * @param {object} params
    * @param {boolean} params.value - the value being managed
    * @param {boolean} params.defaultValue - automatically assigned to value when the widget appears in a form
    * @param {object} params.config -
    * @param {string} params.config.label - label to use alongside the select input
    */

    const viewModel = function(params) {
        params.configKeys = ['defaultValue'/*, 'trueLabel', 'falseLabel'*/];
         
        BooleanCheckboxWidgetViewModel.apply(this, [params]);
        var self = this;
        this.setValue = function(val) {
            if (ko.unwrap(self.disabled) === false) {
                if (val === self.value()) {
                    self.value(null);
                } else {
                    self.value(val);
                }
            }
        };

        this.displayValue = ko.computed(function() {
            if (this.value()===true) {
                return this.node.config.trueLabel;
            }
            else /*if (this.value()===false)*/ {
                return this.node.config.falseLabel;
            }
        }, self);

        this.setDefaultValue = function(val) {
            if (val === self.defaultValue()) {
                self.defaultValue(null);
            } else {
                self.defaultValue(val);
            }
        };

        var defaultValue = ko.unwrap(this.defaultValue);

        if (self.value() === null && self.defaultValue() !== null) {
            self.value(self.defaultValue());
        }
        if (this.tile && ko.unwrap(this.tile.tileid) === "" && defaultValue != null && defaultValue !== "") {
            this.value(defaultValue);
        }
    };

    return ko.components.register('checkbox-boolean-widget', {
        viewModel: viewModel,
        template: checkboxBooleanWidgetTemplate,
    });
});
