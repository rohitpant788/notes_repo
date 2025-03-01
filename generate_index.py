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
<html>
<head>
    <title>My Notion Notes</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; display: flex; }}
        #sidebar {{ width: 250px; background: #2C3E50; color: white; padding: 20px; height: 100vh; position: fixed; overflow-y: auto; }}
        #sidebar h2 {{ color: #ecf0f1; font-size: 20px; margin-bottom: 10px; }}
        #sidebar ul {{ list-style-type: none; padding: 0; }}
        #sidebar li {{ margin: 10px 0; }}
        #sidebar a {{ color: white; text-decoration: none; display: block; padding: 8px; border-radius: 5px; }}
        #sidebar a:hover {{ background: #34495E; }}
        #main-content {{ margin-left: 270px; padding: 20px; flex-grow: 1; width: 100%; }}
        #content-frame {{ width: 100%; height: 90vh; border: none; background: #f4f4f4; }}
    </style>
    <script>
        function loadPage(url) {{
            document.getElementById("content-frame").src = url;
        }}

        // Set default page on load
        window.onload = function() {{
            loadPage("{default_file}");
        }};
    </script>
</head>
<body>
    <div id="sidebar">
        <h2>📂 Notes</h2>
        <ul>
""")

        # Add all notes as sidebar links
        for file in sorted(notion_files):
            display_name = clean_file_name(os.path.basename(file))  # Clean filename
            f.write(f'<li><a href="#" onclick="loadPage(\'{file}\')">{display_name}</a></li>\n')

        # Close sidebar and add main content area
        f.write(f"""
        </ul>
    </div>

    <div id="main-content">
        <iframe id="content-frame"></iframe>
    </div>

</body>
</html>
""")

    print(f"✅ index.html has been successfully generated with {len(notion_files)} notes!")

# Run the function
if __name__ == "__main__":
    generate_index()
