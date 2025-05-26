% rebase('layout.tpl', title='Latest Arrivals', year=year)
<link rel="stylesheet" href="/static/content/page_styles/styles_new_products.css">

<!-- Заголовок страницы с логотипом -->
<div class="jumbotron constructor-header">
    <div class="constructor-header-text">
        <h1>New Products</h1>
        <p class="lead">Newest products and trends in the tech world</p>
    </div>
    <img src="/static/resources/logo.png" alt="New Products Logo" class="constructor-logo">
</div>

<!-- Основной контейнер страницы -->
<div class="container">

    <!-- Блок с карточками новостей -->
    <div class="card-container">
        % for index, item in enumerate(new_products):
            <!-- Карточка одной новости -->
            <div class="card news-item">
                <!-- Заголовок карточки: бренд и дата -->
                <div class="card-header">
                    <h3>{{item['author']}}</h3>
                    <small>{{item['date']}}</small>
                </div>

                <!-- Тело карточки: описание, изображение, кнопки -->
                <div class="card-body">
                    <div class="card-text">
                        <p>{{item['text']}}</p>
                    </div>
                    % if item.get('image'):
                        <!-- Изображение продукта, если указано -->
                        <div class="product-image">
                            <img src="/static/resources/{{item['image']}}" alt="Product Image">
                        </div>
                    % end

                    <!-- Кнопки "Delete" и "Order / Pre-order" -->
                    <div class="button-group">
                        <form method="post" class="delete-form" style="display:inline;">
                            <input type="hidden" name="delete_index" value="{{index}}">
                            <button type="submit" class="btn-delete">Delete</button>
                        </form>
                        <button onclick="orderProduct('{{item['author']}}')" class="btn-order">
                            {{item['order_label']}}
                        </button>
                    </div>
                </div>
            </div>
        % end
    </div>

    <hr>

    <!-- Форма добавления новой новости -->
    <form method="post" class="news-form">
        <h2>Add a New Product</h2>

        <!-- Поле: Автор / Название бренда -->
        <div class="form-group">
            <label for="author">Brand / Product Name *</label>
            <input type="text" name="author" id="author" class="form-control" value="{{author or ''}}" required>
            % if errors.get('author'):
                <div class="form-error">{{errors['author']}}</div>
            % end
        </div>

        <!-- Поле: Описание -->
        <div class="form-group">
            <label for="text">Description *</label>
            <textarea name="text" id="text" class="form-control" required>{{text or ''}}</textarea>
            % if errors.get('text'):
                <div class="form-error">{{errors['text']}}</div>
            % end
        </div>

        <!-- Поле: Дата публикации -->
        <div class="form-group">
            <label for="date">Date (YYYY-MM-DD) *</label>
            <input type="date" name="date" id="date" class="form-control" value="{{date or ''}}" required>
            % if errors.get('date'):
                <div class="form-error">{{errors['date']}}</div>
            % end
        </div>

        <!-- Поле: Выбор изображения -->
        <div class="form-group">
            <label for="image">Choose an Image (optional)</label>
            <select name="image" id="image" class="form-control-image">
                <option value="">-- No Image --</option>
                % for img in images:
                    <option value="{{img}}" {{'selected' if image == img else ''}}>{{img}}</option>
                % end
            </select>
        </div>

        <!-- Кнопка отправки формы -->
        <button type="submit" class="btn-submit">Submit</button>
    </form>
</div>

<!-- Скрипт страницы -->
<script src="/static/scripts/new_products.js"></script>
