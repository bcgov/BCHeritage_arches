delete from map_layers where name = 'streets';
delete from map_sources where name = 'mapbox-streets';
update widgets set defaultconfig = jsonb_set(defaultconfig,'{basemap}', '"British Columbia Roads"') where name = 'map-widget';