

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, WebDriverException, StaleElementReferenceException
#from colorama import Fore, Back, Style
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
            msg = '[x] pré-requis - success' ; f_result.write( msg + '\n')
            return True
        except NoSuchElementException:
            msg = '[x] pré-requis - failed' ; f_result.write( msg + '\n')
            return False

    # OUVRE LE SITE
    def tca_open_site():
        try:
            msg = '[x] open site - run' ; f_result.write( msg + '\n')
            driver.get("https://glisshop.com")
            msg = '[x] open site - success' ; f_result.write( msg + '\n')  
            return True
        except:
            msg = '[x] open site - failed' ; f_result.write( msg + '\n')
            return False

    # OUVRIR L'ONGLET POUR CRÉER UN COMPTE
    def tca_open_account():
        try:
            msg = '[x] open account - run' ; f_result.write( msg + '\n')
            elemAccount = driver.find_element(By.XPATH, "//a[@class='header_link d-block']")
            elemAccount.click()
            msg = '[x] open account - success' ; f_result.write( msg + '\n')
            return True   
        except NoSuchElementException :
            msg = '[x] open account - failed' ; f_result.write( msg + '\n')
            return False

    # REMPLIR LE FORMULAIRE D'INSCRIPTION
    def tca_fill_form():

        def tca_fill_form_email():
            try:
                msg = '[x] fill form - run' ; f_result.write( msg + '\n')
                elemInputEmail = driver.find_element(By.ID, "rbs-user-create-account-email")
                elemInputEmail.send_keys( row[0] )
                time.sleep(1.5)
                try:
                    tempvar2 = driver.find_element(By.XPATH, '//p[contains( text() , "Cette adresse e-mail n\'est pas valide." )]')
                    if tempvar2.get_attribute('class') == "text-danger" :
                        msg = '     [x] - fill email - failed -> Email invalid' ; f_result.write( msg + '\n')
                        return False
                except NoSuchElementException:
                    try:
                        tempvar1 = driver.find_element(By.XPATH, '//p[contains( text() , "Ce champ doit contenir une adresse e-mail valide" )]')
                        if tempvar1.get_attribute('class') == "text-danger" :
                            msg = '     [x] - fill email - failed -> Email invalid' ; f_result.write( msg + '\n')
                            return False
                        else:
                            try:
                                tempvar3 = driver.find_element(By.XPATH, '//p[contains( text() , "Cette adresse e-mail est déjà utilisée." )]')
                                if tempvar3.get_attribute('class') == "text-danger" :
                                    msg = '     [x] - fill email - failed -> Email already used' ; f_result.write( msg + '\n')
                                    return False
                            except NoSuchElementException:    
                                msg = '     [x] - fill email - success' ; f_result.write( msg + '\n')
                                return True
                    except NoSuchElementException:
                        msg = '[x] fill form - failed -> fill email failed' ; f_result.write( msg + '\n')
                        return False
            except NoSuchElementException :
                msg = '[x] fill form - failed -> fill email failed' ; f_result.write( msg + '\n')
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
                        msg = '     [x] - fill password - failed - passwords does not match together' ; f_result.write( msg + '\n')
                        return False 
                    else:
                        msg = '     [x] - fill password - success' ; f_result.write( msg + '\n')
                        return True 
                except NoSuchElementException:
                    msg = '[x] fill form - failed -> fill password failed' ; f_result.write( msg + '\n')
                    return False
            except NoSuchElementException:
                msg = '[x] fill form - failed -> fill password failed' ; f_result.write( msg + '\n')
                return False

        if tca_fill_form_email():
            if tca_fill_form_password():
                msg = '[x] fill form - success' ; f_result.write( msg + '\n')
                return True          

        msg = '[x] fill form - failed' ; f_result.write( msg + '\n')
        return False             

    # APPUYER SUR LE BOUTON DE SUBMITION
    def tca_click_submit():
        try:
            elemBtnSendForm = driver.find_element(By.XPATH, "//button[@class='btn btn_l btn_l1 btn_full btn_l1_quaternary']")
            if elemBtnSendForm.get_attribute('disabled'):
                msg = '[x] click button submit - failed - submit button is disabled' ; f_result.write( msg + '\n')
                return False
            else :    
                #elemBtnSendForm.click()
                driver.execute_script( "arguments[0].click();" , elemBtnSendForm )
                msg = '[x] click button submit - success' ; f_result.write( msg + '\n')
                return True
        except NoSuchElementException:
            msg = '[x] click button submit - failed' ; f_result.write( msg + '\n')
            return False

    # VERIFIER SI LES PASSWORDS SONT VALIDES
    def tca_check_password():
        time.sleep(1.5)
        try:
            driver.find_element(By.XPATH, '//p[contains( text() , "Le mot de passe doit comporter 8 caractères" )]')
            msg = '[x] check password - failed -> passwords not in format' ; f_result.write( msg + '\n') 
            return False
        except NoSuchElementException :
            msg = '[x] check password - success' ; f_result.write( msg + '\n')                                                        
            return True

    # VERIFIER SI LE COMTPE A ETE CREE
    def tca_check_account_created():
        msg = '[x] send form - run' ; f_result.write( msg + '\n')
        try:
            if driver.find_element( By.XPATH, '//p[contains( text() , "Votre compte a bien été créé." )]' ):                                                      
                msg = '[x] send form - success -> Compte créé' ; f_result.write( msg + '\n')
                time.sleep(2)
                return True
        except NoSuchElementException:
            msg = '[x] send form - failed' ; f_result.write( msg + '\n')
            return False


    try:
        with open('./dataCreateAccount.csv') as csvCreateAccount:
            with open('./feuilleResultats.md', 'w', encoding='utf-8') as f_result:
                csvReader = csv.reader( csvCreateAccount, delimiter=';' )
                msg = "[x] pré-requis - run" ; f_result.write( msg + '\n')
                #____________________________________
                if tca_run_pre(): 
                #____________________________________
                    for row in csvReader:
                        msg = "\n\n\n\n\n``_____________________________________________``"
                        f_result.write( msg + '\n') ; 
                        msg = "**###################################################**\n" + \
                              "**#########**      CREER LES COMPTES     **##########**\n" + \
                              "**###################################################**"
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
        msg = 'Erreur -> fichier(s) non chargé(s)' ; f_result.write( msg + '\n')



#################################################################
###########         CONNECTER LES COMPTES            ############
#################################################################
def test_login_account( seDeconnecter , modifier ):

    # OUVRE LE SITE ET REFUSE LES COOKIES
    def tla_run_pre():
        try:
            driver.get("https://glisshop.com")
            time.sleep(5)
            elemCloseCookie = driver.find_element(By.XPATH, "//button[@id='tarteaucitronAllDenied2']")
            #elemCloseCookie.click()
            driver.execute_script( "arguments[0].click();" , elemCloseCookie )
            msg = '[x] pré-requis - success' ; f_result.write( msg + '\n')
            return True
        except NoSuchElementException:
            msg = '[x] pré-requis - failed' ; f_result.write( msg + '\n')
            return False

    # OUVRE LE SITE
    def tla_open_site():
        try:
            msg = '[x] open site - run' ; f_result.write( msg + '\n')
            driver.get("https://glisshop.com")
            msg = '[x] open site - success' ; f_result.write( msg + '\n')  
            return True
        except:
            msg = '[x] open site - failed' ; f_result.write( msg + '\n')
            return False

    # OUVRIR L'ONGLET POUR SE CONNECTER
    def tla_open_account():
        try:
            msg = '[x] open account sign in - run' ; f_result.write( msg + '\n')
            elemAccount = driver.find_element(By.XPATH, "//a[@class='header_link d-block']")
            #elemAccount.click() 
            driver.execute_script( "arguments[0].click();" , elemAccount )
            try:
                elemLog = driver.find_element(By.XPATH, '//a[contains( text() , "Déjà client" )]')
                elemLog.click()
                msg = '[x] open account sign in - success' ; f_result.write( msg + '\n')
                return True  
            except NoSuchElementException:
                msg = '[x] open account sign in - failed' ; f_result.write( msg + '\n')
                return False     
        except NoSuchElementException :
            msg = '[x] open account sign in - failed' ; f_result.write( msg + '\n')
            return False

    # REMPLIR LES CHAMPS 
    def tla_fill_form():
        try:
            msg = "[x] fill form - run" ; f_result.write( msg + '\n')
            elemEmail = driver.find_element( By.XPATH, '//input[@placeholder="Saisissez votre adresse e-mail *"]' )
            elemEmail.send_keys(row[0])
            elemPassw = driver.find_element( By.XPATH, '//input[@placeholder="Votre mot de passe *"]' )
            elemPassw.send_keys(row[1])
            elemShowPassw = driver.find_element( By.XPATH, '//button[@title="Voir le mot de passe"]' )
            #elemShowPassw.click()
            driver.execute_script( "arguments[0].click();" , elemShowPassw )
            msg = "    [x] - fill form - Email filled"    ; f_result.write( msg + '\n')
            msg = "    [x] - fill form - Password filled" ; f_result.write( msg + '\n')
            msg = "[x] fill form - success" ; f_result.write( msg + '\n')
            return True
        except NoSuchElementException:
            msg = "[x] fill form - failed" ; f_result.write( msg + '\n')
            return False

    # APPUYER SUR LE BOUTON DE SUBMITION
    def tla_submit_button():
        try:
            elemBtnSendForm = driver.find_element(By.XPATH, "//button[@class='btn btn_l btn_l1 btn_full btn_l1_quaternary']")
            if elemBtnSendForm.get_attribute('disabled'):
                msg = '[x] click button submit - failed - submit button is disabled' ; f_result.write( msg + '\n')
                return False
            else :    
                #elemBtnSendForm.click()
                driver.execute_script( "arguments[0].click();" , elemBtnSendForm )
                msg = '[x] click button submit - success' ; f_result.write( msg + '\n')
                return True
        except NoSuchElementException:
            msg = '[x] click button submit - failed' ; f_result.write( msg + '\n')
            return False

    # CHECK IS VALID
    def tla_check_form():
        time.sleep(1.5)
        try:
            driver.find_element(By.XPATH, '//p[contains( text() , "L\'identifiant et le mot de passe ne correspondent pas." )]')
            msg = '[x] check data sent - failed -> id and password does not match' ; f_result.write( msg + '\n') 
            return False
        except NoSuchElementException :
            msg = '[x] check data sent - success' ; f_result.write( msg + '\n')   
            msg = '[x] user is logged successfuly' ; f_result.write( msg + '\n')                                                      
            return True


    #################################################################
    ###########         DECONNECTER LES COMPTES          ############
    #################################################################
        # PRÉREQUIS ËTRE CONNECTÉ
    def test_logout_account():
        time.sleep(1)
        try:
            f_result.write('\n')
            msg = "**###################################################**\n" + \
                  "**########**   DÉCONNECTER LES COMPTES   **##########**\n" + \
                  "**###################################################**"
            f_result.write( msg + '\n')
            msg = '[x] open site - run' ; f_result.write( msg + '\n')
            driver.get("https://glisshop.com")
            time.sleep(2)
            msg = '[x] open site - success' ; f_result.write( msg + '\n')
            msg = '[x] open account - run' ; f_result.write( msg + '\n')
            elemAcc = driver.find_element( By.XPATH, '//a[@href="mon-compte/mes-informations.html"]' )
            #elemAcc.click()
            driver.execute_script( "arguments[0].click();" , elemAcc )
            msg = '[x] open account - success' ; f_result.write( msg + '\n')
            time.sleep(2)
            try:
                msg = '[x] account click logout - run' ; f_result.write( msg + '\n')
                elemLogout = driver.find_element( By.XPATH, '//a[@title="Déconnexion"]' )
                #elemLogout.click()
                driver.execute_script( "arguments[0].click();" , elemLogout )
                msg = '[x] account click logout - success' ; f_result.write( msg + '\n')
                return True
            except NoSuchElementException:
                msg = '[x] account click logout - failed' ; f_result.write( msg + '\n')
                return False
        except NoSuchElementException:
            msg = '     [x] open account - failed' ; f_result.write( msg + '\n')
            return False

    #################################################################
    ###########         MODIFIER LE COMPTE               ############
    #################################################################
        # PRÉREQUIS ËTRE CONNECTÉ
    def test_update_account():


        # OUVRE LE SITE
        def tua_open_file():
            try:
                msg = '[x] open site - run' ; f_result.write( msg + '\n')
                driver.get("https://glisshop.com")
                time.sleep(2)
                msg = '[x] open site - success' ; f_result.write( msg + '\n')
                return True
            except:
                msg = '[x] open site - failed' ; f_result.write( msg + '\n')
                return False

        # CLICK SUR L'ONGLET DU COMPTE
        def tua_open_tab_account():
            try:
                msg = '[x] open account tab - run' ; f_result.write( msg + '\n')
                elemTab = driver.find_element(By.XPATH, "//a[@href='mon-compte/mes-informations.html']")
                #elemTab.click()
                driver.execute_script( "arguments[0].click();" , elemTab )
                msg = '[x] open account tab - success' ; f_result.write( msg + '\n')
                return True
            except NoSuchElementException:
                msg = '[x] open account tab - failed' ; f_result.write( msg + '\n')
                return False

        # CLICK SUR L'ONGLET ACCUEIL DU COMPTE
        def tua_open_tab_home():
            try:
                msg = '[x] open accueil tab - run' ; f_result.write( msg + '\n')
                elemAcc = driver.find_element(By.XPATH, "//a[@title='ACCUEIL']")
                #elemAcc.click()
                driver.execute_script( "arguments[0].click();" , elemAcc )
                msg = '[x] open accueil tab - success' ; f_result.write( msg + '\n')
                return True
            except NoSuchElementException:
                msg = '[x] open accueil tab - failed' ; f_result.write( msg + '\n')
                return False        

        # CLICK SUR LE BOUTON MODIFIER
        def tua_click_button_modif():
            try:
                time.sleep(1)
                msg = '[x] click modifier button - run' ; f_result.write( msg + '\n')


                elemClick = driver.find_element(By.XPATH, "//button[@data-ng-click='openEdit()']")
                driver.execute_script( "arguments[0].click();" , elemClick )
                #elemClick.click()
                #wait = WebDriverWait(driver, 7)
                #wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Next')]"))).click()
                time.sleep(2)

                msg = '[x] click modifier button - success' ; f_result.write( msg + '\n') 
                return True          
            except NoSuchElementException:
                msg = '[x] click modifier button - failed' ; f_result.write( msg + '\n')
                return False

        # FILL FORM
        def tua_fill_form_account():
            msg = '[x] fill account info - run' ; f_result.write( msg + '\n')
            # f_result.write( '\n\n' + str(csvReader2[0]) + '\n\n' )
            # print( '\n\n' + str(csvReader2[0]) + '\n\n' )
            # print( '\n\n' )

            def tua_fill_prenom():
                try:
                    msg = ' ->  [x] fill prénom - run' ; f_result.write( msg + '\n')
                    elemP = driver.find_element(By.XPATH, "//input[@placeholder='Prénom']")
                    elemP.clear()
                    elemP.send_keys(row2[0])
                    msg = ' ->  [x] fill prénom - success' ; f_result.write( msg + '\n')
                    return True               
                except NoSuchElementException:
                    msg = ' ->  [x] fill prénom - failed' ; f_result.write( msg + '\n')
                    return False

            def tua_fill_nom():
                try:
                    msg = ' ->  [x] fill nom - run' ; f_result.write( msg + '\n')
                    elemP = driver.find_element(By.XPATH, "//input[@placeholder='Nom']")
                    elemP.clear()
                    elemP.send_keys(row2[1])
                    msg = ' ->  [x] fill nom - success' ; f_result.write( msg + '\n')
                    return True
                except NoSuchElementException:
                    msg = ' ->  [x] fill nom - failed' ; f_result.write( msg + '\n')
                    return False

            def tua_fill_phone():
                try:
                    msg = ' ->  [x] fill phone number - run' ; f_result.write( msg + '\n')
                    elemP = driver.find_element(By.XPATH, "//input[@placeholder='Téléphone portable pour la livraison *']")
                    elemP.clear()
                    elemP.send_keys(row2[2])
                    msg = ' ->  [x] fill phone number - success' ; f_result.write( msg + '\n')
                    return True
                except NoSuchElementException:
                    msg = ' ->  [x] fill phone number - failed' ; f_result.write( msg + '\n')
                    return False

            def tua_fill_anniv():
                try:
                    msg = ' ->  [x] fill anniversary - run' ; f_result.write( msg + '\n')
                    elemP = driver.find_element(By.XPATH, '//input[@placeholder="Date d\'anniversaire"]')
                    elemP.clear()
                    elemP.send_keys(row2[3])
                    msg = ' ->  [x] fill anniversary - success' ; f_result.write( msg + '\n')
                    return True
                except NoSuchElementException:
                    msg = ' ->  [x] fill anniversary - failed' ; f_result.write( msg + '\n')
                    return False

            def tua_fill_pseudo():
                try:
                    msg = ' ->  [x] fill pseudo - run' ; f_result.write( msg + '\n')
                    elemP = driver.find_element(By.XPATH, "//input[@placeholder='Pseudonyme']")
                    elemP.clear()
                    elemP.send_keys(row2[4])
                    msg = ' ->  [x] fill pseudo - success' ; f_result.write( msg + '\n')
                    return True
                except NoSuchElementException:
                    msg = ' ->  [x] fill pseudo - failed' ; f_result.write( msg + '\n')
                    return False

            if tua_fill_prenom():
                if tua_fill_nom():
                    if tua_fill_phone():
                        if tua_fill_anniv():
                            if tua_fill_pseudo():
                                msg = '[x] fill account info - success' ; f_result.write( msg + '\n')
                                time.sleep(5)
                                return True

            msg = '[x] fill account info - failed' ; f_result.write( msg + '\n')
            return False                    

        # CLICK BTN UPDATE
        def tua_click_btn_update():
            try:
                msg = '[x] click update button - run' ; f_result.write( msg + '\n')
                elemP = driver.find_element(By.XPATH, "//button[@data-ng-click='saveAccount()']")
                if elemP.get_attribute('disabled'):
                    msg = '[x] click update button - failed -> button disabled' ; f_result.write( msg + '\n')
                    return False
                else:
                    #elemP.click()
                    driver.execute_script( "arguments[0].click();" , elemP )
                    msg = '[x] click update button - success' ; f_result.write( msg + '\n')
                    msg = '[x] account updated - success' ; f_result.write( msg + '\n')
                    time.sleep(4)
                    return True
            except NoSuchElementException:
                msg = '[x] click update button - failed -> button not found' ; f_result.write( msg + '\n')
                return False    

        time.sleep(1)
        try:
            with open('./dataUpdateAccount.csv') as csvU:
                csvReader2 = csv.reader( csvU, delimiter=';' )
                f_result.write('\n')
                msg = "**###################################################**\n" + \
                      "**########**     MODIFIER LES COMPTES    **##########**\n" + \
                      "**###################################################**"
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
                                            msg = "[x] account updated successfuly " ; f_result.write( msg + '\n')
                                            return True 
                    return False
        except:
            msg = "[x] account update failed" ; f_result.write( msg + '\n')   
            return False                             




    try:
        with open('./dataConnectionAccount.csv') as csvConnectAccount:
            with open('./feuilleResultats.md', 'w', encoding='utf-8') as f_result:
                csvReader = csv.reader( csvConnectAccount, delimiter=';' )
                msg = "[x] pré-requis - run" ; f_result.write( msg + '\n')
                #____________________________________
                if tla_run_pre(): 
                #____________________________________
                    i = 0
                    for row in csvReader:
                        msg = "\n\n\n\n\n``_____________________________________________``\n"
                        f_result.write( msg + '\n')
                        msg = "**###################################################**\n" + \
                              "**#########**   CONNECTER LES COMPTES    **##########**\n" + \
                              "**###################################################**"
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
        msg = 'Erreur -> fichier(s) non chargé(s)' ; f_result.write( msg + '\n')  



#################################################################
###########           RECHERCHER ARTICLES            ############
#################################################################
def test_find_article( addToCart , removeToCart ):

    #################################################################
    ###########         AJOUTER AU PANIER                ############
    #################################################################
    def test_add_cart():
        try:
            time.sleep(1)
            msg = "-[x] click button add to cart - run" ; f_result.write( msg + '\n' )

            elemtemp = driver.find_element( By.XPATH, '//button[ @data-ng-click="goToCart()" ]' )
            driver.execute_script( "arguments[0].click();" , elemtemp )
            time.sleep(1)

            elemV = driver.find_element( By.XPATH, '//button[ @data-ng-click="addProducts()" ]' )
            driver.execute_script( "arguments[0].click();" , elemV )

            time.sleep(2)
            msg = "-[x] click button add to cart - success" ; f_result.write( msg + '\n' )
            try:
                time.sleep(1)
                msg = "--[x] click button view cart - run" ; f_result.write( msg + '\n' )
                elemV = driver.find_element( By.XPATH, '//a[ contains( text() , "Voir mon panier" ) ]' )
                #elemV.click()
                driver.execute_script( "arguments[0].click();" , elemV )
                msg = "--[x] click button view cart - success" ; f_result.write( msg + '\n' )
                time.sleep(5)
            except NoSuchElementException:
                msg = "--[x] click button view cart - failed" ; f_result.write( msg + '\n' )

        except WebDriverException:
            try:
                time.sleep(1)

                f_result.write( '-[v] \n' )

                elemtemp = driver.find_element( By.XPATH, '//button[ @data-ng-click="goToCart()" ]' )
                driver.execute_script( "arguments[0].click();" , elemtemp )
                time.sleep(1)

                elemV = driver.find_element( By.XPATH, '//button[ @data-ng-click="addProducts()" ]' )
                driver.execute_script( "arguments[0].click();" , elemV )

                time.sleep(2)
                msg = "-[x] click button add to cart - success" ; f_result.write( msg + '\n' )
                try:
                    time.sleep(1)
                    msg = "--[x] click button view cart - run" ; f_result.write( msg + '\n' )
                    elemV = driver.find_element( By.XPATH, '//a[ contains( text() , "Voir mon panier" ) ]' )
                    #elemV.click()
                    driver.execute_script( "arguments[0].click();" , elemV )
                    msg = "--[x] click button view cart - success" ; f_result.write( msg + '\n' )
                    time.sleep(5)
                except NoSuchElementException:
                    msg = "--[x] click button view cart - failed" ; f_result.write( msg + '\n' )

            except WebDriverException:
                pass
        except NoSuchElementException:
            msg = "-[x] click button add to cart - failed" ; f_result.write( msg + '\n' )


    #################################################################
    ###########         SUPPRIMER DU PANIER              ############
    #################################################################
    def test_delete_all_cart():
        try:
            time.sleep(4)
            msg = "-[x] click button delete to cart - run" ; f_result.write( msg + '\n' )
            elemD = driver.find_elements( By.XPATH, '//button[@data-ng-click="remove()"]' )
            for e in elemD:
                #e.click()
                driver.execute_script( "arguments[0].click();" , e )
                time.sleep(4)
            msg = "-[x] click button delete to cart - success" ; f_result.write( msg + '\n' )   
        except StaleElementReferenceException:
            elemD = driver.find_elements( By.XPATH, '//button[@data-ng-click="remove()"]' )
            for e in elemD:
                #e.click()
                driver.execute_script( "arguments[0].click();" , e )
                time.sleep(4)
            msg = "-[x] click button delete to cart - success" ; f_result.write( msg + '\n' )  
        except NoSuchElementException:
            msg = "-[x] click button delete to cart - failed" ; f_result.write( msg + '\n' )


    try:
        with open( './dataFindArticle.csv' ) as csvF:
            with open('./feuilleResultats.md', 'w', encoding='utf-8') as f_result:
                csvReader3 = csv.reader( csvF, delimiter=';' )

                driver.maximize_window()

                msg = "\n\n\n\n\n``_____________________________________________``"
                msg = "**###################################################**\n" + \
                      "**#########**     CHERCHER UN ARTICLE    **##########**\n" + \
                      "**###################################################**"
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
                        msg = "[x] Finding element - run" ; f_result.write( msg + '\n')
                        try:
                            msg = "    [x] Fill search input - run" ; f_result.write( msg + '\n' )
                            elemG = driver.find_element( By.XPATH, "//button[@title='Recherchez un produit, une marque,...']" ) 
                            #elemG.click()
                            driver.execute_script( "arguments[0].click();" , elemG )
                            msg = "    [x] Fill search input - success" ; f_result.write( msg + '\n' )
                            msg = "[x] Finding element - success" ; f_result.write( msg + '\n')
                            time.sleep(3)

                            try: 
                                msg = "[x] click the result - run" ; f_result.write( msg + '\n' )
                                elemV = driver.find_element( By.XPATH, '//a[ @data-role="result-link" ]' )
                                driver.execute_script( "arguments[0].click();" , elemV )
                                #elemV.click()
                                msg = "[x] click the result - success" ; f_result.write( msg + '\n' )
                                time.sleep(4)

                                if addToCart and bool(addToCart):
                                    f_result.write( '\n' )
                                    msg = "**###################################################**\n" + \
                                          "**#########**     AJOUTER UN ARTICLE     **##########**\n" + \
                                          "**###################################################**"
                                    f_result.write( msg + '\n\n' )
                                    test_add_cart()
                                    if removeToCart and bool(removeToCart):
                                        f_result.write( '\n' )
                                        msg = "**###################################################**\n" + \
                                              "**#########**     SUPPRIMER LE PANNIER   **##########**\n" + \
                                              "**###################################################**"
                                        f_result.write( msg + '\n\n')
                                        test_delete_all_cart()

                            except NoSuchElementException:
                                msg = "[x] click the result - failed" ; f_result.write( msg + '\n' )

                        except NoSuchElementException:
                            msg = "    [x] Fill search input - failed" ; f_result.write( msg + '\n' )
                            msg = "[x] Finding element - failed" ; f_result.write( msg + '\n')

                except NoSuchElementException:
                    msg = "Erreur boutton chercher pas trouvé" ; f_result.write( msg + '\n' )

    except:
        msg = 'Erreur -> fichier(s) non chargé(s)' ; f_result.write( msg + '\n')



#################################################################
###########               COMMANDER                  ############
#################################################################








        ##### Créer les comptes #####
#test_create_account()

        ##### Connecter les comptes #####
#test_login_account( seDeconnecter = False , modifier = False )

        ##### Connecter et Déconnecter les comptes #####
#test_login_account( seDeconnecter = True , modifier = False )

        ##### Connecter, Modifier et Déconnecter les comptes #####
#test_login_account( seDeconnecter = True , modifier = True )

        ##### Chercher un article #####
#test_find_article( addToCart = False , removeToCart = False )

        ##### Chercher un article , l'ajouter au panier #####
#test_find_article( addToCart = True , removeToCart = False )

        ##### Chercher un article , l'ajouter au panier , supprimer tous les articles #####
test_find_article( addToCart = True , removeToCart = True  )

        ##### Fermer les fichiers #####
closeFile()

