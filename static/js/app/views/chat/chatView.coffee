define ['marionette', 'app.lib/realtimeController', 'text!/tpl/ChatView'],
(Marionette, RealtimeController, Template) ->
    class ChatView extends Marionette.ItemView
        controller = new RealtimeController()
        template: _.template(Template)
        ui:
            chatMessage: '#chat-message'

        events:
            "click #chat-send": "sendChatMessage"

        sendChatMessage: ->
            console.log("ChatView: sendChatMessage")
            message = @ui.chatMessage.val()
            if message
                controller.sendMessage(message)

    ChatView