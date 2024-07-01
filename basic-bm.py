import json

class BookmarkManager:
    def __init__(self):
        self.bookmarks = {}

    def load_bookmarks(self, filename):
        with open(filename, 'r') as file:
            self.bookmarks = json.load(file)

    def save_bookmarks(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.bookmarks, file, indent=4)

    def search_bookmarks(self, query):
        results = []
        for bookmark in self.bookmarks:
            if query.lower() in bookmark['title'].lower():
                results.append(bookmark)
        return results

    def sort_bookmarks(self):
        self.bookmarks.sort(key=lambda x: x['title'])

    def edit_bookmark(self, index, new_title):
        self.bookmarks[index]['title'] = new_title

    def add_bookmark(self, title, url):
        bookmark = {'title': title, 'url': url}
        self.bookmarks.append(bookmark)

# Example usage:
manager = BookmarkManager()
manager.load_bookmarks('bookmarks.json')

# Search for bookmarks
results = manager.search_bookmarks('python')
for bookmark in results:
    print(bookmark)

# Sort bookmarks
manager.sort_bookmarks()

# Edit a bookmark
manager.edit_bookmark(0, 'New Title')

# Add a bookmark
manager.add_bookmark('Google', 'http://www.google.com')

# Save bookmarks
manager.save_bookmarks('bookmarks_sorted.json')
