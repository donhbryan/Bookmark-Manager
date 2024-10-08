import json

# Bookmark class to store bookmark data
class Bookmark:
  def __init__(self, title, url, folder=None):
    self.title = title
    self.url = url
    self.folder = folder
    self.children = []  # List to store child bookmarks

# Function to load bookmarks from JSON file
def load_bookmarks(file_path):
  try:
    with open(file_path, 'r') as f:
      data = json.load(f)
      return parse_json(data)
  except FileNotFoundError:
    print(f"File not found: {file_path}")
    return None
  except json.JSONDecodeError:
    print(f"Error parsing JSON file: {file_path}")
    return None

# Function to parse JSON data into Bookmark objects
def parse_json(data):
  if isinstance(data, dict):
    bookmark = Bookmark(data['title'], data['url'], data.get('folder'))
    if 'children' in data:
      for child in data['children']:
        bookmark.children.append(parse_json(child))
    return bookmark
  elif isinstance(data, list):
    return [parse_json(item) for item in data]
  else:
    return None

# Function to save bookmarks to JSON file
def save_bookmarks(bookmarks, file_path):
  with open(file_path, 'w') as f:
    json.dump(bookmarks, f, indent=4)

# Function to display bookmarks in a hierarchical manner
def display_bookmarks(bookmarks, indent=0):
  for bookmark in bookmarks:
    print(" " * indent + bookmark.title)
    if bookmark.folder:
      print(" " * (indent + 2) + f"[Folder] {bookmark.folder}")
    if bookmark.children:
      display_bookmarks(bookmark.children, indent + 2)

# Function to search bookmarks by title
def search_bookmarks(bookmarks, query):
  results = []
  for bookmark in bookmarks:
    if query.lower() in bookmark.title.lower():
      results.append(bookmark)
    if bookmark.children:
      results.extend(search_bookmarks(bookmark.children, query))
  return results

# Function to edit bookmark details (title, url)
def edit_bookmark(bookmark):
  new_title = input("Enter new title (or leave blank to keep): ")
  if new_title:
    bookmark.title = new_title
  new_url = input("Enter new URL (or leave blank to keep): ")
  if new_url:
    bookmark.url = new_url

# Function to group bookmarks into a new folder
def group_bookmarks(bookmarks, folder_name):
  new_folder = Bookmark(folder_name, None)
  selected_bookmarks = []
  while True:
    results = search_bookmarks(bookmarks, input("Search for bookmarks to group (or 'q' to quit): "))
    if not results and input("No results found. Continue (y/n)? ").lower() != 'y':
      break
    for bookmark in results:
      if bookmark not in selected_bookmarks:
        selected_bookmarks.append(bookmark)
        bookmarks.remove(bookmark)
  new_folder.children = selected_bookmarks
  bookmarks.append(new_folder)

# Function to ungroup a folder, moving its contents to the parent folder
def ungroup_bookmarks(bookmarks, folder):
  if folder.children:
    for child in folder.children:
      bookmarks.append(child)
  bookmarks.remove(folder)

# Main program loop
def main():
  bookmarks = []
  file_path = input("Enter file path for bookmarks (or 'q' to quit): ")
  if file_path.lower() != 'q':
    chrome_bookmarks = load_bookmarks(file_path)
    if chrome_bookmarks:
      bookmarks = chrome_bookmarks

  while True:
    print("\nMenu:")
    print("1. Export Bookmarks (JSON)")
    print("2. Import Bookmarks (JSON)")
    print("3. Display Bookmarks")
    print("4. Search Bookmarks")
    print("5. Edit Bookmark")
    print("6. Group Bookmarks")
    print("7. Ungroup Bookmarks")
    print("8. Quit")
    
main()
