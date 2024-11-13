define([
    'jquery',
    'underscore',
    'knockout',
    'backbone',
    'arches',
    'viewmodels/alert',
    'js-cookie',
], function($, _, ko, BackBone, arches, AlertViewModel, Cookies) {
    return Backbone.View.extend({
        constructor: function() {
            this.name = 'Base Search View';
            this.filter = {};
            this.defaultQuery = {};
            Backbone.View.apply(this, arguments);
        },

        initialize: function(sharedStateObject) {
            const self = this;
            $.extend(this, sharedStateObject);
            this.query = sharedStateObject.query;
            this.queryString = sharedStateObject.queryString;
            this.updateRequest = sharedStateObject.updateRequest;
            this.userIsReviewer = sharedStateObject.userIsReviewer;
            this.total = sharedStateObject.total;
            this.userid = sharedStateObject.userid;
            this.hits = sharedStateObject.hits;
            this.alert = sharedStateObject.alert;
            this.sharedStateObject = sharedStateObject;
            this.queryString.subscribe(function() {
                if (this.searchViewFiltersLoaded()) {
                    this.doQuery();
                } else {
                    this.searchViewFiltersLoaded.subscribe(function() {
                        this.doQuery();
                    }, this);
                }
            }, this);
            // init query
            if (self.updateRequest === undefined) {
                if (this.searchViewFiltersLoaded()) {
                    this.doQuery();
                } else {
                    this.searchViewFiltersLoaded.subscribe(function() {
                        this.doQuery();
                    }, this);
                }
            }
        },

        doQuery: function() {
            var maxUrlLength = 8192;
            const queryObj = this.query();
            if (self.updateRequest) { self.updateRequest.abort(); }

            var request_type = (arches.urls.search_results.length +
                $.param(this.sharedStateObject.queryString()).split('+').join('%20').length)
            < maxUrlLength ? "GET" : "POST";

            self.updateRequest = $.ajax({
                type: request_type,
                url: arches.urls.search_results,
                data: _.extend(queryObj, {'csrfmiddlewaretoken': Cookies.get('csrftoken')}),
                context: this,
                success: function(response) {
                    _.each(this.sharedStateObject.searchResults, function(value, key, results) {
                        if (key !== 'timestamp') {
                            delete this.sharedStateObject.searchResults[key];
                        }
                    }, this);
                    _.each(response, function(value, key, response) {
                        if (key !== 'timestamp') {
                            this.sharedStateObject.searchResults[key] = value;
                        }
                    }, this);
                    this.sharedStateObject.searchResults.timestamp(response.timestamp);
                    this.sharedStateObject.userIsReviewer(response.reviewer);
                    this.sharedStateObject.userid(response.userid);
                    this.sharedStateObject.total(response.total_results);
                    this.sharedStateObject.hits(response.results.hits.hits.length);
                    this.sharedStateObject.alert(false);
                },
                error: function(response, status, error) {
                    const alert = new AlertViewModel('ep-alert-red', arches.translations.requestFailed.title, response.responseJSON?.message);
                    if(self.updateRequest.statusText !== 'abort'){
                        this.alert(alert);
                    }
                    this.sharedStateObject.loading(false);
                },
                complete: function(request, status) {
                    self.updateRequest = undefined;
                    if (request_type === "GET")
                    {
                        window.history.pushState({}, '', '?' + $.param(queryObj).split('+').join('%20'));
                    }
                    this.sharedStateObject.loading(false);
                }
            });
        },

        clearQuery: function(){
            Object.values(this.searchFilterVms).forEach(function(value){
                if (value()){
                    if (value().clear){
                        value().clear();
                    }
                }
            }, this);
            this.query(this.defaultQuery);
        },
    });
});
