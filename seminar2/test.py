next_href = "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
result = '/'.join(next_href.split('/')[:-1])
print(result)