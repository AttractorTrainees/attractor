#Укажем что это за фича
Feature: Checking search
#Укажем имя сценария (в одной фиче может быть несколько)
Scenario: Search for an account
#И используем наши шаги.
  Given website "localhost:8000/login/"
  Then I will see the account details
