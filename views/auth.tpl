% rebase('layout.tpl', title=title, year=year)

<link rel="stylesheet" href="/static/content/page_styles/styles_auth.css">

<div class="jumbotron">
    <div>
        <h1>{{ title }}</h1>
        <h3 class="mb-4">{{ message }}</h3>
    </div>
</div>

<div class="user-profile-container">
    <div class="card shadow-sm">
        <div class="row">
            <!-- Registration Form -->
            <div class="col-md-6">
                <h4 class="mb-3 text-center">Register</h4>
                <form method="POST" action="/register">
                    <div class="form-group">
                        <label for="reg_firstname">First Name</label>
                        <input type="text" id="reg_firstname" name="firstname" placeholder="Enter first name" required>
                    </div>
                    <div class="form-group">
                        <label for="reg_lastname">Last Name</label>
                        <input type="text" id="reg_lastname" name="lastname" placeholder="Enter last name" required>
                    </div>
                    <div class="form-group">
                        <label for="reg_email">Email</label>
                        <input type="email" id="reg_email" name="email" placeholder="Enter email" required>
                    </div>
                    <div class="form-group">
                        <label for="reg_phone">Phone Number</label>
                        <input type="tel" id="reg_phone" name="phone" placeholder="Enter phone number" required>
                    </div>
                    <div class="form-group">
                        <label for="reg_birthdate">Date of Birth</label>
                        <input type="date" id="reg_birthdate" name="birthdate" required>
                    </div>
                    <div class="form-group">
                        <label for="reg_username">Username</label>
                        <input type="text" id="reg_username" name="username" placeholder="Enter username" required>
                    </div>
                    <div class="form-group">
                        <label for="reg_password">Password</label>
                        <input type="password" id="reg_password" name="password" placeholder="Enter password" required>
                    </div>
                    <div class="d-flex justify-content-center mt-3">
                        <button type="submit" class="btn-submit">Register</button>
                    </div>
                </form>
            </div>
            <!-- Login Form -->
            <div class="col-md-6">
                <h4 class="mb-3 text-center">Login</h4>
                <form method="POST" action="/login">
                    <div class="form-group">
                        <label for="login_username">Username</label>
                        <input type="text" id="login_username" name="username" placeholder="Enter username" required>
                    </div>
                    <div class="form-group">
                        <label for="login_password">Password</label>
                        <input type="password" id="login_password" name="password" placeholder="Enter password" required>
                    </div>
                    <div class="d-flex justify-content-center">
                        <button type="submit" class="btn-submit">Login</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>