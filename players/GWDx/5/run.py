from selenium import webdriver
from selenium.webdriver.common.by import By
import re

# firefox
driver = webdriver.Firefox()

driver.get('http://202.38.93.111:10047')

# input type="text"
inputBox = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
inputBox.send_keys(
    '1:MEUCIQC24dB6B24/LDr2O+4cifbzOEFDbkXg3hJIqTXuuvpa1QIgbzMM/F0uUmYIudtM6qEDvOpEHbtTZjSjTWMcA5zhnos= ')

# input type="submit"
driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

# click img-fluid
driver.find_element(By.CLASS_NAME, 'img-fluid').click()

# # see source code
# with open('1.html', 'w') as f:
#     f.write(driver.page_source)

# <label for="captcha1">160092426831461187501631690638141489463+53014117698106737620695077701380624357 的结果是？</label>
#           <input type="text" class="form-control" id="captcha1" name="captcha1" placeholder="请输入结果">
# solve captcha1-3
for i in range(3):
    # get captcha
    captcha = driver.find_element(By.CSS_SELECTOR, 'label[for="captcha' + str(i + 1) + '"]').text
    print(captcha)
    # get result
    result = re.search(r'(.+) 的结果是', captcha).group(1)
    ans = eval(result)
    print(ans)
    # input result
    driver.find_element(By.CSS_SELECTOR, 'input[name="captcha' + str(i + 1) + '"]').send_keys(ans)

# <button type="submit" class="btn btn-primary" id="submit">提交</button>
# click submit
driver.find_element(By.ID, 'submit').click()
