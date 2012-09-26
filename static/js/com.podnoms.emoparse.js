$(function(){

    // Load an Adium Emoticonset.
    function emo_set_load( emoticon_set, callback ) {
        var emoticons_base = '../../shared/emoticons/' + emoticon_set + '/',
            obj = {};

        // For some reason, jQuery's :contains doesn't seem to work when parsing XML in IE.
        function contains( text ) {
            return function() {
                return ( this.textContent || this.text || '' ).indexOf( text ) !== -1;
            }
        };

        $.ajax({
            // The web server must be configured to serve .plist files as text/xml!
            dataType: 'xml',

            // The XML file that defines the Adium Emoticonset.
            url: emoticons_base + 'Emoticons.plist',

            // Parse Adium Emoticonset .plist file.
            success: function( data, textStatus ){
                $(data).find( 'plist > dict > dict > key' ).each(function(){

                    var that = $(this),
                        image = that.text(),
                        equivalents = that.next().children().filter( contains('Equivalents') ).next().children(),
                        name = that.next().children( 'key' ).filter( contains('Name') ).next().text(),
                        text,
                        arr = [];

                    debug.log( image, equivalents.length, name );

                    equivalents.each(function(){
                        text = $(this).text();
                        text && arr.push( text );
                    });

                    obj[ arr.shift() ] = [ emoticons_base + image, name ].concat( arr );
                });

                // Overwrite all current emoticons with those in the Emoticonset.
                callback( emotify.emoticons( true, obj ) );
            },

            // Oops?
            error: function() {
                callback( false );
            }
        });
    };

    // When an Adium Emoticonset is loaded, update the page.
    function emo_set_onload( emoticons ) {
        if ( !emoticons ) {
            debug.log( 'Error loading emoticons!' );
            return;
        }

        // Let's override the "cowboy" smiley with something a little sexier :D
        emotify.emoticons({
            "<):)": [ "../../shared/cowboy.png", "cowboy" ]
        });

        // Generate "emoticons key" table for this example.
        var html = '',
            cols = 7,
            i = -1;

        $.each( emotify.emoticons(), function(k,v){
            i++;
            html += i % cols == 0 ? '<tr>' : '';
            html += '<td class="key1">' + k + '<\/td><td class="key2">' + emotify( k ) + '<\/td>';
            html += i % cols == cols - 1 ? '<\/tr>' : '';
        });

        while ( ++i % cols ) {
            html += '<td class="key3" colspan="2"><\/td>';
        }

        $('#key').html( '<table>' + html + '<\/table>' );

        // Redraw the output.
        $('textarea').keyup();
    };

    // When the textarea changes, update the output!
    $('textarea')
        .keyup(function(){
            var text = $(this).val(),
                html = emotify( text );

            $('#output').html( html.replace( /\n/g, "<br/>" ) );

        })
        .keyup();

    // When the select changes, load an Adium Emoticonset!
    $('#choose')
        .change(function(){
            emo_set_load( $(this).val(), emo_set_onload );
        })
        .change();

});
