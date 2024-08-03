async function fetchLoginPage() {
    try {
        const request = await fetch('/user/login', {
            method: 'GET',
            credentials: 'include'  // Включает cookie в запрос
        });

        if (request.ok) {
            const cookies = document.cookie; // Получаем все cookie
            console.log(cookies); // Выводим все cookie в консоль
        } else {
            console.error('Ошибка при получении страницы:', request.status);
        }

    } catch (error) {
        console.error('Ошибка:', error);
    }
}

fetchLoginPage();
console.log(5555)