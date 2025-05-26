// Функция для обработки нажатия кнопки "Order" или "Pre-order"
function orderProduct(productName) {
    // Получаем модальное окно по ID
    const modal = document.getElementById("orderModal");

    // Получаем элемент для отображения сообщения внутри модального окна
    const message = document.getElementById("orderMessage");

    // Получаем кнопку закрытия модального окна
    const closeBtn = document.querySelector(".modal-close");

    // Устанавливаем текст сообщения с названием продукта
    message.textContent = `Product “${productName}” has been added to the cart!`;

    // Показываем модальное окно, устанавливая стиль display в "block"
    modal.style.display = "block";

    // При нажатии на кнопку закрытия — скрываем модальное окно
    closeBtn.onclick = () => {
        modal.style.display = "none";
    };

    // Если пользователь кликнул вне модального окна — тоже скрываем его
    window.onclick = (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };
}
