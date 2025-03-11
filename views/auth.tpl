% rebase('layout.tpl', title=title, year=year)

<div class="jumbotron" style="background-color: orange; color: white; margin-top: 20px; padding: 20px; display: flex; flex-direction: column; justify-content: center; align-items: center; border-radius: 20px; text-align: center; width: 100%;">
    <div>
        <h1>{{ title }}</h1>
        <h3 class="mb-4">{{ message }}</h3>
    </div>
</div>

<div class="user-profile-container" style="padding: 20px; max-width: 1000px; margin: 0 auto;">
    <div class="card shadow-sm" style="border-radius: 20px; padding: 20px; background-color: #fff;">
        <div class="row">
            <!-- Registration Form -->
            <div class="col-md-6" style="padding: 20px;">
                <h4 class="mb-3 text-center" style="font-size: 28px; margin-top: -10px;">Register</h4>
                <form method="POST" action="/register">
                    <div style="background-color: #f5f5f5; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
                        <label for="reg_firstname" style="display: block; color: #777; font-size: 14px; margin-bottom: 5px;">First Name</label>
                        <input type="text" id="reg_firstname" name="firstname" placeholder="Enter first name" style="width: 100%; border: none; background: transparent; font-size: 16px; padding: 0;" required>
                    </div>
                    <div style="background-color: #f5f5f5; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
                        <label for="reg_lastname" style="display: block; color: #777; font-size: 14px; margin-bottom: 5px;">Last Name</label>
                        <input type="text" id="reg_lastname" name="lastname" placeholder="Enter last name" style="width: 100%; border: none; background: transparent; font-size: 16px; padding: 0;" required>
                    </div>
                    <div style="background-color: #f5f5f5; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
                        <label for="reg_email" style="display: block; color: #777; font-size: 14px; margin-bottom: 5px;">Email</label>
                        <input type="email" id="reg_email" name="email" placeholder="Enter email" style="width: 100%; border: none; background: transparent; font-size: 16px; padding: 0;" required>
                    </div>
                    <div style="background-color: #f5f5f5; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
                        <label for="reg_phone" style="display: block; color: #777; font-size: 14px; margin-bottom: 5px;">Phone Number</label>
                        <input type="tel" id="reg_phone" name="phone" placeholder="Enter phone number" style="width: 100%; border: none; background: transparent; font-size: 16px; padding: 0;" required>
                    </div>
                    <div style="background-color: #f5f5f5; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
                        <label for="reg_birthdate" style="display: block; color: #777; font-size: 14px; margin-bottom: 5px;">Date of Birth</label>
                        <input type="date" id="reg_birthdate" name="birthdate" style="width: 100%; border: none; background: transparent; font-size: 16px; padding: 0;" required>
                    </div>
                    <div class="d-flex justify-content-center mt-3">
                        <button type="submit" style="background-color: #FF8C00; border: none; cursor: pointer; color: white; font-size: 14px; font-weight: 500; padding: 8px 15px; border-radius: 5px;">Register</button>
                    </div>
                </form>
            </div>
            <!-- Login Form -->
            <div class="col-md-6" style="padding: 20px;">
                <h4 class="mb-3 text-center" style="font-size: 28px; margin-top: -10px;">Login</h4>
                <form method="POST" action="/login">
                    <div style="background-color: #f5f5f5; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
                        <label for="login_username" style="display: block; color: #777; font-size: 14px; margin-bottom: 5px;">Username</label>
                        <input type="text" id="login_username" name="username" placeholder="Enter username" style="width: 100%; border: none; background: transparent; font-size: 16px; padding: 0;" required>
                    </div>
                    <div style="background-color: #f5f5f5; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
                        <label for="login_password" style="display: block; color: #777; font-size: 14px; margin-bottom: 5px;">Password</label>
                        <input type="password" id="login_password" name="password" placeholder="Enter password" style="width: 100%; border: none; background: transparent; font-size: 16px; padding: 0;" required>
                    </div>
                    <div class="d-flex justify-content-center">
                        <button type="submit" style="background-color: #FF8C00; border: none; cursor: pointer; color: white; font-size: 14px; font-weight: 500; padding: 8px 15px; border-radius: 5px;">Login</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
