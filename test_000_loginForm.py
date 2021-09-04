import time
import unittest

from parameterized import parameterized

import cfg.test_data as test_data
from cfg.cfg import *


class TestLoginForm(unittest.TestCase):
    enter_button = None
    email_error = None
    pass_error = None
    input_login = None
    input_password = None

    @classmethod
    def setUpClass(cls) -> None:
        d.get(test_data.URI + test_data.LOGIN_PAGE)
        cls.enter_button = d.find_element_by_class_name(
            "btn-default.left.login")
        cls.email_error = d.find_element_by_id("2email-error")
        cls.pass_error = d.find_element_by_id("pass-error")
        cls.input_login = d.find_element_by_name("session[login]")
        cls.input_password = d.find_element_by_name("session[password]")

    @classmethod
    def clean_inputs(cls) -> None:
        cls.input_login.send_keys(Keys.CONTROL + "a")
        cls.input_login.send_keys(Keys.DELETE)
        cls.input_password.send_keys(Keys.CONTROL + "a")
        cls.input_password.send_keys(Keys.DELETE)

    # В результате выполнения тестов может перестраивается DOM
    # (в тесте 030 -- поля ввода переходят в подкласс "field_with_errors")
    # Один из способов обойти проблему - обновлять страницу, дать время на
    # перегрузку страницы и заново найти нужные поля.
    @classmethod
    def setUp(cls) -> None:
        d.refresh()
        time.sleep(1)
        cls.enter_button = d.find_element_by_class_name(
            "btn-default.left.login")
        cls.email_error = d.find_element_by_id("2email-error")
        cls.pass_error = d.find_element_by_id("pass-error")
        cls.input_login = d.find_element_by_name("session[login]")
        cls.input_password = d.find_element_by_name("session[password]")
        cls.clean_inputs()

    @classmethod
    def tearDownClass(cls) -> None:
        d.close()

    # Тест на открытие сайта
    def test_000_open_site(self):
        self.assertIn("Личный кабинет пользователя", d.title)

    # Логинимся не вводя логин и пароль
    def test_010_login_without_name_password(self):
        # click по кнопке "Войти"
        self.enter_button.click()
        self.assertIn("Некорректный email", self.email_error.text)
        self.assertTrue(self.email_error.is_displayed())
        self.assertIn("Пароль не может быть пустым", self.pass_error.text)
        self.assertTrue(self.pass_error.is_displayed())

    # Ряд тестов на некорректный логин (email), но с корректным паролем
    @parameterized.expand(test_data.INVALID_LOGINS)
    def test_020_login_with_invalid_login(self, login):
        self.input_login.send_keys(login)
        self.input_password.send_keys(test_data.VALID_PASSWORD)
        # click по кнопке "Войти"
        self.enter_button.click()
        # Должно быть отображено сообщение об ошибке email, но не пароля
        self.assertIn("Некорректный email", self.email_error.text)
        self.assertTrue(self.email_error.is_displayed())
        self.assertFalse(self.pass_error.is_displayed())

    # Тест на корректный логин (email), но с пустым паролем
    def test_030_login_with_valid_login_and_empty_password(self):
        self.input_login.send_keys(test_data.VALID_LOGIN)
        # click по кнопке "Войти"
        self.enter_button.click()
        # Должно быть отображено сообщение об ошибке пароля, но не email
        self.assertIn("Пароль не может быть пустым", self.pass_error.text)
        self.assertTrue(self.pass_error.is_displayed())
        self.assertFalse(self.email_error.is_displayed())

    # Тест на корректный логин (email), но неверный пароль
    def test_040_login_with_valid_login_and_wrong_password(self):
        self.input_login.send_keys(test_data.VALID_LOGIN)
        self.input_password.send_keys(test_data.WRONG_PASSWORD)
        # click по кнопке "Войти"
        self.enter_button.click()
        # Должно быть отображено сообщение об ошибке пароля или email
        # Здесь появляется ранее не существовавший div,
        # приходится искать его отдельно.
        self.assertIn("Неверный логин или пароль",
                      d.find_element_by_class_name("red").text)
        self.assertTrue(d.find_element_by_class_name("red").is_displayed())

    # Тест на корректный незарегистрированный логин (email) с валидным паролем
    def test_050_login_with_unreg_email_and_valid_password(self):
        self.input_login.send_keys(test_data.VALID_LOGIN_NO_REGISTERED)
        self.input_password.send_keys(test_data.WRONG_PASSWORD)
        # click по кнопке "Войти"
        self.enter_button.click()
        # Должно быть отображено сообщение об ошибке пароля или email
        # Здесь появляется ранее не существовавший div,
        # приходится искать его отдельно.
        self.assertIn("Неверный логин или пароль",
                      d.find_element_by_class_name("red").text)
        self.assertTrue(d.find_element_by_class_name("red").is_displayed())

    # Логинимся валидным пользователем и выходим
    def test_090_login_registered_user(self):
        # self.input_login = d.find_element_by_name("session[login]")
        # self.input_password = d.find_element_by_name("session[password]")
        self.input_login.send_keys(test_data.VALID_LOGIN)
        self.input_password.send_keys(test_data.WRONG_PASSWORD)
        # click по кнопке "Войти"
        self.enter_button.click()
        # Условие успешного входа мне не известно
        self.assertIn("Выполнен вход",
                      d.find_element_by_tag_name("body").text)


if __name__ == "__main__":
    tests_000 = unittest.TestLoader().loadTestsFromTestCase(TestLoginForm)
    test_mw = unittest.TestSuite([tests_000])
    result = unittest.TextTestRunner(verbosity=2).run(test_mw)

    if result.wasSuccessful():
        exit(0)
    else:
        exit(1)
