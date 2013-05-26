define ['app', 'marionette', 'text!/tpl/UserListItemView'],
(App, Marionette, Template)->
    class UserItemView extends Marionette.ItemView
        template: _.template(Template)
        tagName: "tr"
