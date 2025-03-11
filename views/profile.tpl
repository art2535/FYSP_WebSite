% rebase('layout.tpl', title='User Profile', year=year)

<div class="jumbotron" style="background-color: orange; color: white; margin-top: 20px; padding: 20px; display: flex; flex-direction: column; justify-content: center; align-items: center; border-radius: 20px; text-align: center; width: 100%;">
    <div>
        <h1>{{ title }}</h1>
        <h3 class="mb-4">{{ message }}</h3>
    </div>
</div>

<div class="user-profile-container" style="padding: 20px; max-width: 1000px; margin: 0 auto;">
    <div style="display: flex; align-items: center; margin-bottom: 30px;">
        <div style="background-color: #f5f5f5; border-radius: 50%; width: 80px; height: 80px; display: flex; justify-content: center; align-items: center; margin-right: 20px; position: relative;">
            <img src="/static/resources/logo.png" alt="Profile Picture" style="width: 50px; height: 50px;">
            <label for="avatar-upload" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 50%; background-color: rgba(0,0,0,0.3); display: flex; justify-content: center; align-items: center; cursor: pointer; opacity: 0; transition: opacity 0.2s ease;">
                <img src="/static/resources/camera-icon.png" alt="Change Photo" style="width: 24px; height: 24px; filter: brightness(0) invert(1);">
            </label>
            <input type="file" id="avatar-upload" name="avatar" accept="image/*" style="display: none;">
        </div>
        <div>
            <h2 style="margin: 0; font-size: 24px;">User name</h2>
            <p style="margin: 5px 0 0; color: #777;">Registration date: 18.09.2020</p>
        </div>
    </div>

    <div style="display: flex; flex-wrap: wrap; gap: 20px;">
        <div style="flex: 1; min-width: 300px;">
            <div style="background-color: #f5f5f5; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
                <label for="firstName" style="display: block; color: #777; font-size: 14px; margin-bottom: 5px;">First name</label>
                <input type="text" id="firstName" name="firstName" value="firstName" style="width: 100%; border: none; background: transparent; font-size: 16px; padding: 0;">
            </div>

            <div style="background-color: #f5f5f5; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
                <label for="phone" style="display: block; color: #777; font-size: 14px; margin-bottom: 5px;">Phone</label>
                <input type="tel" id="phone" name="phone" value="+7 000 000-00-00" style="width: 100%; border: none; background: transparent; font-size: 16px; padding: 0;">
            </div>

            <div style="background-color: #f5f5f5; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
                <label for="nickname" style="display: block; color: #777; font-size: 14px; margin-bottom: 5px;">Nickname</label>
                <input type="text" id="nickname" name="nickname" value="nickName" style="width: 100%; border: none; background: transparent; font-size: 16px; padding: 0;">
            </div>
        </div>

        <div style="flex: 1; min-width: 300px;">
            <div style="background-color: #f5f5f5; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
                <label for="lastName" style="display: block; color: #777; font-size: 14px; margin-bottom: 5px;">Last name</label>
                <input type="text" id="lastName" name="lastName" value="lastName" style="width: 100%; border: none; background: transparent; font-size: 16px; padding: 0;">
            </div>

            <div style="background-color: #f5f5f5; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
                <label for="email" style="display: block; color: #777; font-size: 14px; margin-bottom: 5px;">Email</label>
                <input type="email" id="email" name="email" value="example@gmail.com" style="width: 100%; border: none; background: transparent; font-size: 16px; padding: 0;">
            </div>

            <div style="background-color: #f5f5f5; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
                <label for="birthdate" style="display: block; color: #777; font-size: 14px; margin-bottom: 5px;">Date of birth</label>
                <input type="date" id="birthdate" name="birthdate" value="1990-01-01" style="width: 100%; border: none; background: transparent; font-size: 16px; padding: 0;">
            </div>
        </div>
    </div>

    <div style="margin-top: 20px; display: flex; justify-content: space-between;">
        <div style="display: flex;">
            <button type="submit" onclick="alert('Данные успешно сохранены')" style="background-color: #FF8C00; border: none; cursor: pointer; color: white; font-size: 14px; font-weight: 500; margin-right: 20px; padding: 8px 15px; border-radius: 5px;">
                Save changed
            </button>
            <a onclick="alert('Пароль успешно изменен')" style="background-color: #FF8C00; border: none; cursor: pointer; color: white; font-size: 14px; text-decoration: none; padding: 8px 15px; border-radius: 5px; display: inline-block;">
                Change password
            </a>
        </div>
        <div>
            <a href="/logout" style="background-color: #FF8C00; border: none; display: flex; align-items: center; cursor: pointer; color: white; font-size: 14px; text-decoration: none; padding: 8px 15px; border-radius: 5px;">
                <span style="margin-right: 5px;">↩</span> Logout
            </a>
        </div>
    </div>
</div>
