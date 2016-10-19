class DataBase:
    def __init__(self):
        """(article_id,content,author,date)"""
        self.articles = [(1, """Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has
                            been the industry's standard dummy text ever since the 1500s, when an unknown printer took a
                            galley of type and scrambled it to make a type specimen book. It has survived not only five
                            centuries, but also the leap into electronic typesetting, remaining essentially unchanged.
                            It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum
                            passages, and more recently with desktop publishing software like Aldus PageMaker including
                            versions of Lorem Ipsum.""",
                          'Author1', '1995.01.05'),
                         (1, """Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has
                                                     been the industry's standard dummy text ever since the 1500s, when an unknown printer took a
                                                     galley of type and scrambled it to make a type specimen book. It has survived not only five
                                                     centuries, but also the leap into electronic typesetting, remaining essentially unchanged.
                                                     It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum
                                                     passages, and more recently with desktop publishing software like Aldus PageMaker including
                                                     versions of Lorem Ipsum.""",
                          'Author1', '1995.01.05'),
                         (1, """Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has
                                    been the industry's standard dummy text ever since the 1500s, when an unknown printer took a
                                    galley of type and scrambled it to make a type specimen book. It has survived not only five
                                    centuries, but also the leap into electronic typesetting, remaining essentially unchanged.
                                    It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum
                                    passages, and more recently with desktop publishing software like Aldus PageMaker including
                                    versions of Lorem Ipsum.""",
                          'Author1', '1995.01.05')
                         ]
        self.users = [(1, 'admin', 'admin', '')]


class GetData:
    def __init__(self):
        self.data_base = DataBase()

    def get_articles(self):
        return self.data_base.articles

    def get_article(self, id):
        for value in self.data_base.articles:
            if id == value[0]:
                return value
        print('Запись не найдена')
        return None

    def add_article(self, content, author_id, date):
        last_id = 1
        if len(self.data_base.articles) != 0:
            last_id = self.data_base.articles[-1][0]
        self.data_base.articles.append((last_id + 1, content, author_id, date))
        return True

    def delete_article(self, id):
        if len(self.data_base.articles) == 0:
            print('БД пустая')
            return False
        for item in self.data_base.articles:
            if id == item[0]:
                self.data_base.articles.remove(item)
                return True
        print('Запись не найдена')
        return False

    def get_user(self, login):
        for item in self.data_base.users:
            if login == item[1]:
                return item
        print('Запись не найдена')

    def get_sessionid(self):
        pass
