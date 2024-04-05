const ownerColor = 'red';
const guestColor = 'blue';
const ownerUserId = 'owner@email.com';
const guestUserId = 'guest@email.com';
const userId = '';
const defaultColor = 'gray';

/**
 * Determines the color to use for messages based on the user's ID.
 * @param {string} userId - The ID of the user for whom to determine the message color.
 * @returns {string} - The color associated with the user, or the default color if no specific association exists.
 */
function getColorForUser(userId) {
    if (userId === ownerUserId) {
        return ownerColor;
    }
    else if (userId === guestUserId) {
        return guestColor;
    }
    return defaultColor;
}

// Initializes and manages the chat functionality
$(function() {
    var socket = io.connect('https://' + document.domain + ':' + location.port + '/chat');

    socket.on('connect', function() {
        socket.emit('joined', {});
    });

    socket.on('status', function(data) {
        let tag = document.createElement("p");
        let text = document.createTextNode(data.msg);
        tag.appendChild(text);
        tag.className = 'message-right';
        let color = getColorForUser(data.userId);
        tag.style.color = color;
        let element = document.getElementById("chat");
        element.appendChild(tag);
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });

    socket.on('message', function(data) {
        let color = getColorForUser(data.userId);
        let msgElement = $('<div>').text(data.msg).css('color', color);
        $('#chat').append(msgElement);
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });

    $('#sendButton').click(function() {
        socket.emit('text', {msg: $('#messageInput').val()});
        $('#messageInput').val('');
    });

    $('#messageInput').keypress(function(e) {
        if (e.which == 13) {  // Enter key
            socket.emit('text', {msg: $('#messageInput').val()});
            $('#messageInput').val('');
        }
    });

    $('#leaveButton').click(function() {
        socket.emit('left');
        window.location.href = '/';
    });
});
