async function sendCookie() {
    const ws = new WebSocket("ws://localhost:8000/ws");
    await new Promise((resolve) => {
        ws.onopen = function(e) {
            resolve();
        };
        });
    ws.send(document.cookie);
}

async function deleteToken() {
    const cookieName = 'jwt';
    document.cookie = cookieName + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;';
    const currentUrl = window.location.href;
    const url = new URL(currentUrl);
    window.location.href = url;
}

