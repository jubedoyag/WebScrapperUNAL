# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException


def get_subjects():

    # se obtienen las credenciales del usuario (usuario y contrasena),
    # deben estar almacenadas en un archivo llamado 'credentials'
    # en la misma carpeta del archivo main.py (la raiz del proyecto).
    user_creds = open("credentials", "r")
    username = user_creds.readline().split(":")[1]
    passwd = user_creds.readline().split(":")[1]

    driver = webdriver.Chrome()
    url = ("https://autenticasia.unal.edu.co/oam/server/obrareq.cgi?encquery%3DsPivFLUJbDm04UJiqUMhoocO3oC1NAK19%2Ft"
           "%2F1DdT%2Fq2Ig6I8JoaqUiaZVz4ye52vW0sU9GVcG%2BH%2BpQUH0vTfrEo3qo9HwSXyfNTw%2FzBg26Oq5yPwm%2BYxMMVR8XgRu"
           "%2Fb2SzkQxQB2vncXHg%2BiPoVIR6gllWeQc6%2B%2F"
           "%2Fs8SFNkKGwa22Ze1M2Aku6b91PSixPgPrtznsmdjVf4irYDGreePm461kNHk3b3VP8WbjPpu4S4q71lna"
           "%2ByVxh0CpsgojZMyy5gLnc5VJzlky3eKJcz45tC5u%2Bx3Zd4foA%2F8F2ZYc2g%3D%20agentid%3DWTUNC_AWS%20ver%3D1"
           "%20crmethod%3D2&ECID-Context=1.0063X2AaV_m6MQRMyYbe6G0005vR002Smp%3BkXjE")
    driver.get(url)

    user_input_elem = driver.find_element(By.ID, "username")
    user_input_elem.clear()
    user_input_elem.send_keys(username)
    # user_input_elem.send_keys(Keys.RETURN)

    pass_input_elem = driver.find_element(By.ID, "password")
    pass_input_elem.clear()
    pass_input_elem.send_keys(passwd)
    pass_input_elem.send_keys(Keys.RETURN)

    # este es el grupo 'Proceso de inscripcion'
    panel_group_elems = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "af_panelAccordion_header-title"))
    )
    for panel_elem in panel_group_elems:
        try:
            if panel_elem.get_attribute("title") == "Proceso de inscripción":
                span_elem = panel_elem.find_element(By.TAG_NAME, "span")
                span_elem.click()

        except Exception as e:
            print(f"Error al filtrar/encontrar elemento 'panel' con texto \"Proceso de inscripcion\": {e}")

    # este es el enlace 'Asignaturas por insc.'
    a_link_elem = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[title=\"Asignaturas disponibles para cursar\"]"))
    )
    a_link_elem.click()

    # aqui se elige el plan de estudios
    plan_elem = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "pt1:r1:1:soc3::content"))
    )
    plan_options = plan_elem.find_elements(By.TAG_NAME, "option")
    for option in plan_options:
        chosen_value = "0"
        if option.get_attribute("value") == chosen_value:
            option.click()

    # aqui se elige el periodo academico
    period_elem = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "pt1:r1:1:soc2::content"))
    )
    period_options = period_elem.find_elements(By.TAG_NAME, "option")
    for option in period_options:
        chosen_value = "0"
        if option.get_attribute("value") == chosen_value:
            option.click()

    # aqui se elige el tipo de asign.
    subjs_elem = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "pt1:r1:1:soc4::content"))
    )
    subjs_options = subjs_elem.find_elements(By.TAG_NAME, "option")
    for option in subjs_options:
        chosen_value = "7"
        if option.get_attribute("value") == chosen_value:
            option.click()

    # aqui se elige la opcion de facultad o solo plan
    other_elem = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "pt1:r1:1:soc5::content"))
    )
    other_options = other_elem.find_elements(By.TAG_NAME, "option")
    for option in other_options:
        chosen_value = "0"
        if option.get_attribute("value") == chosen_value:
            option.click()

    # aqui se elige la sede en la cual buscar (o facultad)
    option_elem = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "option[value=\"28\"]"))
    )
    option_elem.click()

    # aqui se presiona el boton para mostrar las asignaturas
    a_link_elems = driver.find_elements(By.CSS_SELECTOR, "span a")
    for a_elem in a_link_elems:
        try:
            span_elem = a_elem.find_element(By.TAG_NAME, "span")
            if span_elem.text == "Mostrar":
                span_elem.click()

        except Exception as e:
            print(f"Error al encontrar/presionar elemento 'boton' \"Mostrar\": {e}")

    subjs_table_elem = WebDriverWait(driver, 25).until(
        EC.presence_of_element_located((By.CLASS_NAME, "af_table_data-body"))
    )

    # obtener las materias electivas
    subjects_elems = subjs_table_elem.find_elements(By.TAG_NAME, "tr")
    # lista donde guardamos las materias virtuales papu
    virtual_subjects = []
    for i in range(len(subjects_elems)):
        try:
            subj_elem = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "tr[_afrrk=\"" + str(i) + "\"]"))
            )
            a_subj_link = subj_elem.find_element(By.TAG_NAME, "a")
            a_subj_text = a_subj_link.text
            a_subj_link.click()

            # revisar si la materia es virtual ...
            table_title_elems = WebDriverWait(driver, 5).until(
                # EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h2.af_showDetailHeader_title-text0 "))
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table.p_AFDisclosed"))
            )

            # ... para algun grupo ofertado
            for title_elem in table_title_elems:
                header_elem = title_elem.find_element(By.CSS_SELECTOR, "h2.af_showDetailHeader_title-text0 ")
                header_text = header_elem.text.lower()
                if "telepresencial" in header_text or "virtual" in header_text:
                    virtual_subjects.append(a_subj_text)
                    break

        except TimeoutException as e:
            print(f"Elemento no encontrado en el tiempo dado: {e}")
        except NoSuchElementException as e:
            print(f"Elemento no encontrado: {e}")
        except ElementNotInteractableException as e:
            print(f"Elemento no interactuable: {e}")

        except Exception as e:
            print(f"Error inesperado en la electiva #{i+1} (elemento <tr> con atributo _afrrk={i}): {e}")

        finally:
            # volver a la pagina previa
            back_btn_elem = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.af_panelBox_center a"))
            )
            back_btn_elem.click()

    driver.close()

    for s in virtual_subjects:
        print(s)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_subjects()
