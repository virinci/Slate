import json
import subprocess as sp
import shutil
import sys
from pathlib import Path


blog_root = Path("..")


def copy_assets(blog: Path):
    extensions = ("jpeg", "mov", "mp4", "png")
    assets_src = blog / "blogs/assets"
    assets_dst = blog / "docs/assets"

    for ext in extensions:
        for src in assets_src.glob(f"*.{ext}"):
            shutil.copy2(src, assets_dst / src.name)


def get_home_button(file_name: str) -> str:
    base_path = (len(file_name.split("/")) - 1) * "../"
    return f"<a class='home' href='{base_path}index.html'>HOME</a>{switch_theme_btn_html}\n\n---\n\n"


def markdown_to_html(
    title: str, markdown_text: str, markdown_file: str, css_file: str, /
):
    markdown_text = markdown_text.encode()

    markdown_file = blog_root / "docs" / markdown_file
    assert markdown_file.suffix == ".md"
    html_file = markdown_file.with_suffix(".html")

    process = sp.run(
        (
            path_to_pandoc,
            "--metadata",
            f"title='{title}'",
            "--standalone",
            "--no-highlight",
            f"--css={css_file}",
            f"--output={html_file}",
        ),
        input=markdown_text,
        capture_output=True,
    )

    if process.returncode == 0:
        print(f"\033[32m{markdown_file} successfully translated to HTML\033[0m")
    else:
        print(f"\033[31mERROR: {process.stderr.decode()}\033[0m")


def create_dir(file_path: str):
    Path(file_path).mkdir(parents=True, exist_ok=True)


def create_blog(title: str, file_name: str, dir_name: str):
    blog_content = []

    blog_content.append("<h1>" + profile["name"] + "</h1>")
    blog_content.append('<div class="contents">')
    blog_content.append(get_home_button(file_name))

    with open(blog_root / "blogs" / file_name, "r") as file:
        blog_content.append("".join(file.readlines()))

    blog_content.append("\n")

    highlight_min_js = blog_root / "docs/highlight.min.js"
    file_dir = (blog_root / "docs" / file_name).resolve().parent
    assert highlight_min_js.is_file()

    highlight_min_js = highlight_min_js.resolve().relative_to(file_dir, walk_up=True)
    css_file = (
        (blog_root / "docs/blog.css").resolve().relative_to(file_dir, walk_up=True)
    )

    blog_content.append(
        f"\n<script src='{highlight_min_js}'></script><script>hljs.highlightAll();</script>"
    )

    blog_content.append(switch_theme_btn_js)
    blog_content.append(analytics)
    blog_content.append("</div>")
    blog_content.append(copyright_text)

    if dir_name != "":
        create_dir("../docs/" + dir_name)

    markdown_text = "\n".join(blog_content)
    markdown_to_html(title, markdown_text, file_name, css_file)


path_to_pandoc = "pandoc"

if len(sys.argv) >= 2:
    path_to_pandoc = sys.argv[1]
else:
    print("Trying installed pandoc at PATH")

profile = {}
blogs = []
contacts = []


LOGO_SVGS = {
    "mail": """
<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none"
    stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
    class="feather feather-mail">
    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
    <polyline points="22,6 12,13 2,6"></polyline>
</svg>
""",
    "twitter": """
<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none"
    stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
    class="feather feather-twitter">
    <path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z">
    </path>
</svg>
""",
    "github": """
<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none"
    stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
    class="feather feather-github">
    <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22">
    </path>
</svg>
""",
    "mastodon": """
<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none"
    stroke="white" stroke-linecap="round" stroke-linejoin="round">
    <path d="M21.327 8.566c0-4.339-2.843-5.61-2.843-5.61-1.433-.658-3.894-.935-6.451-.956h-.063c-2.557.021-5.016.298-6.45.956 0 0-2.843 1.272-2.843 5.61 0 .993-.019 2.181.012 3.441.103 4.243.778 8.425 4.701 9.463 1.809.479 3.362.579 4.612.51 2.268-.126 3.541-.809 3.541-.809l-.075-1.646s-1.621.511-3.441.449c-1.804-.062-3.707-.194-3.999-2.409a4.523 4.523 0 0 1-.04-.621s1.77.433 4.014.536c1.372.063 2.658-.08 3.965-.236 2.506-.299 4.688-1.843 4.962-3.254.434-2.223.398-5.424.398-5.424zm-3.353 5.59h-2.081V9.057c0-1.075-.452-1.62-1.357-1.62-1 0-1.501.647-1.501 1.927v2.791h-2.069V9.364c0-1.28-.501-1.927-1.502-1.927-.905 0-1.357.546-1.357 1.62v5.099H6.026V8.903c0-1.074.273-1.927.823-2.558.566-.631 1.307-.955 2.228-.955 1.065 0 1.872.409 2.405 1.228l.518.869.519-.869c.533-.819 1.34-1.228 2.405-1.228.92 0 1.662.324 2.228.955.549.631.822 1.484.822 2.558v5.253z"/>
</svg>
""",
    "linkedin": """
<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-linkedin">
    <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path>
    <rect x="2" y="9" width="4" height="12"></rect>
    <circle cx="4" cy="4" r="2"></circle>
</svg>
""",
    "instagram": """
<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-instagram">
    <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
    <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
    <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
</svg>
""",
}

# Make button
switch_theme_btn_html = """
<button id="btn" onclick="setTheme()">THEME</button>
"""
switch_theme_btn_js = ""

with open("js/theming.js") as file:
    script = file.read()
    switch_theme_btn_js = f"<script>{script}</script>"

with open("../profile.json") as file:
    profile = json.load(file)

for blog in profile["blogs"]:
    if blog.get("series") is not None:
        series = blog["series"]

        blogs.append("<details>")
        blogs.append("<summary>" + blog["name"] + "</summary>")

        for chapter in series:
            name = chapter["name"]
            link = chapter["link"]

            is_disabled = chapter.get("disabled", False)

            if is_disabled:
                blogs.append(
                    f"<a class='disabled' href='{link[:-3]}.html'> <li><s>{name}</s></li> </a>"
                )
            else:
                blogs.append(f"<a href='{link[:-3]}.html'> <li>{name}</li> </a>")

        blogs.append("</details>")
    else:
        name = blog["name"]
        link = blog["link"]
        is_disabled = blog.get("disabled", False)

        if is_disabled:
            blogs.append(
                f"<a class='disabled' href='{link[:-3]}.html'> <li><s>{name}</s></li> </a>"
            )
        else:
            blogs.append(f"<a href='{link[:-3]}.html'> <li>{name}</li> </a>")


# Contacts icons
socials = ("twitter", "mastodon", "instagram", "linkedin", "github")
for social in socials:
    if profile.get(social) is None:
        print(f"-> {social} account skipped")
    else:
        # contacts.append(f"<a rel='me' href='{profile['mastodon']}'> {LOGO_SVGS[social]} </a>")
        contacts.append(f"<a href='{profile[social]}'> {LOGO_SVGS[social]} </a>")

if profile.get("mail") is None:
    print("-> Mail skipped")
else:
    contacts.append(f"<a href='mailto:{profile['mail']}'> {LOGO_SVGS['mail']} </a>")

contact = ""
if len(contacts) != 0:
    contact = (
        "<br><h2>CONTACTS</h2><hr><div class='contact'>" + "".join(contacts) + "</div>"
    )

copyright_text = ""
if profile.get("copyright") is None:
    print("-> copyright skipped")
else:
    copyright_text = f"<footer>{profile['copyright']}</footer>"

analytics = ""
if profile.get("analytics") is None:
    print("-> Analytics skipped")
else:
    analytics = profile["analytics"]


index_html = f"""
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>{profile["name"]}</title>
        <link rel="stylesheet" href="./index.css">
        <link rel="icon" href="./favicon.ico" type="image/x-icon">
    </head>
    <body>
        <div class="contents">
            <h1 style="display: inline-block; padding-right: 20px;">{profile["name"]}</h1>
            {switch_theme_btn_html}

            <hr>

            <div class="profile">
                <img src="{profile["profile_picture"]}" width="150" height="150" style="float:left; margin-right: 15px; margin-top: 5px;">
                <p>
                    {"<br>".join(profile["description"])}
                </p>
                <br>
            </div>

            <h2>BLOGS</h2>

            <hr>

            <div class="project">
                <ul>
                    {"".join(blogs)}
                </ul>
            </div>

            {contact}
        </div>

        {copyright_text}
        {switch_theme_btn_js}
        {analytics}

        <!--
        <main>
            <h1>Welcome to My Website</h1>
        </main>
        <script src="index.js"></script>
        -->
      </body>
</html>
"""

# Clean build docs
assert not (blog_root / "docs").exists(), f"Please remove {blog_root / 'docs'}"
create_dir("../docs")

with open("../docs/index.html", "w") as file:
    file.write(index_html)


# Copy resources
shutil.copy2(
    "../" + profile["profile_picture"], "../docs/" + profile["profile_picture"]
)
shutil.copy2("css/blog.css", "../docs/blog.css")
shutil.copy2("css/index.css", "../docs/index.css")
shutil.copy2("js/highlight.min.js", "../docs/highlight.min.js")

# Clean build assets
assert not (
    blog_root / "docs/assets"
).exists(), f"Please remove {blog_root / 'docs/assets'}"
create_dir("../docs/assets")

copy_assets(Path("../"))

for blog in profile["blogs"]:
    is_series = blog.get("series")
    if is_series is not None:
        series = blog["series"]

        for chapter in series:
            title = chapter["name"]
            file_name = chapter["link"]
            create_blog(title, file_name, file_name.split("/")[0])
    else:
        title = blog["name"]
        file_name = blog["link"]
        create_blog(title, file_name, "")
