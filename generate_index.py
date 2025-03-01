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

    # Default file to load (SpringBoot Basics or the first available file)
    default_file = next((file for file in notion_files if "SpringBoot - Basics" in file), None)
    default_file = default_file if default_file else (notion_files[0] if notion_files else "")

    # Start writing the index.html file
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>My Notion Notes</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        /* General Styling */
        body {{
            font-family: 'Poppins', sans-serif;
            background: #f8f9fa;
            color: #333;
            display: flex;
            overflow: hidden;
        }}

        /* Top Navbar */
        .navbar {{
            background: #3949AB;
            color: white;
            padding: 12px 20px;
            font-weight: bold;
            width: 100%;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 1000;
        }}

        .navbar a {{
            color: white;
            text-decoration: none;
            margin-right: 15px;
        }}

        /* Sidebar */
        #sidebar {{
            width: 280px;
            background: white;
            padding: 20px;
            height: 100vh;
            position: fixed;
            border-right: 1px solid #ddd;
            overflow-y: auto;
            resize: horizontal;
            overflow-x: hidden;
            min-width: 200px;
            max-width: 500px;
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

        /* Draggable Sidebar Handle */
        #sidebar-resizer {{
            width: 5px;
            background: #ccc;
            cursor: ew-resize;
            position: absolute;
            right: 0;
            top: 0;
            height: 100%;
        }}

        /* Main Content */
        #main-content {{
            flex-grow: 1;
            padding: 20px;
            margin-left: 300px;
            transition: margin-left 0.2s ease-in-out;
            width: calc(100% - 300px);
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
           background: transparent !important;
        }}

        /* Override Notion Styles */
        iframe {{
            width: 100%;
            height: 85vh;
            border: none;
        }}
        
        iframe::-webkit-scrollbar {{
            display: none; /* Hide scrollbars */
        }}

        .dark-mode iframe {{
            filter: invert(0.9);
        }}

    </style>
    <script>
        function loadPage(url) {{
            document.getElementById("content-frame").src = url;
        }}

        function toggleDarkMode() {{
            document.body.classList.toggle("dark-mode");
            localStorage.setItem("darkMode", document.body.classList.contains("dark-mode") ? "enabled" : "disabled");
        }}

        // Draggable Sidebar Logic
        document.addEventListener("DOMContentLoaded", function() {{
            const sidebar = document.getElementById("sidebar");
            const mainContent = document.getElementById("main-content");
            const resizer = document.getElementById("sidebar-resizer");

            let isResizing = false;

            resizer.addEventListener("mousedown", function(event) {{
                isResizing = true;
                document.addEventListener("mousemove", resizeSidebar);
                document.addEventListener("mouseup", stopResizing);
            }});

            function resizeSidebar(event) {{
                if (isResizing) {{
                    let newWidth = event.clientX;
                    if (newWidth >= 200 && newWidth <= 500) {{
                        sidebar.style.width = newWidth + "px";
                        mainContent.style.marginLeft = (newWidth + 20) + "px";
                        mainContent.style.width = "calc(100% - " + (newWidth + 20) + "px)";
                    }}
                }}
            }}

            function stopResizing() {{
                isResizing = false;
                document.removeEventListener("mousemove", resizeSidebar);
                document.removeEventListener("mouseup", stopResizing);
            }}
        }});

        window.onload = function() {{
            loadPage("{default_file}");
            if (localStorage.getItem("darkMode") === "enabled") {{
                document.body.classList.add("dark-mode");
            }}
        }};
    </script>
</head>
<body>
    <div class="navbar">
        <a href="#" onclick="loadPage('{default_file}')">🏠 Home</a>
        <a href="#" onclick="toggleDarkMode()">🌙 Dark Mode</a>
    </div>

    <div id="sidebar">
        <div id="sidebar-resizer"></div>
        <h4>📂 Notes</h4>
        <ul class="list-unstyled">
""")

        # Add all notes as styled sidebar links
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

    print(f"✅ index.html has been successfully generated with {len(notion_files)} notes!")

# Run the function
if __name__ == "__main__":
    generate_index()
