$(document).ready(function() {

  const username = $('#userID').text();
  console.log(username)
  const socket = io({ query: "username=" + username, transports: ['websocket', 'polling'] });

  const form = $('#form');
  var input = $('#input');
  var recipientInput = $('#recipient');
  var messagesContainer = $('#messages');

  socket.on('connect', function() {
  console.log('Connected to server');
  });

  socket.on('message', function(data) {
    var messageElement = $('<div class="message">').addClass(data.sender === username ? 'sent' : 'received');
    var messageContent = $('<div class="message-content">').text(data.sender + ': ' + data.message);
    
    messageElement.append(messageContent);
    messagesContainer.append(messageElement);
    messagesContainer.scrollTop(messagesContainer.prop("scrollHeight"));
  });

  form.on('submit', function(e) {
    e.preventDefault();
    var message = input.val();
    var recipient = recipientInput.val();
    var sender = username;
    socket.emit('private_message', { sender: sender, recipient: recipient, message: message });
    input.val('');
  });



});