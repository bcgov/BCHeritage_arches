define([
    'jquery',
    'knockout',
    'knockout-mapping',
    'underscore',
    'viewmodels/widget',
    'arches',
    'templates/views/components/widgets/borden-number-widget.htm',
    'bindings/chosen'
], function($, ko, koMapping, _, WidgetViewModel, arches, bordenNumberWidgetTemplate) {
    /**
     * registers a text-widget component for use in forms
     * @function external:"ko.components".text-widget
     * @param {object} params
     * @param {string} params.value - the value being managed
     * @param {function} params.config - observable containing config object
     * @param {string} params.config().label - label to use alongside the text input
     * @param {string} params.config().placeholder - default text to show in the text input
     * @param {string} params.config().uneditable - disables widget
     */

        const viewModel = function(params) {
            params.configKeys = ['placeholder', 'width', 'maxLength', 'defaultValue', 'uneditable'];

            WidgetViewModel.apply(this, [params]);
            const self = this;

            self.card = params.card;
            self.currentLanguage = ko.observable({code: arches.activeLanguage});
            self.languages = ko.observableArray();
            self.currentText = ko.observable();
            self.currentDirection = ko.observable();
            self.showi18nOptions = ko.observable(false);

            self.currentDefaultText = ko.observable();
            self.currentDefaultDirection = ko.observable();
            self.currentDefaultLanguage = ko.observable({code: arches.activeLanguage});
            self.urls = arches.urls;

            const initialCurrent = {};
            const initialDefault = {};
            initialDefault[arches.activeLanguage] = {value: '', direction: 'ltr'};
            initialCurrent[arches.activeLanguage] = {value: '', direction: 'ltr'};
            let currentDefaultValue = ko.unwrap(self.defaultValue) || initialDefault;
            let currentValue = koMapping.toJS(self.value)|| initialCurrent;

            if(self.form){
                self.form.on('after-update', (req, tile) => {
                    if (!!req.responseJSON.data[self.node.id]){
                        self.currentText(req.responseJSON.data[self.node.id][self.currentLanguage().code].value)
                    }
                });
                self.form.on('tile-reset', (x) => {
                    if (ko.unwrap(self.value)) {
                        currentValue = koMapping.toJS(self.value);
                        self.currentText(currentValue[self.currentLanguage().code]?.value);
                        self.currentDirection(currentValue[self.currentLanguage().code]?.direction);
                    }
                });
            }

            const init = async() => {
                const languages = arches.languages;
                const currentLanguage = languages?.find(element => element.code == arches.activeLanguage);
                self.languages(languages);
                self.currentLanguage(currentLanguage);
                self.currentDefaultLanguage(currentLanguage);

                if (currentLanguage?.code && currentValue?.[currentLanguage.code]){
                    self.currentText(currentValue?.[currentLanguage.code]?.value);
                    self.currentDirection(currentValue?.[currentLanguage.code]?.direction);
                } else if (!currentLanguage?.code) {
                    self.currentText('');
                    self.currentDirection('ltr');
                } else if (currentValue) {
                    self.currentText('');
                    self.currentDirection('ltr');
                    currentValue[currentLanguage.code] = {value: '', direction: 'ltr'};
                }

                if(currentLanguage?.code && currentDefaultValue?.[currentLanguage.code]){
                    self.currentDefaultText(currentDefaultValue?.[currentLanguage.code]?.value);
                    self.currentDefaultDirection(currentDefaultValue?.[currentLanguage.code]?.direction);
                } else if (!currentLanguage?.code) {
                    self.currentDefaultText('');
                    self.currentDefaultDirection('ltr');
            } else if (currentDefaultValue) {
                    self.currentDefaultText('');
                    self.currentDefaultDirection('ltr');
                    currentDefaultValue[currentLanguage.code] = {value: '', direction: 'ltr'};
                }
            if (ko.unwrap(self.placeholder) && (typeof ko.unwrap(self.placeholder) !== "string")) {
                self.placeholder(self.placeholder()[self.currentLanguage().code]);
            }
            };

            init();

            self.disable = ko.computed(() => {
                return ko.unwrap(self.disabled) ||
                    ko.unwrap(self.uneditable) ||
                    !!ko.unwrap(self.currentText);
            }, self);

            self.currentDefaultText.subscribe(newValue => {
                const currentLanguage = self.currentDefaultLanguage();
                if(!currentLanguage) { return; }
                currentDefaultValue[currentLanguage.code].value = newValue;
                self.defaultValue(currentDefaultValue);
                self.card._card.valueHasMutated();
            });

            self.currentDefaultDirection.subscribe(newValue => {
                const currentLanguage = self.currentDefaultLanguage();
                if(!currentLanguage) { return; }
                if(!currentDefaultValue?.[currentLanguage.code]){
                    currentDefaultValue[currentLanguage.code] = {};
                }
                currentDefaultValue[currentLanguage.code].direction = newValue;
                self.defaultValue(currentDefaultValue);
                self.card._card.valueHasMutated();
            });

            self.currentDefaultLanguage.subscribe(newValue => {
                if(!self.currentDefaultLanguage()){ return; }
                const currentLanguage = self.currentDefaultLanguage();
                if(!currentDefaultValue?.[currentLanguage.code]) {
                    currentDefaultValue[currentLanguage.code] = {
                        value: '',
                        direction: currentLanguage?.default_direction
                    };
                    self.defaultValue(currentDefaultValue);
                    self.card._card.valueHasMutated();
                }

                self.currentDefaultText(self.defaultValue()?.[currentLanguage.code]?.value);
                self.currentDefaultDirection(self.defaultValue()?.[currentLanguage.code]?.direction);

            });

        const valueLeaf = self.value?.[arches.activeLanguage]?.value || self.value;
        valueLeaf?.subscribe(newValue => {
            const currentLanguage = self.currentLanguage();
            if(!currentLanguage) { return; }
            if(JSON.stringify(currentValue) != JSON.stringify(ko.toJS(ko.unwrap(self.value)))){
                self.currentText(newValue?.[currentLanguage.code]?.value || newValue);
            }
        });

            self.currentText.subscribe(newValue => {
                const currentLanguage = self.currentLanguage();
                if(!currentLanguage) { return; }

            if(!currentValue?.[currentLanguage.code]){
                currentValue[currentLanguage.code] = {};
            }
            currentValue[currentLanguage.code].value = newValue?.[currentLanguage.code] ? newValue[currentLanguage.code]?.value : newValue;

                if (ko.isObservable(self.value)) {
                    self.value(currentValue);
                } else {
                    self.value[currentLanguage.code].value(newValue);
                }

            });

            self.currentDirection.subscribe(newValue => {
                const currentLanguage = self.currentLanguage();
                if(!currentLanguage) { return; }

                if(!currentValue?.[currentLanguage.code]){
                    currentValue[currentLanguage.code] = {};
                }
                currentValue[currentLanguage.code].direction = newValue;
                if (ko.isObservable(self.value)) {
                    self.value(currentValue);
                } else {
                    self.value[currentLanguage.code].direction(newValue);
                }
            });

            self.currentLanguage.subscribe(() => {
                if(!self.currentLanguage()){ return; }
                const currentLanguage = self.currentLanguage();

                self.currentText(koMapping.toJS(self.value)[currentLanguage.code]?.value);
                self.currentDirection(koMapping.toJS(self.value)[currentLanguage.code]?.direction);

            });

            self.getBordenNumber = function() {
                let url = `${self.urls.root}borden_number/${self.tile.resourceinstance_id}`;
                console.log(`Get borden number from ${url}...`)
                self.form.loading(true);
                $.ajax({
                    // type: "PUT",
                    url: url
                }).done(function(data){
                    console.log(`Data: ${JSON.stringify(data)}`);
                    console.log(data);
                    if (data.status === "success")
                    {
                        self.currentText(data.borden_number);
                    }
                    self.form.loading(false);
                });
            }
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
        };

    return ko.components.register('borden-number-widget', {
        viewModel: viewModel,
        template: bordenNumberWidgetTemplate
    });
});
