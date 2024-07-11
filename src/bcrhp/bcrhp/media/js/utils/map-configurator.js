define(['mapbox-gl'], function(MapboxGl){

    let mapConfigurator = {
        /* Can tell which context we are in by the following. In each case, we are in that context if the search returns
            an object
            Search map: map.getCanvasContainer().closest("section.search-map-container")
            Map Header: map.getCanvasContainer().closest("div.report-map-header-component")
            Map Editor: map.getCanvasContainer().closest("div.map-widget")
        */
        icons: [],
        /*
        icons: [{"name":"micro-marker", "url":'/int/bc-fossil-management/files/media/img/markers/micro.png'},
            {"name":"macro-marker", "url":'/int/bc-fossil-management/files/media/img/markers/macro.png'},
            {"name":"macromicro-marker", "url":'/int/bc-fossil-management/files/media/img/markers/macromicro.png'},
        ],
         */

        preConfig: function(map) {
            console.log("Custom pre-config");
            console.log("Adding control");
            map.addControl(new MapboxGl.ScaleControl({ maxWidth: 200}));
            this.icons.forEach(function(icon) {
                console.log(`Loading ${icon.name}: ${icon.url}`);
                map.loadImage(icon.url,
                    (error, image) => {
                        if (error) throw error;
                        map.addImage(icon.name, image);
                    });
            });
        },

        postConfig: function(map) {
            console.log("Custom post-config");
            // Workaround for bug in core causing geocoder placeholder to be null
            map._controls.forEach(control => {
                if (control.hasOwnProperty("geocoderService") && control.hasOwnProperty("placeholder"))
              {
                    control.setPlaceholder("Find an address...");
                }
            });
        },
    };

    return mapConfigurator;
});
