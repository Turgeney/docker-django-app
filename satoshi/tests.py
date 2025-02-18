from django.test import TestCase
from django.urls import reverse
from .models import Users

class UsersViewsTests(TestCase):

    def test_index_page_GET(self):
        """Тест GET-запроса в index_page: страница должна отображаться с пустой формой"""
        response = self.client.get(reverse('Стартовая'))  # Обращаемся к URL через имя маршрута
        self.assertEqual(response.status_code, 200)  # Проверяем, что запрос возвращает статус 200
        self.assertContains(response, '<form')  # Убедимся, что HTML-страница содержит форму

    def test_index_page_POST_valid_data(self):
        """Тест POST-запроса с корректными данными: пользователь должен быть создан, затем перенаправление"""
        data = {
            'user_name': 'John',
            'user_surname': 'Doe',
            'user_hobby': 'Testing new apps'
        }
        response = self.client.post(reverse('Стартовая'), data=data)  # Посылаем POST-запрос с данными
        self.assertEqual(response.status_code, 302)  # Проверяем, что произошло перенаправление (302)
        self.assertRedirects(response, reverse('all_users'))  # Перенаправление должно быть к `all_users`

        # Проверяем, что данные действительно сохранены в базе
        self.assertEqual(Users.objects.count(), 1)  # В базе должен быть 1 пользователь
        user = Users.objects.first()
        self.assertEqual(user.user_name, 'John') 
        self.assertEqual(user.user_surname, 'Doe')  
        self.assertEqual(user.user_hobby, 'Testing new apps')  

    def test_index_page_POST_invalid_data(self):
        """Тест POST-запроса с некорректными данными: форма должна быть показана снова с ошибками"""
        data = {}  # Отправляем пустую форму
        response = self.client.post(reverse('Стартовая'), data=data)
        self.assertEqual(response.status_code, 200)  # Форма будет рендериться снова
        self.assertContains(response, '<ul class="errorlist">')  # Проверка, что ошибки отображаются
        self.assertEqual(Users.objects.count(), 0)  # Пользователь не создаётся

    def test_all_users_GET(self):
        """Тест GET-запроса в all_users: проверяем отображение списка пользователей"""
        # Создаём тестовых пользователей
        Users.objects.create(user_name="John", user_surname = "Smith", user_hobby = "Testing even newer apps")
        Users.objects.create(user_name="Jane", user_surname = "Chungus", user_hobby = "Being called funny names")

        response = self.client.get(reverse('all_users'))  # GET-запрос на страницу всех пользователей
        self.assertEqual(response.status_code, 200)  # Статус запроса 200
        self.assertContains(response, 'Smith')  # Проверяем, что первый пользователь отображается
        self.assertContains(response, 'Chungus')  # Проверяем, что второй пользователь отображается
