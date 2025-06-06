﻿<html lang="ru">
<head>
    % rebase('layout.tpl', title=title, year=year)
    <meta charset="UTF-8">
    <title>Reviews</title>
    <link rel="stylesheet" href="/static/content/page_styles/style_reviews.css"> <!-- Page styles -->
</head>
<body>

% if errors:
<div id="error-popup" class="error-popup">
    <button onclick="hideError()" class="close-btn">×</button>
    <ul>
    % for err in errors:
        <li>{{ err }}</li> <!-- Display validation errors -->
    % end
    </ul>
</div>
% end

<div class="jumbotron">
    <h1>Reviews</h1>
    <p class="lead">Leave a review about our products and company</p>
    <a class="leave-review-link" onclick="scrollToReviewForm()">Leave a review</a> <!-- Scroll to review form -->
</div>

<div class="filter-card">
    <div class="filter-section">
        <h2>Category</h2>
        <div class="filters category-filters">
            <!-- Category filter buttons -->
            <button class="filter-button {{ 'active' if filter_category == 'all' else '' }}" onclick="setFilter('all')">All</button>
            <button class="filter-button {{ 'active' if filter_category == 'product' else '' }}" onclick="setFilter('product')">About Product</button>
            <button class="filter-button {{ 'active' if filter_category == 'company' else '' }}" onclick="setFilter('company')">About Company</button>
        </div>
    </div>

    <div class="filter-section">
        <h2>Filtering by</h2>
        <div class="filters sort-filters">
            <!-- Sort order buttons -->
            <button class="filter-button {{ 'active' if sort_order == 'new' else '' }}" onclick="setSort('new')">Newest first</button>
            <button class="filter-button {{ 'active' if sort_order == 'old' else '' }}" onclick="setSort('old')">Oldest first</button>
        </div>
    </div>
</div>

<!-- Hidden form to submit filter params -->
<form id="filter-form" method="GET" action="/reviews">
    <input type="hidden" name="filter_category" id="filter_category" value="{{ filter_category or 'all' }}">
    <input type="hidden" name="sort_order" id="sort_order" value="{{ sort_order or '' }}">
</form>

<div class="reviews-container" id="reviewsContainer">
    % for review in reviews:
    <div class="review" data-category="{{ review['category'] }}" data-date="{{ review['date'] }}">
        <img src="{{ review['avatar_url'] }}" alt="Avatar" class="avatar"> <!-- User avatar -->
        <div class="review-content">
            <div class="top-info">
                <div class="review-header">
                    <div class="nickname">{{ review['nickname'] }}</div> <!-- Reviewer nickname -->
                    <div class="category">
                        {{ review['category'].capitalize() }}
                        % if review['category'] == 'product' and 'product_name' in review:
                            ({{ review['product_name'] }}) <!-- Show product name if product review -->
                        % end
                    </div>
                </div>
                <div class="stars">{{ '★' * review['rating'] }}{{ '☆' * (5 - review['rating']) }}</div> <!-- Star rating -->
            </div>
            <div class="text">
                {{ review['text'] }} <!-- Review text -->
            </div>
            <div class="date">{{ review['date'] }}</div> <!-- Review date -->
        </div>
    </div>
    % end
</div>

<div class="review-form" id="reviewForm">
    <h2>Add your review</h2>
    <form method="POST" action="/reviews">
    <div class="form-row">
        <input type="text" name="nickname" placeholder="Your nickname" required
               value="{{ form_data['nickname'] }}"> <!-- Nickname input -->
        <select name="category" id="category" required>
            <option value="company" {{ 'selected' if form_data['category'] == 'company' else '' }}>About company</option>
            <option value="product" {{ 'selected' if form_data['category'] == 'product' else '' }}>About product</option>
        </select> <!-- Category selector -->
        <input type="number" name="rating" max="5" min="1" placeholder="Rating (1-5)" required
               value="{{ form_data['rating'] }}"> <!-- Rating input -->
    </div>
    <div class="form-row product-row" id="product-field" style="display: {{ 'flex' if form_data['category'] == 'product' else 'none' }};">
        <select name="product_id" id="product-select" {{ 'required' if form_data['category'] == 'product' else '' }}>
            % for product in products:
                <option value="{{ product['id'] }}" {{ 'selected' if form_data['product_id'] == product['id'] else '' }}>
                    {{ product['name'] }}
                </option>
            % end
        </select> <!-- Product selector shown only for product reviews -->
    </div>
    <textarea name="text" rows="5" placeholder="Write your review..." required>{{ form_data['text'] }}</textarea> <!-- Review text area -->
    <button type="submit">Send feedback</button> <!-- Submit button -->
</form>
</div>

<script src="/static/scripts/work_elements_reviews.js"></script> <!-- JS for filters and form behavior -->

</body>
</html>
