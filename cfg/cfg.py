from selenium import webdriver

### Chrome ###
options = webdriver.ChromeOptions()
options.set_capability("browserVersion", "92")
###

### Firefox ###
# options = webdriver.FirefoxOptions()
# options.set_capability("browserVersion", "88")
###

###############################################################################
# 1. Для локального вебдрайвера (закомментировать для удалённого вебдрайвера)
d = webdriver.Chrome(options=options)

# 2. Для удалённого вебдрайвера раскомментировать нужные опции и указать адрес
# options.set_capability("platformName", "LINUX")
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# d = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', options=options)
###############################################################################

d.implicitly_wait(60)
d.set_page_load_timeout(120)
d.set_script_timeout(60)
d.set_window_position(1, 1)
d.set_window_size(1920, 1080)
