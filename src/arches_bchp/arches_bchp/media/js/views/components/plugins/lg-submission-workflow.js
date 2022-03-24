define([
    'knockout',
    'jquery',
    'arches',
    'viewmodels/workflow',
    'viewmodels/workflow-step'
], function(ko, $, arches, Workflow) {
    return ko.components.register('lg-submission-workflow', {
        viewModel: function(params) {
            this.componentName = 'lg-submission-workflow';
            var addressStep =                 {
                title: 'Property Address Prep',
                name: 'set-property-address-prep',
                required: false,
                informationboxdata: {
                    heading: 'Address',
                    text: 'Provide the street address of the property',
                },
                layoutSections: [
                    {
                        componentConfigs: [
                            {
                                componentName: 'default-card',
                                uniqueInstanceName: 'property-address-prep',
                                tilesManaged: 'one',
                                parameters: {
                                    graphid: '224716ae-7b9b-11eb-9ecf-5254008afee6',
                                    nodegroupid: '57819f0c-7c44-11eb-9d65-5254008afee6',
                                    resourceid: "['set-site-name']['site-name'][0]['resourceInstanceId']",
                                },
                            },
                        ],
                    },
                ],
            };

            this.stepConfig = [
                {
                    title: 'Site Name',
                    name: 'set-site-name',  /* unique to workflow */
                    required: true,
                    workflowstepclass: 'lg-submission-name-step',
                    informationboxdata: {
                        heading: 'Common Name',
                        text: 'Name that the site is commonly known as',
                    },
                    layoutSections: [
                        {
                            componentConfigs: [
                                {
                                    componentName: 'default-card',
                                    uniqueInstanceName: 'site-name', /* unique to step */
                                    tilesManaged: 'one',
                                    parameters: {
                                        graphid: '224716ae-7b9b-11eb-9ecf-5254008afee6',
                                        nodegroupid: '70a341ce-7ba0-11eb-8cfe-5254008afee6',
                                    },
                                },
                            ], 
                        },
                    ]
                    ,stepInjectionConfig: {
                        defaultStepChoice: null,
                        stepNameToInjectAfter: function(_step) {
                            return 'set-property-address-prep';
                        },
                        injectionLogic: function(step) {
                            return addressStep;
                        }
                    },
                },
                /*{
                    title: 'Property Address Prep',
                    name: 'set-property-address-prep',
                    required: false,
                    informationboxdata: {
                        heading: 'Address',
                        text: 'Provide the street address of the property',
                    },
                    layoutSections: [
                        {
                            componentConfigs: [
                                {
                                    componentName: 'default-card',
                                    uniqueInstanceName: 'property-address-prep',
                                    tilesManaged: 'one',
                                    parameters: {
                                        graphid: '224716ae-7b9b-11eb-9ecf-5254008afee6',
                                        nodegroupid: '57819f0c-7c44-11eb-9d65-5254008afee6',
                                        resourceid: "['set-site-name']['site-name'][0]['resourceInstanceId']",
                                    },
                                },
                            ],
                        },
                    ],
                },*/
                {
                    title: 'Property Address',
                    name: 'set-property-address',
                    required: true,
                    informationboxdata: {
                        heading: 'Address',
                        text: 'Provide the street address of the property',
                    },
                    layoutSections: [
                        {
                            componentConfigs: [
                                {
                                    componentName: 'default-card',
                                    uniqueInstanceName: 'property-address',
                                    tilesManaged: 'one',
                                    parameters: {
                                        graphid: '224716ae-7b9b-11eb-9ecf-5254008afee6',
                                        nodegroupid: '5781aa1a-7c44-11eb-9d65-5254008afee6',
                                        resourceid: "['set-site-name']['site-name'][0]['resourceInstanceId']",
                                    },
                                },
                            ],
                        },
                    ],
                },
                {
                    title: 'Legal Description',
                    name: 'set-legal-description',
                    required: true,
                    informationboxdata: {
                        heading: 'Legal Description',
                        text: 'Provide the legal description of the property',
                    },
                    layoutSections: [
                        {
                            componentConfigs: [
                                {
                                    componentName: 'default-card',
                                    uniqueInstanceName: 'legal-description',
                                    tilesManaged: 'one',
                                    parameters: {
                                        graphid: '224716ae-7b9b-11eb-9ecf-5254008afee6',
                                        nodegroupid: '5781a4a2-7c44-11eb-9d65-5254008afee6',
                                        resourceid: "['set-site-name']['site-name'][0]['resourceInstanceId']",
                                    },
                                },
                            ],
                        },
                    ],
                },
                {
                    title: 'Spatial Location',
                    name: 'set-spatial-location',
                    required: true,
                    informationboxdata: {
                        heading: 'Legal Description',
                        text: 'Either select a cadastral feature or draw a polygon or upload a geojson file with the site boundaries',
                    },
                    layoutSections: [
                        {
                            componentConfigs: [
                                {
                                    componentName: 'default-card',
                                    uniqueInstanceName: 'spatial-location',
                                    tilesManaged: 'one',
                                    parameters: {
                                        graphid: '224716ae-7b9b-11eb-9ecf-5254008afee6',
                                        nodegroupid: '57817522-7c44-11eb-9d65-5254008afee6',
                                        resourceid: "['set-site-name']['site-name'][0]['resourceInstanceId']",
                                    },
                                },
                            ],
                        },
                    ],
                },
        {
                    title: 'Statement of Significance',
                    name: 'set-sos',  /* unique to workflow */
                    required: true,
                    informationboxdata: {
                        heading: 'Statement of Significance',
                        text: 'Enter a concise description of the significance, heritage value and defining elements',
                    },
                    layoutSections: [
                        {
                            componentConfigs: [
                                {
                                    componentName: 'default-card',
                                    uniqueInstanceName: 'sos', /* unique to step */
                                    tilesManaged: 'one',
                                    parameters: {
                                        graphid: '224716ae-7b9b-11eb-9ecf-5254008afee6',
                                        nodegroupid: 'caf3e8a0-9332-11eb-a27c-5254008afee6',
                                        resourceid: "['set-site-name']['site-name'][0]['resourceInstanceId']",
                                    },
                                },
                            ],
                        },
                    ],
                },
                {
                    title: 'Photographs',
                    name: 'add-photographs',  /* unique to workflow */
                    required: false,
                    informationboxdata: {
                        heading: 'Photographs',
                        text: 'Upload photographs of the observed fossils',
                    },
                    layoutSections: [
                        {
                            componentConfigs: [
                                {
                                    componentName: 'default-card',
                                    uniqueInstanceName: 'photographs', /* unique to step */
                                    tilesManaged: 'one',
                                    parameters: {
                                        graphid: '224716ae-7b9b-11eb-9ecf-5254008afee6',
                                        nodegroupid: '4c032aa0-7b9b-11eb-b087-5254008afee6',
                                        resourceid: "['set-site-name']['site-name'][0]['resourceInstanceId']"
                                    },
                                },
                            ],
                        },
                    ],
                },
                {
                    title: 'Location Map File',
                    name: 'add-location-map-file',  /* unique to workflow */
                    required: false,
                    informationboxdata: {
                        heading: 'Location Map',
                        text: 'Upload image or GIS file of the observed location',
                    },
                    layoutSections: [
                        {
                            componentConfigs: [
                                {
                                    componentName: 'default-card',
                                    uniqueInstanceName: 'location-map-file', /* unique to step */
                                    tilesManaged: 'one',
                                    parameters: {
                                        graphid: '224716ae-7b9b-11eb-9ecf-5254008afee6',
                                        nodegroupid: 'a7a473b0-83be-11ec-a0d2-5254008afee6',
                                        resourceid: "['set-site-name']['site-name'][0]['resourceInstanceId']"
                                    },
                                },
                            ],
                        },
                    ],
                },
                {
                    title: 'Summary',
                    name: 'submit-site',  /* unique to workflow */
                    description: 'Summary',
                    layoutSections: [
                        {
                            componentConfigs: [
                                {
                                    componentName: 'final-step',
                                    uniqueInstanceName: 'submit-site-final',
                                    tilesManaged: 'none',
                                    parameters: {
                                        resourceid: "['set-site-name']['site-name'][0]['resourceInstanceId']"
                                    },
                                },
                            ],
                        },
                    ],
                }
            ];

            Workflow.apply(this, [params]);
        },
        template: { require: 'text!templates/views/components/plugins/lg-submission-workflow.htm' }
    });
});
