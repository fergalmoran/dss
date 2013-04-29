/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */

window.SidebarViewUser = Backbone.View.extend({
    events: {
    },
    render: function () {
        ich.addTemplate('sidebaruser', this.template());
        var rendered = ich.sidebaruser(this.model.toJSON());
        $(this.el).html(rendered);
        return this;
    }
});
