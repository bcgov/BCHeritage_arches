define([
    'knockout',
    'underscore',
    'utils/map-filter-utils',
    'templates/views/components/map_popup/toggle-map-popup.htm',
    'templates/views/components/map_popup/edit-map-popup.htm'
], function (ko, _, mapFilterUtils, default_template, edit_popup) {
    var popupDataProvider = {
            layerConfigs: {
                "WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW":
                    {displayname: [{"key": "PID", title:""}],
                        "map_popup": [
                            {key: "OWNER_TYPE", title: "Owner Type: "},
                            {key: "MUNICIPALITY", title: "Municipality: "},
                            {key: "PID", title: "PID: "},
                            {key: "PIN", title: "PIN: "},
                            {key: "LEGAL_DESCRIPTION", title: "Legal Description: "},
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
                "WHSE_ADMIN_BOUNDARIES.ADM_INDIAN_RESERVES_BANDS_SP":
                    {
                        displayname: [{"key": "BAND_NAME", title: ""}],
                        "map_popup": [{"key": "BAND_NAME", title: "Band Name: "}],
                    },
                "WHSE_ADMIN_BOUNDARIES.CLAB_INDIAN_RESERVES":
                    {
                        displayname: [{"key": "ENGLISH_NAME", title: ""}],
                        "map_popup": [{key: "FRENCH_NAME", title: "French Name: "},
                        ]
                    },
                "WHSE_TANTALIS.TA_CROWN_TENURES_SVW":
                    {
                        displayname: [{"key": "TENURE_LOCATION", title: ""}],
                        "map_popup": [{key: "TENURE_PURPOSE", title: "Purpose: "},
                            {key: "TENURE_SUBPURPOSE", title: "Subpurpose: "},
                            {key: "RESPONSIBLE_BUSINESS_UNIT", title: "Business Unit: "},
                            {key: "TENURE_STAGE", title: "Stage: "},
                            {key: "TENURE_STATUS", title: "Status: "},
                            {key: "TENURE_TYPE", title: "Type: "},
                            {key: "TENURE_SUBTYPE", title: "Subtype: "},
                            {key: "TENURE_LEGAL_DESCRIPTION", title: "Legal Description: "},
                        ]
                    },
                "WHSE_ARCHAEOLOGY.RAAD_BORDENGRID":
                    {
                        displayname: [{"key": "BORDGRID", title: ""}],
                        "map_popup": [ ]
                    },
                "WHSE_TANTALIS.TA_SURVEY_PARCELS_SVW":
                    {
                        displayname: [{"key": "LAND_TITLE_OFFICE_IDENTIFIER", title: ""}],
                        "map_popup": [
                            {"key": "LAND_TITLE_OFFICE_IDENTIFIER", title: "Identifier: "},
                            {"key": "PARCEL_TYPE", title: "Parcel Type: "}
                        ]
                    },
                "WHSE_LEGAL_ADMIN_BOUNDARIES.ADM_TOURISM_REGIONS_SP":
                    {
                        displayname: [{"key": "TOURISM_REGION_NAME", title: ""}],
                        "map_popup": [{"key": "TOURISM_REGION_NAME", title: "Region Name: "}]
                    },
                "WHSE_LEGAL_ADMIN_BOUNDARIES.ABMS_ISLANDS_TRUST_SP":
                    {
                        displayname: [{"key": "ADMIN_AREA_NAME", title: ""}],
                        "map_popup": [{"key": "ADMIN_AREA_NAME", title: "Admin Area Name: "}]
                    },
                "WHSE_LEGAL_ADMIN_BOUNDARIES.ABMS_LOCAL_TRUST_AREAS_SP":
                    {
                        displayname: [{"key": "ADMIN_AREA_NAME", title: ""}],
                        "map_popup": [
                            {"key": "ADMIN_AREA_NAME", title: "Admin Area Name: "},
                            {"key": "ADMIN_AREA_GROUP_NAME", title: "Admin Area Group Name: "},
                        ]
                    },

            },
        filterLayers: [
            "WHSE_ADMIN_BOUNDARIES.EBC_REGIONAL_DISTRICTS_SP",
            "WHSE_LEGAL_ADMIN_BOUNDARIES.ABMS_MUNICIPALITIES_SP",
            "WHSE_ADMIN_BOUNDARIES.CLAB_INDIAN_RESERVES",
            "WHSE_LEGAL_ADMIN_BOUNDARIES.ABMS_ISLANDS_TRUST_SP",
            "WHSE_LEGAL_ADMIN_BOUNDARIES.ABMS_LOCAL_TRUST_AREAS_SP",
            "WHSE_LEGAL_ADMIN_BOUNDARIES.ADM_TOURISM_REGIONS_SP",
            "WHSE_TANTALIS.TA_PARK_ECORES_PA_SVW",
            "9f2c9e28-dedb-11ed-ac5a-5254004d77d3", /* Project Sandbox layer */
        ],

            isFeatureClickable: function(feature, map){
                // console.log("bchp.isFeatureClickable()")
                // console.log(`Context: ${map.context}`);
                if (map.context === "resource-editor" &&
                    feature.sourceLayer === "WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW" ||
                    !!feature.properties.resourceinstanceid
                )
                {
                    return true;
                }
                const selectedFeatureIds = ko.unwrap(map.selectedFeatureIds);
                const selectedTool = ko.unwrap(map.selectedTool);
                // If the selected tool isn't empty (we're doing a select) and isn't select-by-feature, not it a mode
                // to select anything
                if ((typeof selectedTool !== 'undefined' && selectedTool !== null && selectedTool !== 'filter_by_feature')
                    || selectedFeatureIds && selectedFeatureIds.length)
                    return false;
                if (feature.sourceLayer in popupDataProvider.layerConfigs)
                    return true;
                return feature.properties.resourceinstanceid;
            },

            getPopupTemplate: function(features){
                if (_.some(features, function(feature) {return feature.sourceLayer === "WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW"}))
                    return edit_popup;
                return default_template;
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
            },
            /**
             * This method enables custom logic for how the feature in the popup should be handled and/or mutated en route to the mapFilter.
             * @param popupFeatureObject - the javascript object of the feature and its associated contexts (e.g. mapCard).
             * @required @method mapCard.filterByFeatureGeom()
             * @required @send argument: @param feature - a geojson feature object
             */
            sendFeatureToMapFilter: function(popupFeatureObject, addToFilter)
            {
                const foundFeature = popupFeatureObject.feature.properties.featureid ? this.findPopupFeatureById(popupFeatureObject) : mapFilterUtils.getFeatureFromWFS(popupFeatureObject.feature, popupFeatureObject.feature.sourceLayer);
                popupFeatureObject.mapCard.filterByFeatureGeom(foundFeature, addToFilter);
            },

            /**
             * Determines whether to show the button for Filter By Feature
             * @param popupFeatureObject - the javascript object of the feature and its associated contexts (e.g. mapCard).
             * @returns {boolean} - whether to show "Filter by Feature" on map popup
             * typically dependent on at least 1 feature with a geometry and/or a featureid/resourceid combo
             */
            showFilterByFeature: function(popupFeatureObject) {
                const noFeatureId = popupFeatureObject.feature?.properties?.featureid === undefined;
                if (noFeatureId)
                    return this.isSelectableAsFilter(popupFeatureObject.feature);
                return this.findPopupFeatureById(popupFeatureObject) !== null;
            },
            findPopupFeatureById: function(popupFeatureObject) {
                let foundFeature = null;
                const strippedFeatureId = popupFeatureObject.feature.properties.featureid.replace(/-/g,"");
                for (let geometry of popupFeatureObject.geometries()) {
                    if (geometry.geom && Array.isArray(geometry.geom.features)) {
                        foundFeature = geometry.geom.features.find(feature => feature.id.replace(/-/g, "") === strippedFeatureId);
                        if (foundFeature)
                            break;
                    }
                }
                return foundFeature;
            },
        };
    return popupDataProvider;
});