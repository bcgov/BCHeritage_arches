define([
    'knockout',
    'underscore',
    'templates/views/components/map_popup/toggle-map-popup.htm'
], function (ko, _, toggle_template) {
    var popupDataProvider = {
            layerConfigs: {
                "WHSE_MINERAL_TENURE.GEOL_BEDROCK_UNIT_POLY_SVW":
                    { displayname: [{"key": "STRATIGRAPHIC_UNIT_CODE", title:""}],
                        map_popup: [{"key": "STRATIGRAPHIC_NAME", "title": "Strat Name:"},
                            {"key": "STRATIGRAPHIC_AGE_NAME", "title": "Strat Name:"},
                            {"key": "ROCK_TYPE_DESCRIPTION", "title": "Rock Type:"}
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
                        ]},
                "WHSE_ADMIN_BOUNDARIES.EBC_REGIONAL_DISTRICTS_SP":
                    {
                        displayname: [{"key": "REGIONAL_DISTRICT_NAME", title: ""}],
                        "map_popup": [{key: "REGIONAL_DISTRICT_ID", title: "District ID: "},
                        ]
                    },
                "WHSE_LEGAL_ADMIN_BOUNDARIES.ABMS_MUNICIPALITIES_SP":
                    {
                        displayname: [{"key": "ADMIN_AREA_NAME", title: ""}],
                        "map_popup": [{key: "ADMIN_AREA_GROUP_NAME", title: "Admin Group: "},
                            {key: "ADMIN_AREA_BOUNDARY_TYPE", title: "Type: "},
                            {key: "AFFECTED_ADMIN_AREA_ABRVN", title: "Affected Area: "},
                        ]
                    },
                "WHSE_TANTALIS.TA_PARK_ECORES_PA_SVW":
                    {
                        displayname: [{"key": "PROTECTED_LANDS_NAME", title: ""}],
                        "map_popup": [{key: "PROTECTED_LANDS_DESIGNATION", title: "Designation: "},
                            {key: "PARK_CLASS", title: "Class: "},
                            {key: "ESTABLISHMENT_DATE", title: "Established: "},
                        ]
                    },
                "WHSE_ADMIN_BOUNDARIES.CLAB_NATIONAL_PARKS":
                    {
                        displayname: [{"key": "ENGLISH_NAME", title: ""}],
                        "map_popup": [{key: "FRENCH_NAME", title: "French Name: "},
                            {key: "LOCAL_NAME", title: "Local Name: "},
                        ]
                    },
                "map_data.fiss_frpc_br":
                    {
                        displayname: [{"key": "strat_unit", title: ""}],
                        "map_popup": [
                            {key: "unit_name", title: "Name: "},
                            {key: "frpc", title: "Ranking: "},
                        ]
                    },
                "map_data.fiss_frpc_ovb":
                    {
                        displayname: [{"key": "strat_unit", title: ""}],
                        "map_popup": [
                            {key: "unit_name", title: "Name: "},
                            {key: "frpc", title: "Ranking: "},
                        ]
                    }


            },
            filterLayers: [
                "WHSE_MINERAL_TENURE.GEOL_BEDROCK_UNIT_POLY_SVW",
                "WHSE_ADMIN_BOUNDARIES.EBC_REGIONAL_DISTRICTS_SP",
                "WHSE_LEGAL_ADMIN_BOUNDARIES.ABMS_MUNICIPALITIES_SP",
                "WHSE_TANTALIS.TA_PARK_ECORES_PA_SVW",
                "WHSE_ADMIN_BOUNDARIES.CLAB_NATIONAL_PARKS",
                "map_data.fiss_frpc_br",
                "map_data.fiss_frpc_ovb",
                "c66518e2-10c6-11ec-adef-5254008afee6", /* Important Areas Resource layer */
                "2336968c-1035-11ec-a3aa-5254008afee6", /* Fossil Site layer */
            ],

            isFeatureClickable: function(feature, map){
                // console.log("fossils_popup_provider.isFeatureClickable()")
                const selectedFeatureIds = ko.unwrap(map.selectedFeatureIds);
                const selectedTool = ko.unwrap(map.selectedTool);
                if ((typeof selectedTool !== 'undefined' && selectedTool !== null) || selectedFeatureIds && selectedFeatureIds.length)
                    
                if (typeof drawMode !== 'undefined' && drawMode !== null && drawMode !== '' && drawMode !== 'filter_by_feature')
                    return false;
                if (feature.sourceLayer in popupDataProvider.layerConfigs)
                    return true;
                return feature.properties.resourceinstanceid;
            },

            getPopupTemplate: function(features){
                return toggle_template;
            },
            isSelectableAsFilter: function(feature) {
                return popupDataProvider.filterLayers.indexOf(feature.sourceLayer) !== -1;
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
        };
    return popupDataProvider;
});