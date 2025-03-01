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
    # Get all HTML files inside the /notion folder
    notion_files = []
    for root, _, files in os.walk(NOTION_FOLDER):
        for file in files:
            if file.endswith(".html"):
                relative_path = os.path.join(root, file).replace("\\", "/")  # Ensure compatibility with Windows
                notion_files.append(relative_path)

    # Default file to load
    default_file = next((file for file in notion_files if "SpringBoot - Basics" in file), None)
    default_file = default_file if default_file else notion_files[0]  # Load first file if "SpringBoot - Basics" is missing

    # Start writing the index.html file
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>My Notion Notes</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        /* General Styles */
        body {{
            font-family: 'Poppins', sans-serif;
            margin: 0;
            display: flex;
            background: #f8f9fa;
            color: #333;
            transition: background 0.3s, color 0.3s;
        }}

        /* Sidebar Styling */
        #sidebar {{
            width: 280px;
            background: #2C3E50;
            color: white;
            padding: 20px;
            height: 100vh;
            position: fixed;
            overflow-y: auto;
            transition: background 0.3s;
            box-shadow: 2px 0 5px rgba(0, 0, 0, 0.2);
        }}

        #sidebar h2 {{
            color: #F8F9FA;
            font-size: 22px;
            margin-bottom: 15px;
            text-align: center;
        }}

        #sidebar .note-link {{
            display: block;
            background: #34495E;
            padding: 10px;
            border-radius: 6px;
            margin-bottom: 6px;
            text-decoration: none;
            color: white;
            font-weight: 500;
            text-align: left;
            transition: background 0.3s ease-in-out;
        }}

        #sidebar .note-link:hover {{
            background: #1ABC9C;
            color: white;
        }}

        /* Main Content */
        #main-content {{
            flex-grow: 1;
            padding: 20px;
            margin-left: 280px; /* Matches sidebar width */
            width: calc(100% - 280px);
            transition: background 0.3s, color 0.3s;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}

        #content-frame {{
            width: 95%;
            height: 90vh;
            border: none;
            background: white;
            transition: background 0.3s;
            border-radius: 8px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        }}

        /* Dark Mode Toggle Button */
        #dark-mode-toggle {{
            position: fixed;
            top: 10px;
            right: 20px;
            padding: 8px 15px;
            border: none;
            background: #2C3E50;
            color: white;
            cursor: pointer;
            border-radius: 5px;
            font-size: 14px;
            transition: background 0.3s;
        }}

        #dark-mode-toggle:hover {{
            background: #1A252F;
        }}

        /* Dark Mode Styles */
        body.dark-mode {{
            background: #181818;
            color: #f8f9fa;
        }}

        #sidebar.dark-mode {{
            background: #1A252F;
        }}

        #sidebar .note-link.dark-mode {{
            background: #343A40;
            color: #f8f9fa;
        }}

        #sidebar .note-link.dark-mode:hover {{
            background: #1ABC9C;
            color: white;
        }}

        #main-content.dark-mode {{
            background: #252525;
            color: #f8f9fa;
        }}

        #content-frame.dark-mode {{
            background: #252525;
        }}

        #dark-mode-toggle.dark-mode {{
            background: #F1C40F;
            color: black;
        }}

        /* Improve readability */
        body.dark-mode p,
        body.dark-mode li,
        body.dark-mode h1,
        body.dark-mode h2,
        body.dark-mode h3,
        body.dark-mode h4,
        body.dark-mode h5,
        body.dark-mode h6 {{
            color: #ffffff !important;
        }}
    </style>
    <script>
        function loadPage(url) {{
            document.getElementById("content-frame").src = url;
        }}

        // Dark Mode Toggle
        function toggleDarkMode() {{
            const elements = [
                document.body, 
                document.getElementById("sidebar"), 
                document.getElementById("main-content"), 
                document.getElementById("content-frame"), 
                document.getElementById("dark-mode-toggle")
            ];

            elements.forEach(el => el.classList.toggle("dark-mode"));

            // Save user preference
            const isDarkMode = document.body.classList.contains("dark-mode");
            localStorage.setItem("darkMode", isDarkMode ? "enabled" : "disabled");
        }}

        // Load dark mode preference
        window.onload = function() {{
            loadPage("{default_file}");

            if (localStorage.getItem("darkMode") === "enabled") {{
                toggleDarkMode();
            }}
        }};
    </script>
</head>
<body>
    <button id="dark-mode-toggle" class="btn btn-sm btn-dark" onclick="toggleDarkMode()">🌙 Dark Mode</button>

    <div id="sidebar">
        <h2>📂 Notes</h2>
        <ul class="list-unstyled">
""")

        # Add all notes as styled sidebar buttons
        for file in sorted(notion_files):
            display_name = clean_file_name(os.path.basename(file))  # Clean filename
            f.write(f'<li><a href="#" class="note-link" onclick="loadPage(\'{file}\')">{display_name}</a></li>\n')

        # Close sidebar and add main content area
        f.write(f"""
        </ul>
    </div>

    <div id="main-content">
        <iframe id="content-frame" class="rounded shadow-lg"></iframe>
    </div>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

</body>
</html>
""")

    print(f"✅ index.html has been successfully generated with {len(notion_files)} notes!")

# Run the function
if __name__ == "__main__":
    generate_index()
