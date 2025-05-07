% rebase('layout.tpl', title=title, year=year)

<h1 style="margin-bottom: 20px;">Partner companies</h1>

<div style="display: flex; gap: 50px; align-items: flex-start;">
    <form action="/add" method="post" enctype="multipart/form-data" style="max-width: 600px;">

        <div style="background-color: #f5f5f5; border-radius: 10px; padding: 15px; margin-bottom: 15px;">
            <label for="name" style="display: block; color: #777; font-size: 14px; margin-bottom: 5px;">Name</label>
            <input type="text" id="name" name="name" value="{{form_data.get('name', '')}}" placeholder="Enter company name"
                   style="width: 100%; border: none; background: transparent; font-size: 16px;" required>
            % if errors.get('name'):
                <div class="error">{{errors['name']}}</div>
            % end
        </div>

        <div style="background-color: #f5f5f5; border-radius: 10px; padding: 15px; margin-bottom: 15px;">
            <label for="description" style="display: block; color: #777; font-size: 14px; margin-bottom: 5px;">Description</label>
            <textarea id="description" name="description" placeholder="Enter description"
                      style="width: 100%; border: none; background: transparent; font-size: 16px;" required>{{form_data.get('description', '')}}</textarea>
            % if errors.get('description'):
                <div class="error">{{errors['description']}}</div>
            % end
        </div>

        <div style="background-color: #f5f5f5; border-radius: 10px; padding: 15px; margin-bottom: 15px;">
            <label for="phone" style="display: block; color: #777; font-size: 14px; margin-bottom: 5px;">Phone</label>
            <input type="text" id="phone" name="phone" placeholder="+7(XXX)XXX-XX-XX" value="{{form_data.get('phone', '')}}"
                   style="width: 100%; border: none; background: transparent; font-size: 16px;" required>
            % if errors.get('phone'):
                <div class="error">{{errors['phone']}}</div>
            % end
        </div>

        <div style="background-color: #f5f5f5; border-radius: 10px; padding: 15px; margin-bottom: 15px;">
            <label for="date" style="display: block; color: #777; font-size: 14px; margin-bottom: 5px;">Date added</label>
            <input type="date" id="date" name="date" value="{{form_data.get('date', '')}}"
                   style="width: 100%; border: none; background: transparent; font-size: 16px;" required>
            % if errors.get('date'):
                <div class="error">{{errors['date']}}</div>
            % end
        </div>

        <div style="background-color: #f5f5f5; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
            <label for="logo" style="display: block; color: #777; font-size: 14px; margin-bottom: 5px;">Logo</label>
            <input type="file" id="logo" name="logo" accept="image/*"
                   style="width: 100%; border: none; background: transparent; font-size: 16px;">
            % if errors.get('logo'):
                <div class="error">{{errors['logo']}}</div>
            % end
        </div>

        <button type="submit" class="btn-submit" style="background-color: #FF8C00; border: none; cursor: pointer; color: white; font-size: 14px; font-weight: 500; padding: 8px 15px; border-radius: 5px;">Add</button>
    </form>

    <img src="/static/resources/logo.png" style="max-width: 300px;" alt="Logotype">
</div>

<hr>

<h2 style="margin-top: 40px;">Our partners</h2>
<ul style="list-style: none; padding: 0;">
    % for c in companies:
        <li style="margin-bottom: 25px; padding: 10px; border: 1px solid #ccc; border-radius: 8px;">
            <strong>{{c['name']}}</strong> ({{c['date']}})<br>
            {{c['description']}}<br>
            Contact: {{c['phone']}}<br>
            % if c.get('logo'):
                <img src="/logos/{{c['logo']}}" alt="Logo" style="max-height: 100px; margin-top: 5px;">
            % end
        </li>
    % end
</ul>