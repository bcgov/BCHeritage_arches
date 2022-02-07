define([
    'knockout',
    'views/components/search/base-filter',
], function(ko, BaseFilter) {
    var componentName = 'own-data-filter';
    return ko.components.register(componentName, {
        viewModel: BaseFilter.extend({
            initialize: function(options) {
                options.name = 'Own Data Filter';
                BaseFilter.prototype.initialize.call(this, options);
                this.restoreState();
            },

            restoreState: function() {
                var queryObj = this.query();
                queryObj[componentName] = 'enabled';
                this.query(queryObj);
            },

        }),
        template: { require: 'text!templates/views/components/search/own-data-filter.htm' }
    });
});
