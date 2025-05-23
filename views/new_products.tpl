% rebase('layout.tpl', title='Актуальные новинки', year=year)

<link rel="stylesheet" href="/static/content/page_styles/styles_new_products.css">

<div class="jumbotron constructor-header">
    <div class="constructor-header-text">
        <h1>Актуальные новинки</h1>
        <p class="lead">Последние поступления и тренды компьютерного мира</p>
    </div>
    <img src="/static/resources/logo.png" alt="Логотип новинок" class="constructor-logo">
</div>

<div class="container">
    <div class="card-container">
        % for item in new_products:
            <div class="card news-item">
                <div class="card-header">
                    <h3>{{item['author']}}</h3>
                    <small>{{item['date']}}</small>
                </div>
                <div class="card-body">
                    <p>{{item['text']}}</p>
                </div>
            </div>
        % end
    </div>

    <hr>

    <form method="post" class="news-form">
        <h2>Добавить новинку</h2>
        % if error:
            <div class="form-error">{{!error}}</div>
        % end
        <div class="form-group">
            <label for="author">Автор / Название *</label>
            <input type="text" name="author" id="author" class="form-control" value="{{author or ''}}" required>
        </div>
        <div class="form-group">
            <label for="text">Описание *</label>
            <textarea name="text" id="text" class="form-control" required>{{text or ''}}</textarea>
        </div>
        <div class="form-group">
            <label for="date">Дата (ГГГГ-ММ-ДД) *</label>
            <input type="date" name="date" id="date" class="form-control" value="{{date or ''}}" required>
        </div>
        <button type="submit" class="btn-submit">Разместить</button>
    </form>
</div>
