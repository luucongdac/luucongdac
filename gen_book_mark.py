import re

# Dữ liệu mẫu bạn đã cung cấp
data = """


"""

# Hàm trích xuất bookmark từ dữ liệu
def extract_bookmarks(data):
    bookmarks = {}
    
    # Tìm tất cả các subfolder trong dấu [xxx]
    folder_pattern = re.compile(r'---\[(.*?)\]---')
    folder_matches = folder_pattern.findall(data)

    # Lặp qua từng subfolder
    for folder in folder_matches:
        # Tìm các mục trong subfolder
        folder_data_pattern = re.compile(r'---\[' + re.escape(folder) + r'\]---(.*?)(?=---\[|\Z)', re.DOTALL)
        folder_data = folder_data_pattern.search(data).group(1).strip()

        # Tìm các mục name:link
        link_pattern = re.compile(r'(\S+):\s*(https?://\S+)')
        links = link_pattern.findall(folder_data)

        # Lưu vào dict
        bookmarks[folder] = [{"Name": name, "Link": link} for name, link in links]

    return bookmarks

# Hàm tạo file bookmark
def generate_bookmark_file(bookmarks_data):
    header = '''
    <!DOCTYPE NETSCAPE-Bookmark-file-1>
    <!-- This is an automatically generated file.
         It will be read and overwritten.
         DO NOT EDIT! -->
    <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
    <TITLE>Bookmarks</TITLE>
    <H1>Bookmarks</H1>
    <DL><p>
        <DT><H3 ADD_DATE="1730285454" LAST_MODIFIED="1730721852" PERSONAL_TOOLBAR_FOLDER="true">Bookmarks bar</H3>
        <DL><p>
    '''
    
    botder = '''
        </DL><p>
    </DL><p>
    '''
    
    bookmark_in_subfolder_template = '''
        <DT><H3 ADD_DATE="1730285467" LAST_MODIFIED="0">{NameFolder}</H3>
        <DL><p>
            {Links}
        </DL><p>
    '''
    
    bookmark_template = '''
        <DT><A HREF="{Link}" ADD_DATE="1728961208" ICON="">{Name}</A>
    '''

    # Tạo nội dung bookmark từ dữ liệu
    bookmark_file_content = header
    for folder, bookmarks in bookmarks_data.items():
        links_content = "".join([bookmark_template.format(Name=bookmark["Name"], Link=bookmark["Link"]) for bookmark in bookmarks])
        bookmark_file_content += bookmark_in_subfolder_template.format(NameFolder=folder, Links=links_content)
    
    bookmark_file_content += botder
    return bookmark_file_content

# Trích xuất dữ liệu bookmark từ mẫu dữ liệu
bookmarks_data = extract_bookmarks(data)

# Tạo file bookmark HTML
bookmark_file_content = generate_bookmark_file(bookmarks_data)

# Lưu vào file import.html
with open('import.html', 'w', encoding='utf-8') as f:
    f.write(bookmark_file_content)

print("Bookmarks saved to import.html")
