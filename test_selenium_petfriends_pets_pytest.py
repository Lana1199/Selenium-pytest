import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wdw

@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    #Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')
    driver.maximize_window()
    yield driver
    driver.quit()

#Неявные ожидания.

def test_all_pets_cards(driver):
   #Вводим email
    driver.find_element(By.ID, 'email').send_keys('sv.lana1199@gmail.com')
   #Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('dveri2014')
    #Ставим величину неявного ожидания элементов в 5 секунд.
    driver.implicitly_wait(5)
   #Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   #Проверяем, что мы оказались на главной странице сайта
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"


    #Нажимаем на кнопку Мои питомцы.
    driver.find_element(By.XPATH, '//a[text()="Мои питомцы"]').click()

   # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'H2').text == "Лана"

   # Объявили три переменные, в которых записали все найденные элементы на странице: в images — все картинки питомцев,
   # в names — все их имена, в ages — возрасты.

    driver.implicitly_wait(2)

    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')

    driver.implicitly_wait(2)

    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')

    driver.implicitly_wait(2)

    ages = driver.find_elements(By.CSS_SELECTOR, '.card-deck .age')

   #Организуем цикл, который может перебрать все эти элементы.

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert ages[i].text != ''


#Явные ожидания.

def test_pets_table(driver):
    """Проверка таблицы питомцев на наличие всех колонок"""

    driver.find_element(By.ID, 'email').send_keys('sv.lana1199@gmail.com')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('dveri2014')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Ожидание загрузки главной страницы
    wdw(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//a[text()=\"Мои питомцы\"]')))

    # Нажимаем на кнопку Мои питомцы.
    driver.find_element(By.XPATH, '//a[text()="Мои питомцы"]').click()



    # Переход на страницу со списком питомцев
    driver.get('https://petfriends.skillfactory.ru/my_pets')

    # Ожидание появления таблицы
    wdw(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.table')))

    # Проверка наличия всех колонок в таблице
    expected_columns = ['Фото', 'Имя', 'Порода', 'Возраст','']
    table_head = driver.find_element(By.CSS_SELECTOR, '.table thead tr')
    columns = table_head.find_elements(By.TAG_NAME, 'th')
    column_names = [column.text for column in columns]
    assert column_names == expected_columns


