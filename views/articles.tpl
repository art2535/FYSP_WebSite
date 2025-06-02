% rebase('layout.tpl', title=title_page, year=year, current_page='articles')

<link rel="stylesheet" type="text/css" href="/static/content/page_styles/styles_articles.css">

<div class="constructor-header">
    <div class="constructor-header-text">
        <h2>Articles</h2>
        <p>Learn more about technologies and components.</p>
    </div>
    <img src="/static/resources/logo.png" alt="Article Logo" class="constructor-logo">
</div>

<div class="container article-container">

    <h2>Existing Articles</h2>
    <div class="row article-row">
        % if not articles:
            <p>No articles yet. Be the first to add one!</p>
        % else:
            % for i, article in enumerate(articles):
            <div class="col-md-6 article-item">
                <div class="card">
                    <div class="card-header">
                        <h3>{{ article.get('title', 'No Title') }}</h3>
                        <small>Author: {{ article.get('author', 'Unknown') }} | Date: {{ article.get('date', 'No Date') }}</small>
                    </div>
                    <div class="card-body">
                        <p>{{ article.get('text', 'No text.') }}</p>
                    </div>
                    <div class="card-footer">
                        % if article.get('link') and (article['link'].startswith('http://') or article['link'].startswith('https://')):
                            <a href="{{ article['link'] }}" target="_blank" class="btn btn-primary btn-delete">Go to Article</a>
                        % else:
                             <button type="button" class="btn btn-secondary btn-delete" disabled>Link Missing</button>
                        % end
                    </div>
                </div>
            </div>
            % # Исправленная строка: используем len(articles) для проверки последнего элемента
            % if (i + 1) % 2 == 0 and i < len(articles) - 1:
        </div>
        <div class="row article-row">
            % end
            % end
        % end
    </div>

    <hr class="my-4"> <div class="article-form-container">
        <h2>Add New Article</h2>
        <form action="/articles" method="post" class="article-form">
            <div class="form-group">
                <label for="title">Title:</label>
                <input type="text" id="title" name="title" class="form-control" value="{{ form_data.get('title', '') }}" required>
                % if 'title' in errors:
                <span class="error-message">{{ errors['title'] }}</span>
                % end
            </div>
            <div class="form-group">
                <label for="author">Author:</label>
                <input type="text" id="author" name="author" class="form-control" value="{{ form_data.get('author', '') }}" required>
                % if 'author' in errors:
                <span class="error-message">{{ errors['author'] }}</span>
                % end
            </div>
            <div class="form-group">
                <label for="text">Article Text:</label>
                <textarea id="text" name="text" class="form-control" required>{{ form_data.get('text', '') }}</textarea>
                % if 'text' in errors:
                <span class="error-message">{{ errors['text'] }}</span>
                % end
            </div>
            <div class="form-group">
                <label for="date">Publication Date:</label>
                <input type="date" id="date" name="date" class="form-control" value="{{ form_data.get('date', '') }}" required>
                % if 'date' in errors:
                <span class="error-message">{{ errors['date'] }}</span>
                % end
            </div>
            <div class="form-group">
                <label for="link">Article Link:</label>
                <input type="url" id="link" name="link" class="form-control" value="{{ form_data.get('link', '') }}" placeholder="https://example.com/article" required>
                % if 'link' in errors:
                <span class="error-message">{{ errors['link'] }}</span>
                % end
            </div>

            % if 'form' in errors:
            <div class="alert alert-danger" role="alert">
                {{ errors['form'] }}
            </div>
            % end
            <button type="submit" class="btn btn-submit">Add Article</button>
        </form>
    </div>
</div>