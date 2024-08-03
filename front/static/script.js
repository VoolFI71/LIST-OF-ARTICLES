async function fetchLoginPage() {
    try {
        const request = await fetch('/user/login', {
            method: 'GET',
            credentials: 'include'  // Включает cookie в запрос
        });

        if (request.ok) {
            const cookies = document.cookie; // Получаем все cookie
            if (cookies[0]+cookies[1]+cookies[2] != "jwt"){
                const contentDiv = document.getElementById('content');
                contentDiv.innerHTML = cookies;
            }
        } else {
            console.log(33)
        }

    } catch (error) {
        console.error('Ошибка:', error);
    }
}

fetchLoginPage();
