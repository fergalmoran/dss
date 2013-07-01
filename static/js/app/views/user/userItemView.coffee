define ['app', 'moment', 'marionette', 'text!/tpl/UserListItemView'],
(App, moment, Marionette, Template)->
    class UserItemView extends Marionette.ItemView
        template: _.template(Template)
        tagName: "tr"

        templateHelpers:
            humanise: (date)->
                moment(date).fromNow()
