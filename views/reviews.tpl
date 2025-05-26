reviews:
<html lang="ru">
<head>
    % rebase('layout.tpl', title=title, year=year)
    <meta charset="UTF-8">
    <title>Reviews</title>
    <link rel="stylesheet" href="/static/content/page_styles/style_reviews.css">
</head>
<body>

<div class="jumbotron">
    <h1>Reviews</h1>
    <p class="lead">Leave a review about our products and company</p>
</div>

<div class="filters">
    <button class="filter-button">All</button>
    <button class="filter-button">About product</button>
    <button class="filter-button">About company</button>
    <button class="filter-button">New ones first</button>
    <button class="filter-button">The old ones first</button>
    <a href="#" class="leave-review-link" onclick="scrollToReviewForm()">Leave a review</a>
</div>

<div class="reviews-container" id="reviewsContainer">
    % for review in reviews:
    <div class="review">
        <img src="{{ review['avatar_url'] }}" alt="Avatar" class="avatar">
        <div class="review-content">
            <div class="top-info">
                <div class="review-header">
                    <div class="nickname">{{ review['nickname'] }}</div>
                    <div class="category">
                        {{ review['category'].capitalize() }}
                        % if review['category'] == 'product' and 'product_name' in review:
                            ({{ review['product_name'] }})
                        % end
                    </div>
                </div>
                <div class="stars">{{ '★' * review['rating'] }}{{ '☆' * (5 - review['rating']) }}</div>
            </div>
            <div class="text">
                {{ review['text'] }}
            </div>
            <div class="date">{{ review['date'] }}</div>
        </div>
    </div>
    % end
</div>

<div class="review-form" id="reviewForm">
    <h2>Add your review</h2>
    <form method="POST" action="/reviews">
        <div class="form-row">
            <input type="text" name="nickname" placeholder="Your nickname" required>
            <select name="category" id="category" required>
                <option value="company">About company</option>
                <option value="product">About product</option>
            </select>
            <input type="number" name="rating" max="5" min="1" placeholder="Rating (1-5)" required>
        </div>
        <div class="form-row product-row" id="product-field" style="display: none;">
            <select name="product_id" id="product-select">
                % for product in products:
                    <option value="{{ product['id'] }}">{{ product['name'] }}</option>
                % end
            </select>
        </div>
        <textarea name="text" rows="5" placeholder="Write your review..." required></textarea>
        <button type="submit">Send feedback</button>
    </form>
</div>

<script>
    document.getElementById('category').addEventListener('change', function() {
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
</script>

</body>
</html>
