import os
import re

# Define the directory where Notion files are stored
NOTION_FOLDER = "notion"

# Define the output file
INDEX_FILE = "index.html"

# Function to clean Notion-generated filenames
def clean_file_name(filename):
    filename = filename.replace(".html", "")  # Remove .html extension
    filename = re.sub(r"[-\s]*[\da-f]{32}$", "", filename)  # Remove Notion's unique ID
    filename = filename.replace("-", " ")  # Replace dashes with spaces
    filename = re.sub(r"\s+", " ", filename).strip()  # Remove extra spaces
    return filename

# Function to generate the index.html file
def generate_index():
    notion_files = []
    for root, _, files in os.walk(NOTION_FOLDER):
        for file in files:
            if file.endswith(".html"):
                relative_path = os.path.join(root, file).replace("\\", "/")  # Ensure compatibility with Windows
                notion_files.append(relative_path)

    # Default file to load
    default_file = next((file for file in notion_files if "SpringBoot - Basics" in file), None)
    default_file = default_file if default_file else (notion_files[0] if notion_files else "")

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>My Notion Notes</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{
            font-family: 'Poppins', sans-serif;
            margin: 0;
            background: #f8f9fa;
            color: #333;
        }}

        /* Top Navbar */
        .navbar {{
            background: #3949AB;
            color: white;
            padding: 12px 20px;
            font-weight: bold;
            display: flex;
            align-items: center;
        }}

        .navbar a {{
            color: white;
            text-decoration: none;
            margin-right: 15px;
        }}

        .navbar a:hover {{
            text-decoration: underline;
        }}

        /* Sidebar */
        #sidebar {{
            width: 250px;
            background: white;
            padding: 20px;
            height: 100vh;
            position: fixed;
            border-right: 1px solid #ddd;
            overflow-y: auto;
        }}

        #sidebar h4 {{
            color: #3949AB;
            font-size: 20px;
            margin-bottom: 15px;
        }}

        #sidebar a {{
            text-decoration: none;
            display: block;
            padding: 8px 0;
            color: #333;
        }}

        #sidebar a:hover {{
            color: #3949AB;
            font-weight: bold;
        }}

        /* Main Content */
        #main-content {{
            margin-left: 270px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        #content-frame {{
            width: 100%;
            height: 85vh;
            border: none;
            background: white;
        }}

        /* Dark Mode */
        .dark-mode {{
            background: #181818 !important;
            color: white !important;
        }}

        .dark-mode .navbar, .dark-mode #sidebar {{
            background: #212121 !important;
            color: white !important;
        }}

        .dark-mode a {{
            color: white !important;
        }}

        .dark-mode #content-frame {{
            background: #252525 !important;
        }}

    </style>
    <script>
        function loadPage(url) {{
            document.getElementById("content-frame").src = url;
            document.getElementById("content-frame").style.display = "block";
        }}

        function loadHome() {{
            loadPage("{default_file}");
        }}

        function toggleDarkMode() {{
            document.body.classList.toggle("dark-mode");
            localStorage.setItem("darkMode", document.body.classList.contains("dark-mode") ? "enabled" : "disabled");
        }}

        window.onload = function() {{
            loadPage("{default_file}");  // Load default file on page load

            if (localStorage.getItem("darkMode") === "enabled") {{
                toggleDarkMode();
            }}
        }};
    </script>
</head>
<body>
    <div class="navbar">
        <a href="#" onclick="loadHome()">🏠 Home</a>
        <a href="#">📘 Rohit's Notes</a>
        <a href="#" onclick="toggleDarkMode()">🌙 Dark Mode</a>
    </div>

    <div id="sidebar">
        <h4>📂 Notes</h4>
        <ul class="list-unstyled">
""")

        # Add all notes as a flat list in the sidebar
        for file in sorted(notion_files):
            display_name = clean_file_name(os.path.basename(file))  # Clean filename
            f.write(f'<li><a href="#" class="text-dark" onclick="loadPage(\'{file}\')">{display_name}</a></li>\n')

        # Close sidebar and add main content area
        f.write(f"""
        </ul>
    </div>

    <div id="main-content">
        <iframe id="content-frame"></iframe>
    </div>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

</body>
</html>
""")

    print(f"✅ index.html generated with 'SpringBoot - Basics' as the default page!")

if __name__ == "__main__":
    generate_index()
