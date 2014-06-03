/**
 *
 * See websocket_driver.py for protocol
 * Entry point is AsyncChat
 *
 */

function _processRequests(peopleInChat, consoleBlock, formBlock, inputSocket, outputSocket) {
    var nick = prompt("Enter nick");
    var inputBox = formBlock.find("#input_box");
    formBlock.submit(function (event) {
        outputSocket.send(inputBox.val());
        event.preventDefault();
        inputBox.val("");
        return false;
    });

    outputSocket.onmessage = function (message) {
        var parsedMessage = JSON.parse(message.data);
        var messageType = parsedMessage.message;
        switch (messageType) {
            case "add":
            {
                peopleInChat.text(parsedMessage.text);
                break;
            }
            case "remove":
            {
                break; // TODO: Implement
            }
            case "get_nick":
            {
                outputSocket.send(nick);
                break; // TODO: Implement
            }
            default: // Text
            {
                $("<li></li>").text(parsedMessage.text).appendTo(consoleBlock);
                var lines = consoleBlock.children("li");
                if (lines.length > 10) {
                    lines[0].remove();
                }
            }
        }
    };
    inputSocket.onmessage = outputSocket.onmessage;
}

/**
 *
 * @param peopleInChat jQuery element with list of people in chat
 * @param consoleBlock jQuery element with list of messages
 * @param formBlock jQueryElement with form with input_box and submit button
 * @param ip your ip
 */
function AsyncChat(peopleInChat, consoleBlock, formBlock, ip) {
    var nConnectedSockets = 0;

    var inputSocket = new WebSocket("ws://" + ip + ":2346/");
    var outputSocket = new WebSocket("ws://" + ip + ":2345/");

    function connectionOpened() {
        if (++nConnectedSockets == 2) {
            _processRequests(peopleInChat, consoleBlock, formBlock, inputSocket, outputSocket);
        }
    }

    function connectionClosed() {
        alert("Connection lost");
        location.reload();
    }

    inputSocket.onopen = connectionOpened;
    outputSocket.onopen = connectionOpened;

    inputSocket.onclose = connectionClosed;
    outputSocket.onclose = connectionClosed;
}
