#Укажем что это за фича
Feature: Checking search
#Укажем имя сценария (в одной фиче может быть несколько)
Scenario: Сheck some text in search results
#И используем наши шаги.
  Given website "localhost:8000"
  Then push button with text 'Войти'
  Then login page 'Логин'
  Then authentication 'John Smith'
  Then go throught the links articles 'John Smith'
  Then check access to a edit article 'Редактировать'
  Then do edit 'Редактировать'
  Then check edit 'Отправить'
  Then send edit 'Attractor Blog'
  Then delete article 'John Smith'
  Then do delete article 'Удалить'
  Then do add article 'Добавить запись'
  Then send add article 'Отправить'
  Then logout 'Выйти'
  Then push button with text 'Войти'
  Then wrong login 'Логин'
  Then assert error 'Вы ввели неверную комбинацию логина и пароля.'
