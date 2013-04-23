/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */

window.SidebarViewUser = Backbone.View.extend({
    events: {
    },
    initialize: function () {
        this.render();
    },
    render: function () {
        $(this.el).html(this.template({"item":this.model.toJSON()}));
        return this;
    }
});