function orderProduct(productName) {
    const modal = document.getElementById("orderModal");
    const message = document.getElementById("orderMessage");
    const closeBtn = document.querySelector(".modal-close");

    message.textContent = `Product “${productName}” has been added to the cart!`;
    modal.style.display = "block";

    closeBtn.onclick = () => {
        modal.style.display = "none";
    };

    window.onclick = (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };
}
