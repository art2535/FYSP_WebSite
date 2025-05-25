% rebase('layout.tpl', title='Latest Arrivals', year=year)
<link rel="stylesheet" href="/static/content/page_styles/styles_new_products.css">

<div class="jumbotron constructor-header">
    <div class="constructor-header-text">
        <h1>Latest Products</h1>
        <p class="lead">Newest products and trends in the tech world</p>
    </div>
    <img src="/static/resources/logo.png" alt="New Products Logo" class="constructor-logo">
</div>

<div class="container">
    <div class="card-container">
        % from datetime import datetime
        % now = datetime.now().date()
        % for index, item in enumerate(new_products):
            % item_date = datetime.strptime(item['date'], '%Y-%m-%d').date()
            % is_future = item_date > now
            <div class="card news-item">
                <div class="card-header">
                    <h3>{{item['author']}}</h3>
                    <small>{{item['date']}}</small>
                </div>
                <div class="card-body">
                    <p>{{item['text']}}</p>
                    <form method="post" class="delete-form" style="display:inline;">
                        <input type="hidden" name="delete_index" value="{{index}}">
                        <button type="submit" class="btn-delete">Delete</button>
                    </form>
                    <button onclick="orderProduct('{{item['author']}}')" class="btn-order">
                        {{'Pre-order' if is_future else 'Order'}}
                    </button>
                </div>
            </div>
        % end
    </div>

    <hr>

    <form method="post" class="news-form">
        <h2>Add a New Product</h2>
        % if error:
            <div class="form-error">{{!error}}</div>
        % end
        <div class="form-group">
            <label for="author">Brand / Product Name *</label>
            <input type="text" name="author" id="author" class="form-control" value="{{author or ''}}" required>
        </div>
        <div class="form-group">
            <label for="text">Description *</label>
            <textarea name="text" id="text" class="form-control" required>{{text or ''}}</textarea>
        </div>
        <div class="form-group">
            <label for="date">Date (YYYY-MM-DD) *</label>
            <input type="date" name="date" id="date" class="form-control" value="{{date or ''}}" required>
        </div>
        <button type="submit" class="btn-submit">Submit</button>
    </form>
</div>

<script src="/static/scripts/new_products.js"></script>
