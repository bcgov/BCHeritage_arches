define([
    'knockout',
    'text!templates/views/components/map_popup/toggle-map-popup.htm',
    'text!templates/views/components/map-popup.htm'
], function (ko, toggle_template, default_template) {
    var popupDataProvider = {
            layerConfigs: {
                "WHSE_MINERAL_TENURE.GEOL_BEDROCK_UNIT_POLY_SVW":
                    { displayname: [{"key": "PROJECT_NAME", title:""}],
                        map_popup: [{"key": "MAXIMUM_AGE_NAME", "title": "Max. Age:"},
                            {"key": "MINIMUM_AGE_NAME", "title": "Min Age:"},
                            {"key": "AGE_GROUP", "title": "Age Group:"},
                            {"key": "GROUP_SUITE_NAME", "title": "Group Suite:"},
                            {"key": "ORIGINAL_DESCRIPTION", "title": "Description:"},
                        ]},
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

            isFeatureClickable: function(feature, context){
                console.log("fossils_popup_provider.isFeatureClickable()")
                // return defaultProvider.isFeatureClickable(feature);
                if (feature.sourceLayer in popupDataProvider.layerConfigs)
                    return true;
                return feature.properties.resourceinstanceid;
            },

            getPopupTemplate: function(feature){
                // return default_template;
                return toggle_template;

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