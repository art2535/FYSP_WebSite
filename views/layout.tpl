<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - Online PC Constructor</title>
    <link rel="stylesheet" type="text/css" href="/static/content/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/content/site.css" />
    <script src="/static/scripts/modernizr-2.6.2.js"></script>
</head>

<body>
    <div class="navbar navbar-inverse navbar-fixed-top" style="background: linear-gradient(to right, #F8D568, #FFA000);">
        <div class="container" style="background: transparent;">
            <link rel="stylesheet" href="/static/content/bootstrap.css">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" style="color: #333; font-family: Share-Tech-CYR-Bold; font-weight: bold; font-size: 24px;">Online PC Constructor</a>
            </div>
            <div class="navbar-collapse collapse">
                <ul class="nav navbar-nav">
                    <li><a href="/home" style="color: #333; font-family: Share-Tech-CYR-Bold; font-weight: bold; font-size: 20px; text-decoration: none;">Home</a></li>
                    <li><a href="/auth" style="color: #333; font-family: Share-Tech-CYR-Bold; font-weight: bold; font-size: 20px; text-decoration: none;">Authorization</a></li>
                    <li><a href="/constructor" style="color: #333; font-family: Share-Tech-CYR-Bold; font-weight: bold; font-size: 20px; text-decoration: none;">Constructor</a></li>
                    <li><a href="/profile" style="color: #333; font-family: Share-Tech-CYR-Bold; font-weight: bold; font-size: 20px; text-decoration: none;">Profile</a></li>
                    <li><a href="/reviews" style="color: #333; font-family: Share-Tech-CYR-Bold; font-weight: bold; font-size: 20px; text-decoration: none;">Reviews</a></li>
                    <li><a href="/partners" style="color: #333; font-family: Share-Tech-CYR-Bold; font-weight: bold; font-size: 20px; text-decoration: none;">Partners</a></li>
                    <li><a href="/new_products" style="color: #333; font-family: Share-Tech-CYR-Bold; font-weight: bold; font-size: 20px; text-decoration: none;">New products</a></li>
                    <li><a href="/articles" style="color: #333; font-family: Share-Tech-CYR-Bold; font-weight: bold; font-size: 20px; text-decoration: none;">Articles</a></li>
                </ul>
            </div>
        </div>
    </div>

    <div id="orderModal" class="modal">
      <div class="modal-content">
        <span class="modal-close">&times;</span>
        <p id="orderMessage"></p>
      </div>
    </div>

</body>



    <div class="container body-content">
        {{!base}}
        <hr />
        <footer>
            <p>&copy; {{ year }} - Online PC Constructor | Email - pc_constructor@mail.ru | Phone +78676892723</p>
        </footer>
    </div>

    <script src="/static/scripts/jquery-1.10.2.js"></script>
    <script src="/static/scripts/bootstrap.js"></script>
    <script src="/static/scripts/respond.js"></script>

</body>
</html>