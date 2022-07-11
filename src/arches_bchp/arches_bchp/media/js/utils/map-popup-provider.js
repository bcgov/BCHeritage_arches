define([
    'knockout',
    'text!templates/views/components/toggle-map-popup.htm'
], function (ko, default_template) {
    var popupDataProvider = {
            layerConfigs: {
                "WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW":
                    {displayname: [{"key": "PID", title:""}],
                        "map_popup": [{key: "OWNER_TYPE", title: "Owner Type: "},
                            {key: "PLAN_NUMBER", title: "Plan #: "},
                            {key: "PARCEL_CLASS", title: "Parcel Class: "},
                            {key: "MUNICIPALITY", title: "Municipality: "},
                            {key: "REGIONAL_DISTRICT", title: "Parcel Status: "},
                            {key: "PARCEL_STATUS", title: "Parcel Status: "},
                            {key: "PARCEL_START_DATE", title: "Parcel Start Date: "},
                            {key: "FEATURE_AREA_SQM", title: "Size (SQM): "},
                        ]}

            },

            isFeatureClickable: function(feature, map){
                // console.log("bchp.isFeatureClickable()")
                const selectedFeatureIds = ko.unwrap(map.selectedFeatureIds);
                const selectedTool = ko.unwrap(map.selectedTool);
                if ((typeof selectedTool !== 'undefined' && selectedTool !== null) || selectedFeatureIds && selectedFeatureIds.length)
                    return false;
                if (feature.sourceLayer in popupDataProvider.layerConfigs)
                    return true;
                return feature.properties.resourceinstanceid;
            },

            getPopupTemplate: function(feature){
                return default_template;
            },

            processData: function(dataFeatures) {
                console.log(dataFeatures);
                dataFeatures.popupFeatures.forEach(featureData => {
                    if (!featureData.displayname && featureData.feature.sourceLayer in this.layerConfigs)
                    {
                        featureData.displayname = this.getDisplayValue(featureData, this.layerConfigs[featureData.feature.sourceLayer].displayname);
                    }
                    if (!featureData.map_popup && featureData.feature.sourceLayer in this.layerConfigs)
                    {
                        featureData.map_popup = this.getDisplayValue(featureData, this.layerConfigs[featureData.feature.sourceLayer].map_popup);
                    }
                    featureData.showAll = ko.observable(false);
                    featureData.toggleShowAll = function()
                    {
                        featureData.showAll(!featureData.showAll());
                    };
                    featureData.showExpandButton = function(container, event)
                    {
                        console.log(container);
                        var div = $(container).siblings(".hover-feature");
                        if (div.length > 0)
                        {
                            return (div[0].offsetWidth < div[0].scrollWidth ||
                                div[0].offsetHeight < div[0].scrollHeight);
                        }
                    }
                });
                return dataFeatures;
            },
            getDisplayValue: function(featureData, properties) {
                return ko.computed(function()
                {
                    let returnValue = "";
                    properties.forEach(property => {
                        if (featureData[property.key])
                        {
                            if (returnValue != "") returnValue += "<br>"
                            if (property.title)
                            {
                                returnValue +="<b>"+property.title+"</b> "
                            }
                            returnValue += featureData[property.key];
                        }
                    });
                    return returnValue;
                });
            }
        }
    return popupDataProvider;
});