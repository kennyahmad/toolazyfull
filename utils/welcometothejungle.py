import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoAlertPresentException


def login(driver, mail,info,error):
    """Se connecter au site welcometothejungle.com"""
    info(f"Connexion avec {mail['mail']} sur welcometothejungle.com")
    driver.get("https://welcometothejungle.com/fr/")
    time.sleep(3)

    try:
        alert = driver.switch_to.alert
        alert.accept()
    except NoAlertPresentException:
        pass

    # Gestion du pop-up pour les cookies
    try:
        cookie_div = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "axeptio_overlay")))
        cookie_button = cookie_div.find_element(By.ID, "axeptio_btn_acceptAll")
        driver.execute_script("arguments[0].click();", cookie_button)
    except TimeoutException:
        return login(driver, user)
    except NoSuchElementException:
        pass

    # Login
    login_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/header/div/div[3]/div[2]/button[2]")))
    login_button.click()

    time.sleep(5)

    try:
        # email_input = driver.find_element(By.ID,"email_login")
        email_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "email_login")))
        email_input.send_keys(mail['mail'])
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys(mail['websites']['welcometothejungle']['password'])
        password_input.send_keys(Keys.ENTER)
    except NoSuchElementException:
        a = 0

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "folder")))
        return True
    except TimeoutException:
        # driver.refresh()
        return False


def logout(driver,info,error):
    time.sleep(1)
    info("Déconnexion")
    try:
        menu_button = driver.find_element(By.CSS_SELECTOR, "i.sc-kmASHI.inkvsG")
        driver.execute_script("arguments[0].click();", menu_button)
        logout_button = driver.find_element(By.NAME, "log_out")
        driver.execute_script("arguments[0].click();", logout_button)
    except NoSuchElementException:
        driver.delete_all_cookies()
        driver.refresh()
    time.sleep(1)


def recherche(driver, link,info,error):
    """Effectuer une recherche"""
    # Recherche
    driver.get(link)

    try:
        alert = driver.switch_to.alert
        alert.accept()
    except NoAlertPresentException:
        pass

    # Séléction des résultats de recherches
    try:
        jobs_results = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//ol[@data-testid='jobs_index-search-results']")))
    except TimeoutException:
        return False
    jobs = jobs_results.find_elements_by_class_name("ais-Hits-list-item")
    links = [job.find_element(By.TAG_NAME, "a").get_attribute("href") for job in jobs]

    return list(set(links))


def postuler(driver, link,info,error,mail):
    """Postuler pour un job"""
    driver.get(link)

    try:
        alert = driver.switch_to.alert
        alert.accept()
    except NoAlertPresentException:
        pass

    try:
        apply_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//button[@data-testid='job_sticky_left-button-apply']")))
    except TimeoutException as tex:
        apply_button = None

    # Si le le formulaire est sur le site www.welcometothejungle.com

    if apply_button:
        driver.execute_script("arguments[0].click();", apply_button)

        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "legend")))
        except TimeoutException:
            pass

        try:
            cover_letter = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "cover_letter")))
            cover_letter.send_keys(mail['websites']['welcometothejungle']['letter'])
            time.sleep(1)
        except NoSuchElementException:
            pass

        try:
            poste = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "subtitle")))
            if not poste.get_attribute("value"):
                poste.send_keys(mail['websites']['welcometothejungle']['possition'])
            time.sleep(1)
        except NoSuchElementException:
            pass

        terms = driver.find_element(By.ID, "terms")
        driver.execute_script("arguments[0].click();", terms)

        consent = driver.find_element(By.ID, "consent")
        driver.execute_script("arguments[0].click();", consent)

        submit_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='apply-form-submit']")))
        submit_button = driver.find_element(By.XPATH, "//button[@data-testid='apply-form-submit']")
        driver.execute_script("arguments[0].click();", submit_button)
        time.sleep(2)

        try:
            back_to_search_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@class='sc-ZqGJI fcbTIk']")))
            back_to_search_button = driver.find_element(By.XPATH, "//button[@class='sc-ZqGJI fcbTIk']")
            driver.execute_script("arguments[0].click();", back_to_search_button)
        except NoSuchElementException:
            submit_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='apply-form-submit']")))
            submit_button = driver.find_element(By.XPATH, "//button[@data-testid='apply-form-submit']")
            if submit_button:
                return 'Erreur'

        try:
            WebDriverWait(driver, 20).until(
                EC.visibility_of_any_elements_located((By.CLASS_NAME, "ais-SearchBox-form")))
            return "Postulé"
        except TimeoutException:
            return "Non postulé"
        # time.sleep(1)
    else:
        return "Page hors site welcometothejungle"
