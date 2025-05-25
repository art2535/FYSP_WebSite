% rebase('layout.tpl', title=title, year=year)
<link rel="stylesheet" href="/static/content/page_styles/styles_partners.css">

<h1>Partner Companies</h1>

<div class="partner-form-container">
    <form action="/add" method="post" enctype="multipart/form-data">
        <div class="form-group">
            <label for="name">Name</label>
            <input type="text" id="name" name="name" value="{{form_data.get('name', '')}}" placeholder="Enter company name" required>
            % if errors.get('name'):
                <div class="error-message">{{errors['name']}}</div>
            % end
        </div>

        <div class="form-group">
            <label for="description">Description</label>
            <textarea id="description" name="description" placeholder="Enter description" required>{{form_data.get('description', '')}}</textarea>
            % if errors.get('description'):
                <div class="error-message">{{errors['description']}}</div>
            % end
        </div>

        <div class="form-group">
            <label for="phone">Phone</label>
            <input type="text" id="phone" name="phone" placeholder="+7(XXX)XXX-XX-XX" value="{{form_data.get('phone', '')}}" required>
            % if errors.get('phone'):
                <div class="error-message">{{errors['phone']}}</div>
            % end
        </div>

        <div class="form-group">
            <label for="date">Date Added</label>
            <input type="date" id="date" name="date" value="{{form_data.get('date', '')}}" required>
            % if errors.get('date'):
                <div class="error-message">{{errors['date']}}</div>
            % end
        </div>

        <div class="form-group">
            <label for="logo">Logo</label>
            <input type="file" id="logo" name="logo" accept="image/*">
            % if errors.get('logo'):
                <div class="error-message">{{errors['logo']}}</div>
            % end
        </div>

        <button type="submit" class="btn-submit">Add</button>
    </form>

    <img src="/static/resources/logo.png" alt="Logotype" class="partner-logo">
</div>

<hr>

<h2>Our Partners</h2>
<ul class="partner-list">
    % for c in companies:
        <li class="partner27">
            <div class="partner-info">
                <strong>{{c['name']}}</strong> ({{c['date']}})<br>
                {{c['description']}}<br>
                Contact: {{c['phone']}}<br>
            </div>
            % if c.get('logo'):
                <div class="partner-logo-wrapper">
                    <img src="/static/resources/logos/{{c['logo']}}" alt="Logo" class="company-logo">
                </div>
            % end
        </li>
    % end
</ul>