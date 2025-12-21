function sendMessage() {
    const inputField = document.getElementById("user_message");
    const message = inputField.value;
    if (message.trim() !== "") {
        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'user_message=' + encodeURIComponent(message)
        })
        .then(response => {
            if (response.ok) {
                window.location.reload();  // Reload to see new message
            }
        })

    }
}