document.getElementById('category').addEventListener('change', function () {
    const productField = document.getElementById('product-field');
    if (this.value === 'product') {
        productField.style.display = 'flex';
        document.getElementById('product-select').setAttribute('required', 'required');
    } else {
        productField.style.display = 'none';
        document.getElementById('product-select').removeAttribute('required');
    }
});

function scrollToReviewForm() {
    document.getElementById('reviewForm').scrollIntoView({ behavior: 'smooth' });
}

function hideError() {
    const popup = document.getElementById('error-popup');
    if (popup) {
        popup.style.display = 'none';
    }
}

function setFilter(category) {
    document.getElementById('filter_category').value = category;
    document.getElementById('sort_order').value = ''; // Reset sort when changing filter
    document.getElementById('filter-form').submit();
}

function setSort(order) {
    document.getElementById('sort_order').value = order;
    document.getElementById('filter-form').submit();
}
