define([
    'knockout',
    'underscore',
    'viewmodels/widget'
], function(ko, _, WidgetViewModel) {
    /**
     * A viewmodel used for boolean checkbox widgets
     *
     * @constructor
     * @name BooleanCheckboxWidgetViewModel
     *
     * @param  {string} params - a configuration object
     */
    var BooleanCheckboxWidgetViewModel = function(params) {
        var self = this;

        WidgetViewModel.apply(this, [params]);

        var value = self.configForm ? self.defaultValue : self.value;

        this.toggleSelected = function() {
            var selected = !self.isSelected();
            console.log(`Setting selected to ${selected}`);
            self.setSelected(selected);
        };

        this.setSelected = function(selected) {
            if (ko.unwrap(self.disabled) === false) {
                value(selected);
            }
        };

        this.isSelected = function() {
            return !!value();
        };

    };

    return BooleanCheckboxWidgetViewModel;
});
