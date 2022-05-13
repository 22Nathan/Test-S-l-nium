

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, WebDriverException, StaleElementReferenceException, TimeoutException, ElementNotInteractableException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.service import Service

import time
import csv

options = webdriver.EdgeOptions()
options.add_experimental_option( 'excludeSwitches', ['enable-logging'] )

driver = webdriver.Edge(options=options)

# options = webdriver.ChromeOptions()
# options.add_experimental_option( 'excludeSwitches', ['enable-logging'] )
# driver = webdriver.Chrome( "C:\Program Files\Google\Chrome\Application\chrome.exe")



def closeFile():
    try:
        #with open(csvPathFile) as csv:
            #with open('./feuilleResultats.md', 'w') as f_result:
                #csvReader = csv.reader( csv, delimiter=';' )
                pass
    finally:
        #f_result.close()
        #csv.close()  
        driver.quit()                




#################################################################
###########            CREER LES COMPTES             ############
#################################################################
def test_create_account():

    # OUVRE LE SITE ET REFUSE LES COOKIES
    def tca_run_pre():
        try:
            driver.get("https://glisshop.com")
            time.sleep(3)
            elemCloseCookie = driver.find_element(By.XPATH, "//button[@id='tarteaucitronAllDenied2']")
            elemCloseCookie.click()
            msg = '[x] pré-requis - success <br />' ; f_result.write( msg + '\n')
            return True
        except NoSuchElementException:
            msg = '[x] pré-requis - failed <br />' ; f_result.write( msg + '\n')
            return False

    # OUVRE LE SITE
    def tca_open_site():
        try:
            msg = '[x] open site - run <br />' ; f_result.write( msg + '\n')
            driver.get("https://glisshop.com")
            msg = '[x] open site - success <br />' ; f_result.write( msg + '\n')  
            return True
        except:
            msg = '[x] open site - failed <br />' ; f_result.write( msg + '\n')
            return False

    # OUVRIR L'ONGLET POUR CRÉER UN COMPTE
    def tca_open_account():
        try:
            msg = '[x] open account - run <br />' ; f_result.write( msg + '\n')
            elemAccount = driver.find_element(By.XPATH, "//a[@class='header_link d-block']")
            elemAccount.click()
            msg = '[x] open account - success <br />' ; f_result.write( msg + '\n')
            return True   
        except NoSuchElementException :
            msg = '[x] open account - failed <br />' ; f_result.write( msg + '\n')
            return False

    # REMPLIR LE FORMULAIRE D'INSCRIPTION
    def tca_fill_form():

        def tca_fill_form_email():
            try:
                msg = '[x] fill form - run <br />' ; f_result.write( msg + '\n')
                elemInputEmail = driver.find_element(By.ID, "rbs-user-create-account-email")
                elemInputEmail.send_keys( row[0] )
                time.sleep(1.5)
                try:
                    tempvar2 = driver.find_element(By.XPATH, '//p[contains( text() , "Cette adresse e-mail n\'est pas valide." )]')
                    if tempvar2.get_attribute('class') == "text-danger" :
                        msg = '     [x] - fill email - failed -> Email invalid <br /><br />' ; f_result.write( msg + '\n')

                        try:
                            driver.get_screenshot_as_file('./screenshot/emailNotValid.png')
                            f_result.write( '![alt text](./screenshot/emailNotValid.png)' )
                        except:
                            pass

                        return False
                except NoSuchElementException:
                    try:
                        tempvar1 = driver.find_element(By.XPATH, '//p[contains( text() , "Ce champ doit contenir une adresse e-mail valide" )]')
                        if tempvar1.get_attribute('class') == "text-danger" :
                            msg = '     [x] - fill email - failed -> Email invalid <br /><br />' ; f_result.write( msg + '\n')

                            try:
                                driver.get_screenshot_as_file('./screenshot/emailNotValid2.png')
                                f_result.write( '![alt text](./screenshot/emailNotValid2.png)' )
                            except:
                                pass

                            return False
                        else:
                            try:
                                tempvar3 = driver.find_element(By.XPATH, '//p[contains( text() , "Cette adresse e-mail est déjà utilisée." )]')
                                if tempvar3.get_attribute('class') == "text-danger" :
                                    msg = '     [x] - fill email - failed -> Email already used <br /><br />' ; f_result.write( msg + '\n')

                                    try:
                                        driver.get_screenshot_as_file('./screenshot/emailAlreadyUsed.png')
                                        f_result.write( '![alt text](./screenshot/emailAlreadyUsed.png)' )
                                    except:
                                        pass

                                    return False
                            except NoSuchElementException:    
                                msg = '     [x] - fill email - success <br />' ; f_result.write( msg + '\n')
                                return True
                    except NoSuchElementException:
                        msg = '[x] fill form - failed -> fill email failed <br />' ; f_result.write( msg + '\n')
                        return False
            except NoSuchElementException :
                msg = '[x] fill form - failed -> fill email failed <br />' ; f_result.write( msg + '\n')
                return False

        def tca_fill_form_password():
            try:
                tempvar6661 = driver.find_elements(By.XPATH, "//button[@title='Voir le mot de passe']")[0]  
                driver.execute_script( "arguments[0].click();" , tempvar6661 )
                elemInputPassword = driver.find_element(By.ID, "rbs-user-create-account-password")
                elemInputPassword.send_keys( row[1] )

                tempvar6662 = driver.find_elements(By.XPATH, "//button[@title='Voir le mot de passe']")[1]
                driver.execute_script( "arguments[0].click();" , tempvar6662 )
                elemInputConfPassword = driver.find_element(By.ID, "rbs-user-create-account-confirm-password")
                elemInputConfPassword.send_keys( row[2] )

                time.sleep(1.5)
                try:
                    tempvar1 = driver.find_element(By.XPATH, '//p[contains( text() , "Le mot de passe et sa confirmation ne correspondent pas." )]')
                    if tempvar1.get_attribute('class') == "text-danger" :
                        msg = '     [x] - fill password - failed - passwords does not match together <br /><br />' ; f_result.write( msg + '\n')

                        try:
                            driver.get_screenshot_as_file('./screenshot/passwordsDoesNotMatch.png')
                            f_result.write( '![alt text](./screenshot/passwordsDoesNotMatch.png)' )
                        except:
                            pass

                        return False 
                    else:
                        msg = '     [x] - fill password - success <br />' ; f_result.write( msg + '\n')
                        return True 
                except NoSuchElementException:
                    msg = '[x] fill form - failed -> fill password failed <br />' ; f_result.write( msg + '\n')
                    return False
            except NoSuchElementException:
                msg = '[x] fill form - failed -> fill password failed <br />' ; f_result.write( msg + '\n')
                return False

        if tca_fill_form_email():
            if tca_fill_form_password():
                msg = '[x] fill form - success <br />' ; f_result.write( msg + '\n')
                return True          

        msg = '[x] fill form - failed <br />' ; f_result.write( msg + '\n')
        return False             

    # APPUYER SUR LE BOUTON DE SUBMITION
    def tca_click_submit():
        try:
            elemBtnSendForm = driver.find_element(By.XPATH, "//button[@class='btn btn_l btn_l1 btn_full btn_l1_quaternary']")
            if elemBtnSendForm.get_attribute('disabled'):
                msg = '[x] click button submit - failed - submit button is disabled <br />' ; f_result.write( msg + '\n')
                return False
            else :    
                #elemBtnSendForm.click()
                driver.execute_script( "arguments[0].click();" , elemBtnSendForm )
                msg = '[x] click button submit - success <br />' ; f_result.write( msg + '\n')
                return True
        except NoSuchElementException:
            msg = '[x] click button submit - failed <br />' ; f_result.write( msg + '\n')
            return False

    # VERIFIER SI LES PASSWORDS SONT VALIDES
    def tca_check_password():
        time.sleep(1.5)
        try:
            driver.find_element(By.XPATH, '//p[contains( text() , "Le mot de passe doit comporter 8 caractères" )]')
            msg = '[x] check password - failed -> passwords not in format <br /><br />' ; f_result.write( msg + '\n') 

            try:
                driver.get_screenshot_as_file('./screenshot/passwordNotInFormat.png')
                f_result.write( '![alt text](./screenshot/passwordNotInFormat.png)' )
            except:
                pass

            return False
        except NoSuchElementException :
            msg = '[x] check password - success <br />' ; f_result.write( msg + '\n')                                                        
            return True

    # VERIFIER SI LE COMTPE A ETE CREE
    def tca_check_account_created():
        msg = '[x] send form - run <br />' ; f_result.write( msg + '\n')
        try:
            if driver.find_element( By.XPATH, '//p[contains( text() , "Votre compte a bien été créé." )]' ):                                                      
                msg = '[x] send form - success -> Compte créé <br /><br />' ; f_result.write( msg + '\n')
                
                try:
                    driver.get_screenshot_as_file('./screenshot/accountCreated.png')
                    f_result.write( '![alt text](./screenshot/accountCreated.png)' )
                except:
                    pass
                
                time.sleep(2)
                return True
        except NoSuchElementException:
            msg = '[x] send form - failed <br />' ; f_result.write( msg + '\n')
            return False


    try:
        with open('./dataCreateAccount.csv') as csvCreateAccount:
            with open('./feuilleResultats.md', 'w', encoding='utf-8') as f_result:
                csvReader = csv.reader( csvCreateAccount, delimiter=';' )
                msg = "[x] pré-requis - run <br />" ; f_result.write( msg + '\n')
                #____________________________________
                if tca_run_pre(): 
                #____________________________________
                    for row in csvReader:
                        msg = "<br /><br /><br /><br />\n\n\n\n\n``_____________________________________________``"
                        f_result.write( msg + '\n<br />') ; 
                        msg = "**####################################**\n       <br />" + \
                              "**#########** CREER LES COMPTES **##########**\n <br />" + \
                              "**####################################**         <br />"
                        f_result.write( msg + '\n') ; 
                        msg = "Champs : \n# [Email, Password, ConfPassword]" ; f_result.write( msg + '\n')
                        msg = "Début pour les données :" ; f_result.write( msg + '\n')
                        f_result.write( '# ' + str(row) + '\n\n')
                        #____________________________________
                        if tca_open_site():
                            if tca_open_account():
                                if tca_fill_form():
                                    if tca_click_submit():
                                        if tca_check_password():
                                            tca_check_account_created()
                        #____________________________________      
    except:
        msg = 'Erreur -> fichier(s) non chargé(s) <br />' ; f_result.write( msg + '\n')



#################################################################
###########         CONNECTER LES COMPTES            ############
#################################################################
def test_login_account( seDeconnecter , modifier ):

    # OUVRE LE SITE ET REFUSE LES COOKIES
    def tla_run_pre():
        try:
            driver.get("https://glisshop.com")
            driver.maximize_window()
            time.sleep(5)
            elemCloseCookie = driver.find_element(By.XPATH, "//button[@id='tarteaucitronAllDenied2']")
            #elemCloseCookie.click()
            driver.execute_script( "arguments[0].click();" , elemCloseCookie )
            msg = '[x] pré-requis - success <br />' ; f_result.write( msg + '\n')
            return True
        except NoSuchElementException:
            msg = '[x] pré-requis - failed <br />' ; f_result.write( msg + '\n')
            return False

    # OUVRE LE SITE
    def tla_open_site():
        try:
            msg = '[x] open site - run <br />' ; f_result.write( msg + '\n')
            driver.get("https://glisshop.com")
            msg = '[x] open site - success <br />' ; f_result.write( msg + '\n')  
            return True
        except:
            msg = '[x] open site - failed <br />' ; f_result.write( msg + '\n')
            return False

    # OUVRIR L'ONGLET POUR SE CONNECTER
    def tla_open_account():
        try:
            msg = '[x] open account sign in - run <br />' ; f_result.write( msg + '\n')
            elemAccount = driver.find_element(By.XPATH, "//a[@class='header_link d-block']")
            #elemAccount.click() 
            driver.execute_script( "arguments[0].click();" , elemAccount )
            try:
                elemLog = driver.find_element(By.XPATH, '//a[contains( text() , "Déjà client" )]')
                elemLog.click()
                msg = '[x] open account sign in - success <br />' ; f_result.write( msg + '\n')
                return True  
            except NoSuchElementException:
                msg = '[x] open account sign in - failed <br />' ; f_result.write( msg + '\n')
                return False     
        except NoSuchElementException :
            msg = '[x] open account sign in - failed <br />' ; f_result.write( msg + '\n')
            return False

    # REMPLIR LES CHAMPS 
    def tla_fill_form():
        try:
            msg = "[x] fill form - run <br />" ; f_result.write( msg + '\n')
            elemEmail = driver.find_element( By.XPATH, '//input[@placeholder="Saisissez votre adresse e-mail *"]' )
            elemEmail.send_keys(row[0])
            elemPassw = driver.find_element( By.XPATH, '//input[@placeholder="Votre mot de passe *"]' )
            elemPassw.send_keys(row[1])
            elemShowPassw = driver.find_element( By.XPATH, '//button[@title="Voir le mot de passe"]' )
            #elemShowPassw.click()
            driver.execute_script( "arguments[0].click();" , elemShowPassw )
            msg = "    [x] - fill form - Email filled <br />"    ; f_result.write( msg + '\n')
            msg = "    [x] - fill form - Password filled <br />" ; f_result.write( msg + '\n')
            msg = "[x] fill form - success <br />" ; f_result.write( msg + '\n')
            return True
        except NoSuchElementException:
            msg = "[x] fill form - failed <br />" ; f_result.write( msg + '\n')
            return False

    # APPUYER SUR LE BOUTON DE SUBMITION
    def tla_submit_button():
        try:
            elemBtnSendForm = driver.find_element(By.XPATH, "//button[@class='btn btn_l btn_l1 btn_full btn_l1_quaternary']")
            if elemBtnSendForm.get_attribute('disabled'):
                msg = '[x] click button submit - failed - submit button is disabled <br />' ; f_result.write( msg + '\n')
                return False
            else :    
                #elemBtnSendForm.click()
                driver.execute_script( "arguments[0].click();" , elemBtnSendForm )
                msg = '[x] click button submit - success <br />' ; f_result.write( msg + '\n')
                return True
        except NoSuchElementException:
            msg = '[x] click button submit - failed <br />' ; f_result.write( msg + '\n')
            return False

    # CHECK IF VALID
    def tla_check_form():
        time.sleep(1.5)
        try:
            driver.find_element(By.XPATH, '//p[contains( text() , "L\'identifiant et le mot de passe ne correspondent pas." )]')
            msg = '[x] check data sent - failed -> id and password does not match <br /><br />' ; f_result.write( msg + '\n') 

            try:
                driver.get_screenshot_as_file('./screenshot/loginsDoesNotMatch.png')
                f_result.write( '![alt text](./screenshot/loginsDoesNotMatch.png)' )
            except:
                pass

            return False
        except NoSuchElementException :
            msg = '[x] check data sent - success <br />' ; f_result.write( msg + '\n')   
            msg = '[x] user is logged successfuly <br />' ; f_result.write( msg + '\n')                                                      
            return True


    #################################################################
    ###########         DECONNECTER LES COMPTES          ############
    #################################################################
        # PRÉREQUIS ËTRE CONNECTÉ
    def test_logout_account():
        time.sleep(1)
        try:
            f_result.write('\n')
            msg = "**#########################################**\n <br />" + \
                  "**########**   DÉCONNECTER LES COMPTES   **##########**\n <br />" + \
                  "**#########################################** <br />"
            f_result.write( msg + '\n')
            msg = '[x] open site - run <br />' ; f_result.write( msg + '\n')
            driver.get("https://glisshop.com")
            time.sleep(2)
            msg = '[x] open site - success <br />' ; f_result.write( msg + '\n')
            msg = '[x] open account - run <br />' ; f_result.write( msg + '\n')
            elemAcc = driver.find_element( By.XPATH, '//a[@href="mon-compte/mes-informations.html"]' )
            #elemAcc.click()
            driver.execute_script( "arguments[0].click();" , elemAcc )
            msg = '[x] open account - success <br />' ; f_result.write( msg + '\n')
            time.sleep(2)
            try:
                msg = '[x] account click logout - run <br />' ; f_result.write( msg + '\n')
                elemLogout = driver.find_element( By.XPATH, '//a[@title="Déconnexion"]' )
                #elemLogout.click()
                driver.execute_script( "arguments[0].click();" , elemLogout )
                msg = '[x] account click logout - success <br />' ; f_result.write( msg + '\n')
                return True
            except NoSuchElementException:
                msg = '[x] account click logout - failed <br />' ; f_result.write( msg + '\n')
                return False
        except NoSuchElementException:
            msg = '     [x] open account - failed <br />' ; f_result.write( msg + '\n')
            return False

    #################################################################
    ###########         MODIFIER LE COMPTE               ############
    #################################################################
        # PRÉREQUIS ËTRE CONNECTÉ
    def test_update_account():


        # OUVRE LE SITE
        def tua_open_file():
            try:
                msg = '[x] open site - run <br />' ; f_result.write( msg + '\n')
                driver.get("https://glisshop.com")
                time.sleep(2)
                msg = '[x] open site - success <br />' ; f_result.write( msg + '\n')
                return True
            except:
                msg = '[x] open site - failed <br />' ; f_result.write( msg + '\n')
                return False

        # CLICK SUR L'ONGLET DU COMPTE
        def tua_open_tab_account():
            try:
                msg = '[x] open account tab - run <br />' ; f_result.write( msg + '\n')
                elemTab = driver.find_element(By.XPATH, "//a[@href='mon-compte/mes-informations.html']")
                #elemTab.click()
                driver.execute_script( "arguments[0].click();" , elemTab )
                msg = '[x] open account tab - success <br />' ; f_result.write( msg + '\n')
                return True
            except NoSuchElementException:
                msg = '[x] open account tab - failed <br />' ; f_result.write( msg + '\n')
                return False

        # CLICK SUR L'ONGLET ACCUEIL DU COMPTE
        def tua_open_tab_home():
            try:
                msg = '[x] open accueil tab - run <br />' ; f_result.write( msg + '\n')
                elemAcc = driver.find_element(By.XPATH, "//a[@title='ACCUEIL']")
                #elemAcc.click()
                driver.execute_script( "arguments[0].click();" , elemAcc )
                msg = '[x] open accueil tab - success <br />' ; f_result.write( msg + '\n')
                return True
            except NoSuchElementException:
                msg = '[x] open accueil tab - failed <br />' ; f_result.write( msg + '\n')
                return False        

        # CLICK SUR LE BOUTON MODIFIER
        def tua_click_button_modif():
            try:
                time.sleep(1)
                msg = '[x] click modifier button - run <br />' ; f_result.write( msg + '\n')


                elemClick = driver.find_element(By.XPATH, "//button[@data-ng-click='openEdit()']")
                driver.execute_script( "arguments[0].click();" , elemClick )
                #elemClick.click()
                #wait = WebDriverWait(driver, 7)
                #wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Next')]"))).click()
                time.sleep(2)

                msg = '[x] click modifier button - success <br />' ; f_result.write( msg + '\n') 
                return True          
            except NoSuchElementException:
                msg = '[x] click modifier button - failed <br />' ; f_result.write( msg + '\n')
                return False

        # FILL FORM
        def tua_fill_form_account():
            msg = '[x] fill account info - run <br />' ; f_result.write( msg + '\n')
            # f_result.write( '\n\n' + str(csvReader2[0]) + '\n\n' )
            # print( '\n\n' + str(csvReader2[0]) + '\n\n' )
            # print( '\n\n' )

            def tua_fill_prenom():
                try:
                    msg = ' ->  [x] fill prénom - run <br />' ; f_result.write( msg + '\n')
                    elemP = driver.find_element(By.XPATH, "//input[@placeholder='Prénom']")
                    elemP.clear()
                    elemP.send_keys(row2[0])
                    msg = ' ->  [x] fill prénom - success <br />' ; f_result.write( msg + '\n')
                    return True               
                except NoSuchElementException:
                    msg = ' ->  [x] fill prénom - failed <br />' ; f_result.write( msg + '\n')
                    return False

            def tua_fill_nom():
                try:
                    msg = ' ->  [x] fill nom - run <br />' ; f_result.write( msg + '\n')
                    elemP = driver.find_element(By.XPATH, "//input[@placeholder='Nom']")
                    elemP.clear()
                    elemP.send_keys(row2[1])
                    msg = ' ->  [x] fill nom - success <br />' ; f_result.write( msg + '\n')
                    return True
                except NoSuchElementException:
                    msg = ' ->  [x] fill nom - failed <br />' ; f_result.write( msg + '\n')
                    return False

            def tua_fill_phone():
                try:
                    msg = ' ->  [x] fill phone number - run <br />' ; f_result.write( msg + '\n')
                    elemP = driver.find_element(By.XPATH, "//input[@placeholder='Téléphone portable pour la livraison *']")
                    elemP.clear()
                    elemP.send_keys(row2[2])
                    msg = ' ->  [x] fill phone number - success <br />' ; f_result.write( msg + '\n')
                    return True
                except NoSuchElementException:
                    msg = ' ->  [x] fill phone number - failed <br />' ; f_result.write( msg + '\n')
                    return False

            def tua_fill_anniv():
                try:
                    msg = ' ->  [x] fill anniversary - run <br />' ; f_result.write( msg + '\n')
                    elemP = driver.find_element(By.XPATH, '//input[@placeholder="Date d\'anniversaire"]')
                    elemP.clear()
                    elemP.send_keys(row2[3])
                    msg = ' ->  [x] fill anniversary - success <br />' ; f_result.write( msg + '\n')
                    return True
                except NoSuchElementException:
                    msg = ' ->  [x] fill anniversary - failed <br />' ; f_result.write( msg + '\n')
                    return False

            def tua_fill_pseudo():
                try:
                    msg = ' ->  [x] fill pseudo - run <br />' ; f_result.write( msg + '\n')
                    elemP = driver.find_element(By.XPATH, "//input[@placeholder='Pseudonyme']")
                    elemP.clear()
                    elemP.send_keys(row2[4])
                    msg = ' ->  [x] fill pseudo - success <br />' ; f_result.write( msg + '\n')
                    return True
                except NoSuchElementException:
                    msg = ' ->  [x] fill pseudo - failed <br />' ; f_result.write( msg + '\n')
                    return False

            if tua_fill_prenom():
                if tua_fill_nom():
                    if tua_fill_phone():
                        if tua_fill_anniv():
                            if tua_fill_pseudo():
                                msg = '[x] fill account info - success <br />' ; f_result.write( msg + '\n')
                                time.sleep(5)
                                return True

            msg = '[x] fill account info - failed <br />' ; f_result.write( msg + '\n')
            return False                    

        # CLICK BTN UPDATE
        def tua_click_btn_update():
            try:
                msg = '[x] click update button - run <br />' ; f_result.write( msg + '\n')
                elemP = driver.find_element(By.XPATH, "//button[@data-ng-click='saveAccount()']")
                if elemP.get_attribute('disabled'):
                    msg = '[x] click update button - failed -> button disabled <br />' ; f_result.write( msg + '\n')
                    return False
                else:
                    #elemP.click()
                    driver.execute_script( "arguments[0].click();" , elemP )
                    msg = '[x] click update button - success <br />' ; f_result.write( msg + '\n')
                    msg = '[x] account updated - success <br /><br />' ; f_result.write( msg + '\n')
                    time.sleep(0.5)

                    try:
                        driver.get_screenshot_as_file('./screenshot/accountUpdated.png')
                        f_result.write( '![alt text](./screenshot/accountUpdated.png)' )
                    except:
                        pass


                    time.sleep(1)
                    return True
            except NoSuchElementException:
                msg = '[x] click update button - failed -> button not found <br />' ; f_result.write( msg + '\n')
                return False    

        time.sleep(1)
        try:
            with open('./dataUpdateAccount.csv') as csvU:
                csvReader2 = csv.reader( csvU, delimiter=';' )
                f_result.write('\n')
                msg = "**#########################################**\n <br />" + \
                      "**#########**     MODIFIER LES COMPTES    **###########**\n <br />" + \
                      "**#########################################** <br />"
                f_result.write( msg + '\n')

                for row2 in csvReader2:

                    msg = "Champs : \n# [Prénom, Nom, Pseudo, Téléphone, dateNaissance]" ; f_result.write( msg +'\n')
                    msg = "Début pour les données :" ; f_result.write( msg + '\n')
                    f_result.write( '# ' + str( row2 ) + '\n\n' )
                    if tua_open_file():
                        if tua_open_tab_account():
                            if tua_open_tab_home():
                                if tua_click_button_modif():
                                    if tua_fill_form_account():
                                        if tua_click_btn_update():
                                            msg = "[x] account updated successfuly <br />" ; f_result.write( msg + '\n')
                                            return True 
                    return False
        except:
            msg = "[x] account update failed <br />" ; f_result.write( msg + '\n')   
            return False                             






    try:
        with open('./dataConnectionAccount.csv') as csvConnectAccount:
            with open('./feuilleResultats.md', 'w', encoding='utf-8') as f_result:
                csvReader = csv.reader( csvConnectAccount, delimiter=';' )
                msg = "[x] pré-requis - run <br />" ; f_result.write( msg + '\n')
                #____________________________________
                if tla_run_pre(): 
                #____________________________________
                    i = 0
                    for row in csvReader:
                        msg = "<br /><br /><br /><br />\n\n\n\n\n``_____________________________________________``\n"
                        f_result.write( msg + '\n')
                        msg = "**#########################################**\n <br />" + \
                              "**#########**   CONNECTER LES COMPTES    **##########**\n <br />" + \
                              "**#########################################** <br />"
                        f_result.write( msg + '\n') ; msg = "Champs : \n# [Email, Password]"
                        f_result.write( msg + '\n') ; msg = "Début pour les données :"
                        f_result.write( msg + '\n')
                        f_result.write( '# ' + str(row) + '\n\n')
                        #____________________________________
                        if tla_open_site():
                            if tla_open_account():
                                if tla_fill_form():
                                    if tla_submit_button():
                                        if tla_check_form():
                                            if modifier and bool(modifier):
                                                test_update_account()
                                            if seDeconnecter and bool(seDeconnecter):
                                                test_logout_account()  
                        i = i+1                    
                        #____________________________________
    except:
        msg = 'Erreur -> fichier(s) non chargé(s) <br />' ; f_result.write( msg + '\n')  



#################################################################
###########           RECHERCHER ARTICLES            ############
#################################################################
def test_find_article( addToCart , removeToCart , order ):

    #################################################################
    ###########         AJOUTER AU PANIER                ############
    #################################################################
    def test_add_cart():
        try:
            time.sleep(1)
            msg = "-[x] click button add to cart - run <br />" ; f_result.write( msg + '\n' )

            elemtemp = driver.find_element( By.XPATH, '//button[ @data-ng-click="goToCart()" ]' )
            driver.execute_script( "arguments[0].click();" , elemtemp )
            time.sleep(1)

            elemV = driver.find_element( By.XPATH, '//button[ @data-ng-click="addProducts()" ]' )
            driver.execute_script( "arguments[0].click();" , elemV )

            time.sleep(2)
            msg = "-[x] click button add to cart - success <br />" ; f_result.write( msg + '\n' )
            try:
                time.sleep(1)
                msg = "--[x] click button view cart - run <br />" ; f_result.write( msg + '\n' )
                elemV = driver.find_element( By.XPATH, '//a[ contains( text() , "Voir mon panier" ) ]' )
                #elemV.click()
                driver.execute_script( "arguments[0].click();" , elemV )
                msg = "--[x] click button view cart - success <br /><br />" ; f_result.write( msg + '\n' )

                time.sleep(1)

                try:
                    driver.get_screenshot_as_file('./screenshot/cartAdded.png')
                    f_result.write( '![alt text](./screenshot/cartAdded.png)' )
                except:
                    pass

                time.sleep(4)
            except NoSuchElementException:
                msg = "--[x] click button view cart - failed <br />" ; f_result.write( msg + '\n' )

        except WebDriverException:
            try:
                time.sleep(1)

                #f_result.write( '-[v] \n' )

                elemtemp = driver.find_element( By.XPATH, '//button[ @data-ng-click="goToCart()" ]' )
                driver.execute_script( "arguments[0].click();" , elemtemp )
                time.sleep(1)

                elemV = driver.find_element( By.XPATH, '//button[ @data-ng-click="addProducts()" ]' )
                driver.execute_script( "arguments[0].click();" , elemV )

                time.sleep(2)
                msg = "-[x] click button add to cart - success <br />" ; f_result.write( msg + '\n' )
                try:
                    time.sleep(1)
                    msg = "--[x] click button view cart - run <br />" ; f_result.write( msg + '\n' )
                    elemV = driver.find_element( By.XPATH, '//a[ contains( text() , "Voir mon panier" ) ]' )
                    #elemV.click()
                    driver.execute_script( "arguments[0].click();" , elemV )
                    msg = "--[x] click button view cart - success <br />" ; f_result.write( msg + '\n' )
                    time.sleep(1)

                    try:
                        driver.get_screenshot_as_file('./screenshot/cartAdded.png')
                        f_result.write( '![alt text](./screenshot/cartAdded.png)' )
                    except:
                        pass

                    time.sleep(4)
                except NoSuchElementException:
                    msg = "--[x] click button view cart - failed <br />" ; f_result.write( msg + '\n' )

            except WebDriverException:
                pass
        except NoSuchElementException:
            msg = "-[x] click button add to cart - failed <br />" ; f_result.write( msg + '\n' )


    #################################################################
    ###########         SUPPRIMER DU PANIER              ############
    #################################################################
    def test_delete_all_cart():
        try:
            time.sleep(4)
            msg = "-[x] click button delete to cart - run <br />" ; f_result.write( msg + '\n' )
            elemD = driver.find_elements( By.XPATH, '//button[@data-ng-click="remove()"]' )
            for e in elemD:
                #e.click()
                driver.execute_script( "arguments[0].click();" , e )
                time.sleep(4)
            msg = "-[x] click button delete to cart - success <br />" ; f_result.write( msg + '\n' )   
        except StaleElementReferenceException:
            elemD = driver.find_elements( By.XPATH, '//button[@data-ng-click="remove()"]' )
            for e in elemD:
                #e.click()
                driver.execute_script( "arguments[0].click();" , e )
                time.sleep(4)
            msg = "-[x] click button delete to cart - success <br />" ; f_result.write( msg + '\n' )  

            try:
                driver.get_screenshot_as_file('./screenshot/CartDeleted.png')
                f_result.write( '![alt text](./screenshot/CartDeleted.png)' )
            except:
                pass

        except NoSuchElementException:
            msg = "-[x] click button delete to cart - failed <br />" ; f_result.write( msg + '\n' )


    #################################################################
    ###########               COMMANDER                  ############
    #################################################################
    def test_order_command():



        try:

            msg = "[x] order cart products - run <br />" ; f_result.write( msg + '\n' )

            msg = "[x] click button accept terms and conditions - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , "//input[ @id='acceptTermsAndConditions' ]" )
            driver.execute_script( "arguments[0].click();" , elemQ )
            time.sleep(3)
            msg = "[x] click button accept terms and conditions - success <br />" ; f_result.write( msg + '\n' )

            msg = "[x] click button passer commande - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , '//a[ contains( text() , "Passer la commande" ) ]' )
            driver.execute_script( "arguments[0].click();" , elemQ )
            time.sleep(1)
            msg = "[x] click button passer commande - success <br />" ; f_result.write( msg + '\n' )

            msg = "-[x] set genre homme - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , "//input[ @id='gender_male_0' ]" )
            driver.execute_script( "arguments[0].click();" , elemQ )
            time.sleep(1)
            msg = "-[x] set genre homme - success <br />" ; f_result.write( msg + '\n' )

            msg = "-[x] set prénom - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , "//input[ @id='name_0' ]" )
            elemQ.send_keys( 'unPrénom' )
            msg = "-[x] set prénom - success <br />" ; f_result.write( msg + '\n' )

            msg = "-[x] set taille - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , "//input[ @id='size_0' ]" )
            elemQ.send_keys( '170' )
            msg = "-[x] set taille - success <br />" ; f_result.write( msg + '\n' )

            msg = "-[x] set poids - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , "//input[ @id='weight_0' ]" )
            elemQ.send_keys( '60' )
            msg = "-[x] set poids - success <br />" ; f_result.write( msg + '\n' )

            msg = "-[x] set pointure - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , "//input[ @id='foot_size_size_0' ]" )
            elemQ.send_keys( '40' )
            msg = "-[x] set pointure - success <br />" ; f_result.write( msg + '\n' )

            msg = "-[x] click mesure - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , "//input[ @id='foot_size_unit_fr_0' ]" )
            driver.execute_script( "arguments[0].click();" , elemQ )
            msg = "-[x] click mesure - success <br />" ; f_result.write( msg + '\n' )

            msg = "-[x] click save options - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , "//input[ @data-ng-click='saveOptions()' ]" )
            driver.execute_script( "arguments[0].click();" , elemQ )
            time.sleep(4)
            msg = "-[x] click save options - success <br />" ; f_result.write( msg + '\n' )

            msg = "-[x] click passer commande - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , '//a[ contains( text() , "Passer la commande" ) ]' )
            driver.execute_script( "arguments[0].click();" , elemQ )
            time.sleep(4)
            msg = "-[x] click passer commande - success <br />" ; f_result.write( msg + '\n' )




            msg = "-[x] Connection au compte - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , '//li[ contains( text() , " Déjà client " ) ]' )
            driver.execute_script( "arguments[0].click();" , elemQ )
            time.sleep(1)
            msg = "-[x] Connection au compte - success <br />" ; f_result.write( msg + '\n' )
            
            msg = "-[x] fill email - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , "//input[ @placeholder='Saisissez votre adresse e-mail *' ]" )
            elemQ.send_keys( 'aqwzsxedc@gmail.com' )
            msg = "-[x] fill email - success <br />" ; f_result.write( msg + '\n' )

            msg = "-[x] fill password - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , "//input[ @placeholder='Votre mot de passe *' ]" )
            elemQ.send_keys( 'aqwzsxedcA1+' )
            msg = "-[x] fill password - success <br />" ; f_result.write( msg + '\n' )
            time.sleep(2)

            msg = "-[x] Click button connexion au compte - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , '//button[ contains( text() , " Connexion à mon compte " ) ]' )
            driver.execute_script( "arguments[0].click();" , elemQ )
            time.sleep(3)
            msg = "-[x] Click button connexion au compte - success <br />" ; f_result.write( msg + '\n' )



            msg = "-[x] click set new adresse - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , '//button[ contains( text() , " Créer une nouvelle adresse " ) ]' )
            driver.execute_script( "arguments[0].click();" , elemQ )
            time.sleep(1)
            msg = "-[x] click set new adresse - success <br />" ; f_result.write( msg + '\n' )

            msg = "-[x] open country dropdown - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , "//button[@data-toggle='dropdown']" )
            driver.execute_script( "arguments[0].click();" , elemQ )
            msg = "-[x] open country dropdown - sucess <br />" ; f_result.write( msg + '\n' )

            msg = "-[x] choose country fr - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , "//span[@class = 'flag-icon flag-fr'] " )
            driver.execute_script( "arguments[0].click();" , elemQ )
            msg = "-[x] choose country fr - success <br />" ; f_result.write( msg + '\n' )

            try:
                msg = "-[x] set Nom - run <br />" ; f_result.write( msg + '\n' )
                elemQh = driver.find_element( By.XPATH , "//input[ @id='101868_627e4c7e4f551_lastname' ]" )
                time.sleep(1)
                elemQh.send_keys( 'unNom' )
                msg = "-[x] set Nom - success <br />" ; f_result.write( msg + '\n' )
            except ElementNotInteractableException as e:
                # msg = "-[x] set Nom - failed <br />" ; f_result.write( msg + '\n' )
                print(elemQ)
                print(elemQh)
                print(e)
                #elemQh.send_keys( 'unNom' )
                time.sleep(7)

            msg = "-[x] set Prénom - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , "//input[ @id='101868_627e4c7e4f551_firstname' ]" )
            elemQ.send_keys( 'unPrénom' )
            msg = "-[x] set Prénom - success <br />" ; f_result.write( msg + '\n' )

            msg = "-[x] set adresse - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , "//input[ @id='101868_627e4c7e4f551_street' ]" )
            elemQ.send_keys( '10 rue de Paris' )
            msg = "-[x] set adresse - success <br />" ; f_result.write( msg + '\n' )

            msg = "-[x] set code postal - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , "//input[ @id='101868_627e4c7e4f551_zipCode' ]" )
            elemQ.send_keys( '75000' )
            msg = "-[x] set code postal - success <br />" ; f_result.write( msg + '\n' )

            msg = "-[x] set ville - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , "//input[ @id='101868_627e4c7e4f551_locality' ]" )
            elemQ.send_keys( 'Paris' )
            msg = "-[x] set ville - success <br />" ; f_result.write( msg + '\n' )

            msg = "-[x] set téléphone - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , "//input[ @id='101868_627e4c7e4f551_phone' ]" )
            elemQ.send_keys( '0600000000' )
            msg = "-[x] set téléphone - success <br />" ; f_result.write( msg + '\n' )

            msg = "-[x] click valider les coordonnées - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , "//button[ contains( text() , 'Valider mes coordonnées' ) ] " )
            driver.execute_script( "arguments[0].click();" , elemQ )
            time.sleep(8)
            msg = "-[x] click valider les coordonnées - success <br />" ; f_result.write( msg + '\n' )

            msg = "-[x] click valider la livraison - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , "//button[ contains( text() , 'Valider la livraison' ) ] " )
            driver.execute_script( "arguments[0].click();" , elemQ )
            time.sleep(8)
            msg = "-[x] click valider la livraison - success <br />" ; f_result.write( msg + '\n' )

            msg = "-[x] set numéro cb - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , "//input[ @placeholder='Numéro de la carte *' ]" )
            elemQ.send_keys( '4890660016524221' )
            msg = "-[x] set numéro cb - success <br />" ; f_result.write( msg + '\n' )

            msg = "-[x] set cryptogramme cb - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , "//input[ @placeholder='Cryptogramme *' ]" )
            elemQ.send_keys( '002' )
            msg = "-[x] set cryptogramme cb - success <br />" ; f_result.write( msg + '\n' )

            msg = "-[x] set nom prénom cb - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , "//input[ @placeholder='Prénom Nom *' ]" )
            elemQ.send_keys( 'Regina Vise' )
            msg = "-[x] set nom prénom cb - success <br />" ; f_result.write( msg + '\n' )

            msg = "-[x] click button payer la commande - run <br />" ; f_result.write( msg + '\n' )
            elemQ = driver.find_element( By.XPATH , "//button[ contains( text() , ' Payer ma commande ' ) ] " )
            driver.execute_script( "arguments[0].click();" , elemQ )
            time.sleep(12)
            msg = "-[x] click button payer ma commande - success <br />" ; f_result.write( msg + '\n' )

            try:
                driver.get_screenshot_as_file('./screenshot/result.png')
                f_result.write( '![alt text](./screenshot/result.png)' )
            except:
                pass

        except NoSuchElementException:
            pass


    try:
        with open( './dataFindArticle.csv' ) as csvF:
            with open('./feuilleResultats.md', 'w', encoding='utf-8') as f_result:
                csvReader3 = csv.reader( csvF, delimiter=';' )

                driver.maximize_window()

                msg = "<br /><br /><br /><br />\n\n\n\n\n``_____________________________________________``"
                msg = "**######################################**\n <br />" + \
                      "**#########**     CHERCHER UN ARTICLE    **##########**\n <br />" + \
                      "**######################################**   <br />"
                f_result.write( msg + '\n')

                driver.get("https://glisshop.com")
                time.sleep(3)

                #les cookies
                elemCloseCookie = driver.find_element(By.XPATH, "//button[@id='tarteaucitronAllDenied2']")
                #elemCloseCookie.click()
                driver.execute_script( "arguments[0].click();" , elemCloseCookie )

                try:
                    elemP = driver.find_element( By.XPATH, "//input[@placeholder='Recherchez un produit, une marque,......']" )
                    elemP.clear()

                    for row3 in csvReader3:
                        elemP.send_keys(row3)
                        time.sleep(3)

                        msg = "Champs : \n# [Article]" ; f_result.write( msg + '\n' )
                        msg = "Début pour les données :\n# " + str(row3) ; f_result.write( msg + '\n\n' )
                        msg = "[x] Finding element - run <br />" ; f_result.write( msg + '\n')
                        try:
                            msg = "    [x] Fill search input - run <br />" ; f_result.write( msg + '\n' )
                            elemG = driver.find_element( By.XPATH, "//button[@title='Recherchez un produit, une marque,...']" ) 
                            #elemG.click()
                            driver.execute_script( "arguments[0].click();" , elemG )
                            msg = "    [x] Fill search input - success <br />" ; f_result.write( msg + '\n' )
                            msg = "[x] Finding element - success <br />" ; f_result.write( msg + '\n')
                            time.sleep(3)

                            try: 
                                msg = "[x] click the result - run <br />" ; f_result.write( msg + '\n' )
                                elemV = driver.find_element( By.XPATH, '//a[ @data-role="result-link" ]' )
                                driver.execute_script( "arguments[0].click();" , elemV )
                                #elemV.click()
                                msg = "[x] click the result - success <br />" ; f_result.write( msg + '\n' )
                                time.sleep(4)

                                if addToCart and bool(addToCart):
                                    f_result.write( '\n' )
                                    msg = "**########################################**\n <br />" + \
                                          "**#########**     AJOUTER UN ARTICLE     **##########**\n <br />" + \
                                          "**########################################** <br />"
                                    f_result.write( msg + '\n\n' )
                                    test_add_cart()
                                    if removeToCart and bool(removeToCart):
                                        f_result.write( '\n' )
                                        msg = "**########################################**\n <br />" + \
                                              "**#########**     SUPPRIMER LE PANNIER   **##########**\n <br />" + \
                                              "**########################################** <br />"
                                        f_result.write( msg + '\n\n')
                                        test_delete_all_cart()
                                    elif order and bool(order):
                                        f_result.write( '\n' )
                                        msg = "**########################################**\n <br />" + \
                                              "**#########**     COMMANDER LE PANNIER   **##########**\n <br />" + \
                                              "**########################################** <br />"
                                        f_result.write( msg + '\n\n')
                                        test_order_command()

                            except NoSuchElementException:
                                msg = "[x] click the result - failed <br />" ; f_result.write( msg + '\n' )

                        except NoSuchElementException:
                            msg = "    [x] Fill search input - failed <br />" ; f_result.write( msg + '\n' )
                            msg = "[x] Finding element - failed <br />" ; f_result.write( msg + '\n')

                except NoSuchElementException:
                    msg = "Erreur boutton chercher pas trouvé <br />" ; f_result.write( msg + '\n' )
    except:
        msg = 'Erreur -> fichier(s) non chargé(s) <br />' ; f_result.write( msg + '\n')











##### Créer les comptes #####
#test_create_account()


        ##### Connecter les comptes #####
#test_login_account( seDeconnecter = False , modifier = False )


        ##### Connecter et Déconnecter les comptes #####
test_login_account( seDeconnecter = True , modifier = False )


        ##### Connecter, Modifier et Déconnecter les comptes #####
#test_login_account( seDeconnecter = True , modifier = True )


        ##### Chercher un article #####
#test_find_article( addToCart = False , removeToCart = False , order = False )


        ##### Chercher un article , l'ajouter au panier #####
#test_find_article( addToCart = True , removeToCart = False , order = False )


        ##### Chercher un article , l'ajouter au panier , supprimer tous les articles #####
#test_find_article( addToCart = True , removeToCart = True , order = False )

        ##### #####
#test_find_article( addToCart = True , removeToCart = False , order = True )

        ##### Fermer les fichiers #####
closeFile()

