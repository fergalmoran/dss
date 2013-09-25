define ['jquery', 'underscore', 'marionette', 'vent',
        'text!/tpl/SearchView', 'text!/tpl/SearchResultView',
        'lib/bootstrap-typeahead'],
($, _, Marionette, vent, Template, SearchResultView) ->
    class SearchView extends Marionette.CompositeView
        template: _.template(Template)

        ui:
            searchText: '#search-text'

        engine:
            compile: (template) ->
                compiled = _.template(template)
                render: (context) ->
                    compiled context

        onShow: ->
            if typeahead?
                t = $('#search-text', @el).typeahead
                    name: "search"
                    engine: @engine
                    valueKey: "title"
                    template: SearchResultView
                    remote:
                        url: "/api/v1/mix/search?q=%QUERY"
                        dataType: "json"
                        filter: (parsedResponse)->
                            parsedResponse.objects

                $('.tt-hint', @el).addClass('search-query');
                $('.tt-hint', @el).addClass('span3');

                t.on 'typeahead:selected': (event, datum, dataset_name) ->
                    vent.trigger 'navigate:mix', datum.slug
                    $('#search-text', @el).blur()
                    $('.tt-hint', @el).blur()
            else
                console.log("Typeahead disabled")

    SearchView