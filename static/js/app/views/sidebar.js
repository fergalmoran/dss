/**
 * Created with PyCharm.
 * User: fergalm
 * Date: 08/08/12
 * Time: 22:10
 * To change this template use File | Settings | File Templates.
 */
window.SidebarView = Backbone.View.extend({
    initialize: function(){
        this.render();
    },
    render: function(){
        $(this.el).html(this.template());
        return this;
    }
});