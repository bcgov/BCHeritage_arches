define(['knockout',
        'underscore',
        'arches',
        'viewmodels/widget',
        'templates/views/components/widgets/site-name-filter-widget.htm'],
    function (ko, _, arches, WidgetViewModel, nameFilterTemplate) {
    /**
    * registers a text-widget component for use in forms
    * @function external:"ko.components".text-widget
    * @param {object} params
    * @param {string} params.value - the value being managed
    * @param {function} params.config - observable containing config object
    * @param {string} params.config().label - label to use alongside the text input
    */
    return ko.components.register('site-name-filter-widget', {
        viewModel: function(params) {
            params.configKeys = ['visible_name_types', 'name_widget','name_type_widget'];
            WidgetViewModel.apply(this, [params]);
            var self = this;
            this.tile = ko.observable(params.tile);

            this.nameTypes = params.visible_name_types || ko.observableArray();

            // Change this to computed?
            this.filterByType = ko.observable(ko.unwrap(this.nameTypes).length > 0)

            this.nameWidget = params.name_widget;
            this.nameTypeWidget = params.name_type_widget;

            this.showName = ko.observable(false);
            this.siteNameLabel = ko.observable("");
            this.siteName = ko.unwrap(self.tile).data[self.nameWidget.node.nodeid];

            this.setNameVisible = function(widget)
            {
                if (!ko.unwrap(self.filterByType)){
                    self.showName(true);
                    return;
                }
                var valueid = ko.unwrap(self.tile).data[self.nameTypeWidget.node.nodeid]()
                // @todo Is there a better way to do this?
                if (!!valueid)
                {
                    $.ajax(arches.urls.get_pref_label + '?valueid=' + valueid, {
                        dataType: "json"
                    }).done(function(data) {
                        self.showName(_.contains(self.nameTypes, data.value));
                        self.siteNameLabel(`${data.value} Name`);
                    });
                }
            }

            this.siteNameWidget = ko.computed(function()
            {
                self.setNameVisible();
                return self.nameWidget;
            });

            this.siteNameType = ko.computed(function()
            {
                return ko.unwrap(self.tile).data[self.nameTypeWidget.node.nodeid];
            });

            this.siteNameTypeWidget = ko.computed(function()
            {
                return self.nameTypeWidget;
            });

        },
        template: nameFilterTemplate
    });
});
