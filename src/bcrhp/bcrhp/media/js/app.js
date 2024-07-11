// FIXME same setup as arches one.app.js but for some reason App is not
// available when it needs to be
var App = function () {
  function handleBootstrap() {
    /*Tooltips*/
    // FIXME not sure why it's initializing at this time, maybe the DOM
    // hasn't populated yet, when in the browser console, running this works
    //jQuery('[data-toggle="tooltip"]').tooltip();
    //jQuery('.tooltips-show').tooltip('show');
    //jQuery('.tooltips-hide').tooltip('hide');
    //jQuery('.tooltips-toggle').tooltip('toggle');
    //jQuery('.tooltips-destroy').tooltip('destroy');

    /*Popovers*/
    //jQuery('.popovers').popover();
    //jQuery('.popovers-show').popover('show');
    //jQuery('.popovers-hide').popover('hide');
    //jQuery('.popovers-toggle').popover('toggle');
    //jQuery('.popovers-destroy').popover('destroy');
  }

  return {
    init: function() {
      handleBootstrap();
    }
  }
}();
