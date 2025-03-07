% rebase('layout.tpl', title=title, year=year)

<div class="container d-flex justify-content-center align-items-center min-vh-100">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card shadow-sm">
                <div class="card-header bg-primary text-white text-center">
                    <h2>{{ title }}</h2>
                </div>
                <div class="card-body">
                    <h3 class="text-center mb-4">{{ message }}</h3>
                    
                    <div class="row">
                        <!-- Registration Form -->
                        <div class="col-md-6 border-end">
                            <h4 class="text-center mb-3">Register</h4>
                            <form method="POST" action="/register">
                                <div class="mb-3">
                                    <label for="reg_username" class="form-label">Username</label>
                                    <input type="text" class="form-control" id="reg_username" name="username" placeholder="Enter username" required>
                                </div>
                                <div class="mb-3">
                                    <label for="reg_password" class="form-label">Password</label>
                                    <input type="password" class="form-control" id="reg_password" name="password" placeholder="Enter password" required>
                                </div>
                                <div class="d-grid">
                                    <button type="submit" class="btn btn-primary">Register</button>
                                </div>
                            </form>
                        </div>

                        <!-- Login Form -->
                        <div class="col-md-6">
                            <h4 class="text-center mb-3">Login</h4>
                            <form method="POST" action="/login">
                                <div class="mb-3">
                                    <label for="login_username" class="form-label">Username</label>
                                    <input type="text" class="form-control" id="login_username" name="username" placeholder="Enter username" required>
                                </div>
                                <div class="mb-3">
                                    <label for="login_password" class="form-label">Password</label>
                                    <input type="password" class="form-control" id="login_password" name="password" placeholder="Enter password" required>
                                </div>
                                <div class="d-grid">
                                    <button type="submit" class="btn btn-success">Login</button>
                                </div>
                            </form>
                        </div>
                    </div>

                    <!-- Error Message -->
                    % if error:
                        <div class="alert alert-danger mt-4" role="alert">
                            {{ error }}
                        </div>
                    % end
                </div>
                <div class="card-footer text-center">
                    <small class="text-muted">Secure your account today!</small>
                </div>
            </div>
        </div>
    </div>
</div>