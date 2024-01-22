from newspaper import Article

def get_website_information(link):
    article = Article(link)
    article.download()
    article.parse()
    return article.text
