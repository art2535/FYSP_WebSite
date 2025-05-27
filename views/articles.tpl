% rebase('layout.tpl', title=title_page, year=year)

<link rel="stylesheet" type="text/css" href="/static/content/page_styles/styles_articles.css">

<div class="constructor-header">
    <div class="constructor-header-text">
        <h2>Useful Articles</h2>
        <p>Explore insightful articles on PC building, components, and technology trends.</p>
    </div>
    <img src="/static/resources/logo.png" alt="Articles" class="constructor-logo">
</div>

<div class="container article-container">
    % if not articles:
        <div class="col-md-12">
            <p class="text-center">No articles available at the moment. Check back soon!</p>
        </div>
    % else:
        <div class="row">
        % for index, article in enumerate(articles):
            <div class="col-md-4 article-item">
                <div class="card">
                    <div class="card-header">
                        <h3>{{ article.get('title', 'No Title') }}</h3>
                        <small>By: {{ article.get('author', 'Anonymous') }} | Published: {{ article.get('date', 'No Date') }}</small>
                    </div>
                    <div class="card-body">
                        <p>{{ article.get('text', 'No content available.') }}</p>
                    </div>
                     <div class="card-footer">
                        <form action="/articles" method="post" style="display: inline;">
                            <input type="hidden" name="delete_index" value="{{ index }}">
                            <button type="submit" class="btn-delete" onclick="return confirm('Are you sure you want to delete this article?');">Delete</button>
                        </form>
                    </div>
                </div>
            </div>
            % if (index + 1) % 3 == 0 and index != len(articles) - 1:
                </div><div class="row article-row">
            % end
        % end
        </div>
    % end
</div>

<hr>

<div class="container article-form-container">
    <h2>Add New Article</h2>
    % if errors and 'form' in errors:
        <div class="alert alert-danger">{{ errors['form'] }}</div>
    % end
    <form action="/articles" method="post" class="article-form">
        <div class="form-group">
            <label for="title">Title:</label>
            <input type="text" id="title" name="title" class="form-control" value="{{ form_data.get('title', '') }}" required>
            % if errors and 'title' in errors:
                <span class="error-message">{{ errors['title'] }}</span>
            % end
        </div>

        <div class="form-group">
            <label for="author">Author:</label>
            <input type="text" id="author" name="author" class="form-control" value="{{ form_data.get('author', '') }}" required>
            % if errors and 'author' in errors:
                <span class="error-message">{{ errors['author'] }}</span>
            % end
        </div>

        <div class="form-group">
            <label for="text">Text:</label>
            <textarea id="text" name="text" class="form-control" rows="5" required>{{ form_data.get('text', '') }}</textarea>
            % if errors and 'text' in errors:
                <span class="error-message">{{ errors['text'] }}</span>
            % end
        </div>

        <div class="form-group">
            <label for="date">Date:</label>
            <input type="date" id="date" name="date" class="form-control" value="{{ form_data.get('date', '') }}" required>
            % if errors and 'date' in errors:
                <span class="error-message">{{ errors['date'] }}</span>
            % end
        </div>

        <button type="submit" class="btn btn-primary btn-submit">Submit Article</button>
    </form>
</div>