define ['marionette'],
(Marionette)->
    class GenericView extends Marionette.ItemView
        initialize: (options)->
            @template = _.template(options.template)

        true