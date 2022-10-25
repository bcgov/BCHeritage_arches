define([
    'knockout',
    'jquery',
    'arches',
    'viewmodels/workflow',
    'viewmodels/workflow-step',
    'templates/views/components/plugins/public-observation-workflow.htm'
], function(ko, $, arches, Workflow, WorkflowStep, defaultWorkflowTemplate) {
    return ko.components.register('public-observation-workflow', {
        viewModel: function(params) {
            this.componentName = 'public-observation-workflow';

            this.stepConfig = [
                {
                    title: 'Observer Information',
                    name: 'set-observer-info',  /* unique to workflow */
                    required: true,
                    workflowstepclass: 'public-observation-observer-info-step',
                    informationboxdata: {
                        heading: 'Observer Information',
                        text: 'Information about the person that made the fossil observation',
                    },
                    layoutSections: [
                        {
                            componentConfigs: [
                                {
                                    componentName: 'default-card',
                                    uniqueInstanceName: 'observer-info', /* unique to step */
                                    tilesManaged: 'one',
                                    parameters: {
                                        graphid: '82efcd14-82db-11ec-b8e6-5254008afee6',
                                        nodegroupid: 'ac37b2f4-82db-11ec-96d0-5254008afee6',
                                    },
                                },
                            ], 
                        },
                    ]
                },
                {
                    title: 'Location Description',
                    name: 'set-location-description',  /* unique to workflow */
                    required: true,
                    informationboxdata: {
                        heading: 'Place Description',
                        text: 'Provide a detailed description where the fossil was observed',
                    },
                    layoutSections: [
                        {
                            componentConfigs: [
                                {
                                    componentName: 'default-card',
                                    uniqueInstanceName: 'location-description', /* unique to step */
                                    tilesManaged: 'one',
                                    parameters: {
                                        graphid: '82efcd14-82db-11ec-b8e6-5254008afee6',
                                        nodegroupid: '0d429c06-83d8-11ec-9043-5254008afee6',
                                        resourceid: "['set-observer-info']['observer-info'][0]['resourceInstanceId']",
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
                                        graphid: '82efcd14-82db-11ec-b8e6-5254008afee6',
                                        nodegroupid: 'c26e4a9c-82db-11ec-b00b-5254008afee6',
                                        resourceid: "['set-observer-info']['observer-info'][0]['resourceInstanceId']"
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
                                        graphid: '82efcd14-82db-11ec-b8e6-5254008afee6',
                                        nodegroupid: 'a7a473b0-83be-11ec-a0d2-5254008afee6',
                                        resourceid: "['set-observer-info']['observer-info'][0]['resourceInstanceId']"
                                    },
                                },
                            ],
                        },
                    ],
                },
                {
                    title: 'Location Coordinates',
                    name: 'set-location-coordinates',  /* unique to workflow */
                    required: false,
                    informationboxdata: {
                        heading: 'Location Coordinates',
                        text: 'Add a point on the map or upload a GeoJSON or KML file with the site location',
                    },
                    layoutSections: [
                        {
                            componentConfigs: [
                                {
                                    componentName: 'default-card',
                                    uniqueInstanceName: 'location-coordinates', /* unique to step */
                                    tilesManaged: 'one',
                                    parameters: {
                                        graphid: '82efcd14-82db-11ec-b8e6-5254008afee6',
                                        nodegroupid: 'cbe9284c-83be-11ec-805f-5254008afee6',
                                        resourceid: "['set-observer-info']['observer-info'][0]['resourceInstanceId']"
                                    },
                                },
                            ],
                        },
                    ],
                },
                {
                    title: 'Summary',
                    name: 'submit-observation-complete',  /* unique to workflow */
                    description: 'Summary',
                    layoutSections: [
                        {
                            componentConfigs: [
                                {
                                    componentName: 'final-step',
                                    uniqueInstanceName: 'submit-observation-final',
                                    tilesManaged: 'none',
                                    parameters: {
                                        resourceid: "['set-observer-info']['observer-info'][0]['resourceInstanceId']"
                                    },
                                },
                            ],
                        },
                    ],
                }
            ];

            Workflow.apply(this, [params]);
        },
        template: defaultWorkflowTemplate
    });
});
