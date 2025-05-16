% rebase('layout.tpl', title='User Profile', year=year)

<link rel="stylesheet" href="/static/content/page_styles/styles_profile.css">

<div class="jumbotron orange-banner">
    <div>
        <h1>{{ title }}</h1>
        <h3 class="mb-4">{{ message }}</h3>
    </div>
</div>

<div class="user-profile-container">
    <div class="user-header">
        <div class="avatar-container">
            <img src="/static/resources/logo.png" alt="Profile Picture" class="avatar-img">
            <label for="avatar-upload" class="avatar-overlay">
                <img src="/static/resources/camera-icon.png" alt="Change Photo" class="camera-icon">
            </label>
            <input type="file" id="avatar-upload" name="avatar" accept="image/*" style="display: none;">
        </div>
        <div>
            <h2 class="username">User name</h2>
            <p class="reg-date">Registration date: 18.09.2020</p>
        </div>
    </div>

    <div class="form-columns">
        <div class="form-column">
            <div class="form-field">
                <label for="firstName">First name</label>
                <input type="text" id="firstName" name="firstName" value="firstName">
            </div>
            <div class="form-field">
                <label for="phone">Phone</label>
                <input type="tel" id="phone" name="phone" value="+7 000 000-00-00">
            </div>
            <div class="form-field">
                <label for="nickname">Nickname</label>
                <input type="text" id="nickname" name="nickname" value="nickName">
            </div>
        </div>

        <div class="form-column">
            <div class="form-field">
                <label for="lastName">Last name</label>
                <input type="text" id="lastName" name="lastName" value="lastName">
            </div>
            <div class="form-field">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" value="example@gmail.com">
            </div>
            <div class="form-field">
                <label for="birthdate">Date of birth</label>
                <input type="date" id="birthdate" name="birthdate" value="1990-01-01">
            </div>
        </div>
    </div>

    <div class="button-group">
        <div class="left-buttons">
            <button type="submit" onclick="alert('Данные успешно сохранены')">Save changed</button>
            <a onclick="alert('Пароль успешно изменен')">Change password</a>
        </div>
        <div class="right-button">
            <a href="/logout"><span>↩</span> Logout</a>
        </div>
    </div>
</div>