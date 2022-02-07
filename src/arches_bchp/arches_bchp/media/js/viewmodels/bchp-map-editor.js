define([
    'arches',
    'jquery',
    'underscore',
    'knockout',
    'knockout-mapping',
    'uuid',
    'mapbox-gl',
    'mapbox-gl-draw',
    'geojson-extent',
    'geojsonhint',
    'views/components/bchp-map',
    'viewmodels/map-editor',
    'views/components/cards/select-feature-layers',
    'text!templates/views/components/cards/map-popup.htm',
    'text!templates/views/components/cards/bchp-cadastral-map-popup.htm'
], function(arches, $, _, ko, koMapping, uuid, mapboxgl, MapboxDraw, geojsonExtent, geojsonhint, MapComponentViewModel, BaseMapEditorViewModel, selectFeatureLayersFactory, popupTemplate, cadastralPopupTemplate) {
    var viewModel2 = function(params) {
        var self = this;
        self.baseModel =  BaseMapEditorViewModel;
        MapComponentViewModel.apply(this, [params]);
        BaseMapEditorViewModel.apply(this, arguments);
        var resourceId = params.tile ? params.tile.resourceinstance_id : '';
        this.selectSource = ko.observable("cadastral-vector-source");
        this.selectSourceLayer = ko.observable("Cadastral ParcelMap");
        this.selectText = ko.observable("Select Cadastral Feature");
        this.cadastralPopupTemplate = cadastralPopupTemplate;
        var selectSource = this.selectSource();
        var selectSourceLayer = this.selectSourceLayer();
        var selectFeatureLayers = selectFeatureLayersFactory(resourceId, selectSource, selectSourceLayer);

        this.isCadastral = function(feature) {
            return feature.sourceLayer === "WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW";
        };

        this.isFeatureClickable = function(feature)
        {
            console.log("bchp-map-editor isFeatureClickable?");
            //return BaseMapEditorViewModel.prototype.isFeatureClickable.call(this, feature);
            var tool = self.selectedTool();
            console.log("tool: "+tool);
            if (tool && tool !== 'select_feature') return false;
            return feature.properties.resourceinstanceid || self.isSelectable(feature);
        };

        this.onFeatureClick = function(feature, lngLat) {
            console.log("bchp-map-editor onFeatureClick");
            if (this.form.resourceId() === feature.properties.resourceinstanceid)  return;
            self.popupTemplate = self.isCadastral(feature)? self.cadastralPopupTemplate : self.featurePopupTemplate;
            var map = self.map();
            self.popup = new mapboxgl.Popup()
                .setLngLat(lngLat)
                .setHTML(self.popupTemplate)
                .addTo(map);
            //console.log("Content: "+JSON.stringify(feature));
            ko.applyBindingsToDescendants(
                self.getPopupData(feature),
                self.popup._content
            );
            if (map.getStyle() && feature.id) map.setFeatureState(feature, { selected: true });
            self.popup.on('close', function() {
                if (map.getStyle() && feature.id) map.setFeatureState(feature, { selected: false });
                self.popup = undefined;
            });
        };


        class DeleteControl {
            onAdd(map)
            {
                this._map = map;
                this._container = document.createElement('div');
                this._container.className = 'mapboxgl-ctrl mapboxgl-ctrl-group';
                var button = document.createElement('button');
                button.className = 'mapbox-gl-draw_trash';
                var span = document.createElement('span');
                span.className = 'mapboxgl-ctrl-icon';
                button.appendChild(span);
                button.addEventListener("click",  function() {
                    console.log("Click: "+self.draw.getMode());
                    self.draw.trash();
                });
                this._container.appendChild(button);


                //this._container.textContent = 'Hello, world';
                return this._container;
            }
            onRemove(map)
            {
                this._container.parentNode.removeChild(this._container);
                this._map = undefined;
            }
        }
        var setupDraw2 = function(map) {
            map.addControl(new DeleteControl(), "top-left");
            self.draw_mode = ko.pureComputed(function() {
                if (map.draw_mode)
                {
                    console.log("Map!");
                    return "Map!";
                }
                else
                {
                    console.log("No Map!");
                    return "No Map!";
                }
            });
            self.draw_mode.subscribe(function() {
                console.log("Changed!");
            });
            /*
            var modes = MapboxDraw.modes;
            modes.static = {
                onSetup: function() {
                    this.setActionableState();
                    return {};
                },
                toDisplayFeatures: function(state, geojson, display) {
                    display(geojson);
                }
            };
            self.draw = new MapboxDraw({
                displayControlsDefault: false,
                modes: modes,
                controls: {
                    trash: true
                }
            });
            map.addControl(self.draw);
            self.draw.set({
                type: 'FeatureCollection',
                features: self.getDrawFeatures()
            });
            map.on('draw.create', function(e) {
                e.features.forEach(function(feature) {
                    self.draw.setFeatureProperty(feature.id, 'nodeId', self.newNodeId);
                });
                self.updateTiles();
            });
            map.on('draw.update', self.updateTiles);
            map.on('draw.delete', self.updateTiles);
            map.on('draw.modechange', function(e) {
                self.updateTiles();
                self.setSelectLayersVisibility(false);
                map.draw_mode = e.mode;
            });
            map.on('draw.selectionchange', function(e) {
                self.selectedFeatureIds(e.features.map(function(feature) {
                    return feature.id;
                }));
                if (e.features.length > 0) {
                    _.each(self.featureLookup, function(value) {
                        value.selectedTool(null);
                    });
                }
                self.setSelectLayersVisibility(false);
            });

            if (self.form) self.form.on('tile-reset', function() {
                var style = self.map().getStyle();
                if (style) {
                    self.draw.set({
                        type: 'FeatureCollection',
                        features: self.getDrawFeatures()
                    });
                }
                _.each(self.featureLookup, function(value) {
                    if (value.selectedTool()) value.selectedTool('');
                });
            });
            if (self.draw) {
                self.drawAvailable(true);
            }
             */
        };

        this.map.subscribe(setupDraw2);

        self.isSelectable = function(feature) {
            if (self.isCadastral(feature)) return true;
            var selectLayerIds = selectFeatureLayers.map(function(layer) {
                return layer.id;
            });
            return selectLayerIds.indexOf(feature.layer.id) >= 0;
        };

        var addSelectFeatures = function(features) {
            var featureIds = [];
            features.forEach(function(feature) {
                feature.id = uuid.generate();
                if (!feature.properties) feature.properties = {};
                feature.properties = $.extend(feature.properties, { nodeId: self.newNodeId });
                self.draw.add(feature);
                featureIds.push(feature.id);
            });
            self.updateTiles();
            self.popup.remove();
            self.draw.changeMode('simple_select', {
                featureIds: featureIds
            });
            self.selectedFeatureIds(featureIds);
            _.each(self.featureLookup, function(value) {
                value.selectedTool(null);
            });
        };

        self.selectFeature = function(feature) {
            try {
                console.log("Got feature "+feature);
                var geometry;
                var newProperties = {};
                if (self.isCadastral(feature))
                {
                    geometry = self.getFeatureFromWMF(feature);
                    newProperties.fromCadastral = true;
                    newProperties.cadastral_OBJECTID = feature.properties.PID;
                }
                else {
                    geometry = JSON.parse(feature.properties.geojson);
                }
                var newFeature = {
                    "type": "Feature",
                    "properties": newProperties,
                    "geometry": geometry,
                    "showAddButton": "true"
                };
                addSelectFeatures([newFeature]);
            } catch(e) {
                $.getJSON(feature.properties.geojson, function(data) {
                    addSelectFeatures(data.features);
                });
            }
        };

        self.getFeatureFromWMF = function(feature) {
            var geometry;
            var wmfUrl = "https://openmaps.gov.bc.ca/geo/ows?service=WFS&version=1.0.0&request=GetFeature"+
                "&typeNames=WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW&maxFeatures=100&outputFormat=application%2Fjson" +
                "&srsName=EPSG%3A4326&cql_filter=OBJECTID%3D{0}";
            $.ajax(wmfUrl.replace("{0}", feature.properties.OBJECTID),
                {
                    async: false,
                    dataType: "json"
                }).success(function(data)
                {
                    console.log("Got response: "+JSON.stringify(data));
                    geometry = data.features[0].geometry;
                    console.log("Got geometry: "+JSON.stringify(geometry));
                }
            ).error(function(jqXHR, textStatus, errorThrown){
                console.log("Unable to get geometry: "+textStatus);
            });
            return geometry;
        };
    };
    return viewModel2;
});
