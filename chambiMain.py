import requests
import time
import pandas as pd
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from threading import Event
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random
import dataLoad
fileExcelLoad = pd.read_excel(f'{dataLoad.fileExcelLoad}', sheet_name="Sheet1")
linkCheck = f"http://{dataLoad.proxyLink}:6868/status?proxy={dataLoad.proxyLink}:"
linkReset = f"http://{dataLoad.proxyLink}:6868/reset?proxy={dataLoad.proxyLink}:"
linkGetip = f"http://{dataLoad.proxyLink}:6868/api/v1/proxy/public_ip?proxy={dataLoad.proxyLink}:"
linkresetAll = f"http://{dataLoad.proxyLink}:6868/reset_all"
linkFileip = dataLoad.fileIp
portProxyFrom = int(dataLoad.portProxyFrom)
linkNoteAccFail = dataLoad.fileAccFail
linkNoteAccDie = dataLoad.fileAccDie
accPerTurn = int(dataLoad.accPerTurn)
ref_group_link = dataLoad.ref_group_link
linkPicture = dataLoad.linkPicture
scale_windows = dataLoad.scale_windows
colour_in_rgb = str(dataLoad.colour_in_rgb)

api_url = "http://127.0.0.1:19995/api/v3/profiles/{action}/{id}"
time.sleep(1)
def run(x, i):
    setData1 = int(i)
    setData2 =int(x)
    portProxy1 = setData2 + portProxyFrom
    portProxy = str(portProxy1)
    linkCheckProxy = linkCheck + portProxy
    linkResetProxy = linkReset + portProxy
    linkGetipProxy = linkGetip + portProxy    
    rowProfile = setData1 + setData2
    tenProfile1 = fileExcelLoad.iloc[rowProfile, 0]
    tenProfile = str(tenProfile1)
    idTab1 = fileExcelLoad.iloc[rowProfile, 1]  
    profile_id = idTab1.strip()
    for openChrome in range(5):
        while True:
            checkIp = requests.get(linkCheckProxy)
            kqCheckip = checkIp.json()["status"]
            if kqCheckip:
                print("PORT:", portProxy, "- Connected")
                time.sleep(1)
                while True:
                    getIpport = requests.get(linkGetipProxy)
                    ipPort = getIpport.json()["ip"]
                    with open(linkFileip, 'r') as fileip:
                        historyIp = fileip.read()
                        if ipPort not in historyIp:
                            print('Port', portProxy, "ip:", ipPort, 'GOOD !')
                            with open(linkFileip, 'a+') as fileIpload:
                                fileIpload.write(f'{ipPort}\n')
                            time.sleep(1)
                            break
                        else:
                            print('Port', portProxy, "ip:", ipPort, 'bị trùng lặp IP, đang reset lại ip !!!')
                            time.sleep(1)
                            requests.get(linkResetProxy)
                            time.sleep(20)
                        time.sleep(1)
                time.sleep(1)
                break
            else:
                print("Port", portProxy, "Oẳng rồi, đang reset lại, đợi 15s !")
                time.sleep(1)
                requests.get(linkResetProxy)
                time.sleep(20)
            time.sleep(1)
        time.sleep(1) 
        try:            
            line1 = x * 505
            line2 = (x-8)*505
            strLine1 = str(line1)
            strline2 = str(line2)
            if x < 8:
                win_pos_value = f"{strLine1},5"
            else:
                win_pos_value = f"{strline2},700"
            params = {
                "win_scale": scale_windows,
                "win_pos": win_pos_value,
                "win_size": "500,700"
            }
            start_url = api_url.format(action="start", id=profile_id)
            response = requests.get(start_url, params=params)
            if response.status_code == 200:
                data = response.json()
                success_value = data.get('success')
                
                driver_path = data['data']['driver_path']
                remote_debugging_address = data['data']['remote_debugging_address']
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_experimental_option("debuggerAddress", remote_debugging_address)
                service = Service(driver_path)
                driver = webdriver.Chrome(service=service, options=chrome_options)
                try:
                    for tab in range(1,3):
                        driver.switch_to.window(driver.window_handles[tab])
                        driver.close()
                        time.sleep(0.3)
                except:time.sleep(0.5)
                print(f"Profile {tenProfile} mở thành công, code:{success_value}...Delay 6s before loading...")
                time.sleep(6)
                break
        except Exception as e:
            print(f"Đã có lỗi xảy ra: {tenProfile}>>>Đang quay lại từ đầu.")
            time.sleep(5)
            continue
    try:
        for checkAcc in range(8):
            driver.get("chrome://settings/")
            time.sleep(2)
            try:        
                driver.get("https://web.telegram.org/k/")
                time.sleep(2)
            except:pass
            print(f'Đang check live telegram in profile {tenProfile}...')
            if checkAcc == 7:
                print(f'{tenProfile}>>>KO check nổi>>tắt profile...')
                time.sleep(1)
                close_url = api_url.format(action="close", id=profile_id)
                close_response = requests.get(close_url)
                if close_response.status_code == 200:
                    close_data = close_response.json()
                    print(f"Profile {tenProfile} closed, code:{close_data.get('message')}")
                    break
                else:
                    print("Lỗi khi đóng profile. Status code:", close_response.status_code)
            else:pass
            try:
                element = WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.XPATH, '//h4[text()="Log in to Telegram by QR Code"]')))
                print(f'{tenProfile}>>>acc DIE cmnr, tiên sư thằng bán acc')
                with open(linkNoteAccDie, 'a+') as noteAccDie:
                    noteAccDie.write(f'{tenProfile}|accDie\n')
                time.sleep(1)
                close_url = api_url.format(action="close", id=profile_id)
                close_response = requests.get(close_url)
                if close_response.status_code == 200:
                    close_data = close_response.json()
                    print(f"Profile {tenProfile} closed, code:{close_data.get('message')}")
                    break
                else:
                    print("Lỗi khi đóng profile. Status code:", close_response.status_code)
            except:pass
            try:
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="input-search"][1]'))) 
                break
            except:pass
        time.sleep(2)
        print(f"Profile {tenProfile} acc vẫn ngọt lịm>>> Log to Claim...")        
        for logGam1e in range(6):
            if logGam1e == 5:
                time.sleep(1)
                close_url = api_url.format(action="close", id=profile_id)
                close_response = requests.get(close_url)
                if close_response.status_code == 200:
                    close_data = close_response.json()
                    print(f"Profile {tenProfile} closed, code:{close_data.get('message')}")
                    break
                else:
                    print("Lỗi khi đóng profile. Status code:", close_response.status_code)
            else:pass
            try:
                driver.get("chrome://settings/")
                time.sleep(1)
                driver.get(ref_group_link)
                element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, f'//span[@class="translatable-message"]//a[text()="{linkPicture}"]')))
                driver.execute_script("arguments[0].click();", element)
                try:
                    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Launch"]')))
                    driver.execute_script("arguments[0].click();", element)
                except:pass
                          
                iframe = WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[@class="payment-verification"]')))
                try:
                    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Go to Web version"]')))
                    actions = ActionChains(driver)
                    actions.move_to_element(element).click().perform()
                    time.sleep(3)
                    try:
                        for tab in range(1,3):
                            driver.switch_to.window(driver.window_handles[tab])
                            driver.close()
                            time.sleep(0.3)
                    except:time.sleep(0.5)
                    driver.switch_to.window(driver.window_handles[0])
                    iframe = WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[@class="payment-verification"]')))
                    time.sleep(1)
                except:pass

                element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="root"]/div[1]/div[1]/div[1]/div[2]/div[2]/button[1]//*[@class="_button_img_17fy4_119"]')))
                actions = ActionChains(driver)
                actions.move_to_element(element).click().perform()
                time.sleep(3)
                actions.move_to_element(element).click().perform()
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Your balance"]'))) 
                break           
            except:pass
        for claimClick in range(6):
            if claimClick == 5:                
                time.sleep(1)
                close_url = api_url.format(action="close", id=profile_id)
                close_response = requests.get(close_url)
                if close_response.status_code == 200:
                    close_data = close_response.json()
                    print(f"Profile {tenProfile} closed, code:{close_data.get('message')}")
                    break
                else:
                    print("Lỗi khi đóng profile. Status code:", close_response.status_code)
            else:pass            
            try:
                print(f">>>{tenProfile}>>> Claim PX point ")
                time.sleep(1)
                element = driver.find_element(By.XPATH, '//div[text()="Your balance"]')
                driver.execute_script("arguments[0].scrollIntoView();", element)
                time.sleep(2)

                element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="_button_13oyr_11"]')))
                actions = ActionChains(driver)
                actions.move_to_element(element).click().perform()
            except:pass
            try:
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[text()="CLAIM IN "]')))
                print(f">>>{tenProfile}>>> Đã claim xong>>>Vào vẽ tranh")
                break
            except:pass      
        time.sleep(5)
       
        ####//////////////////////////////////////////////
        for logGamePaint in range(6):
            if logGamePaint == 5:
                time.sleep(1)
                close_url = api_url.format(action="close", id=profile_id)
                close_response = requests.get(close_url)
                if close_response.status_code == 200:
                    close_data = close_response.json()
                    print(f"Profile {tenProfile} closed, code:{close_data.get('message')}")
                    break
                else:
                    print("Lỗi khi đóng profile. Status code:", close_response.status_code)
            else:pass
            try:
                driver.get("chrome://settings/")
                time.sleep(1)
                driver.get(ref_group_link)
                element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, f'//span[@class="translatable-message"]//a[text()="{linkPicture}"]')))
                driver.execute_script("arguments[0].click();", element)
                try:
                    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Launch"]')))
                    driver.execute_script("arguments[0].click();", element)
                except:pass
                iframe = WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[@class="payment-verification"]')))
                time.sleep(2)
                try:
                    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Go to Web version"]')))
                    actions = ActionChains(driver)
                    actions.move_to_element(element).click().perform()
                    time.sleep(3)
                    try:
                        for tab in range(1,3):
                            driver.switch_to.window(driver.window_handles[tab])
                            driver.close()
                            time.sleep(0.3)
                    except:time.sleep(0.5)
                    driver.switch_to.window(driver.window_handles[0])
                    iframe = WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[@class="payment-verification"]')))
                    time.sleep(1)
                except:pass
                element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@id="root"]/div[1]/div[1]/div[1]/div[2]/div[2]/button[1]//*[@class="_button_img_17fy4_119"]')))
                break
            except:pass
        #########################
        time.sleep(1)
        print(f" >>>{tenProfile} >>> pick màu")
        canvas = driver.find_element(By.ID, 'canvasHolder')
        canvas_location = canvas.location
        canvas_size = canvas.size
        while True:
            time.sleep(1)
            try:
                random_x = random.randint(-10, 9)
                random_y = random.randint(-12, 11)
                actions = ActionChains(driver)
                actions.move_to_element_with_offset(canvas, random_x, random_y).click().perform()
            except:pass
            try:
                element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="_info_lwgvy_42"]/div[1]')))
                break
            except:pass
        time.sleep(5)
        xpath_father = f'//div[@class="_info_lwgvy_42"]/div[@style="background-color: rgb{colour_in_rgb};"]'
        xpath_son = f'//div[@class="_color_line_epppt_15"]//div[@style="background-color: rgb{colour_in_rgb};"]'
        while True:
            print(f"{tenProfile}>>>ĐANG PICK COLOUR mã màu {colour_in_rgb}")
            try:
                element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="_info_lwgvy_42"]/div[1]')))
                actions = ActionChains(driver)
                actions.move_to_element(element).click().perform()
                try:
                    element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="_color_line_epppt_15"]/div[17]')))
                    actions = ActionChains(driver)
                    actions.move_to_element(element).click().perform()
                except:pass
                try:
                    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath_father)))
                except:
                    element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, xpath_son)))
                    actions = ActionChains(driver)
                    actions.move_to_element(element).click().perform()
                element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath_father)))
                break
            except:pass
        element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="_info_lwgvy_42"]/div[1]')))
        actions = ActionChains(driver)
        actions.move_to_element(element).click().perform()
        print(f"{tenProfile}>>> Painting...")
        canvas = driver.find_element(By.ID, "canvasHolder")
        canvas_location = canvas.location
        canvas_size = canvas.size
        for painting in range(1,100,1):
            randomWait = random.randint(5,12)
            waitTime = randomWait / 10
            time.sleep(waitTime)
            try:
                element = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '//button[@class="_button_lwgvy_147"]/div[1]/div[1]/div[2]/span[2]')))
                soLuot = element.text
                if soLuot== "0":
                    print(f">>>@@@@@{tenProfile} >>> Hết lượt tô màu, Đóng profile sau 3 giây...")
                    time.sleep(1)
                    break
                else:
                    print(f'>>>{tenProfile} >>> Số lượt tô màu còn lại là: <{soLuot}>')
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="_container_b4e6p_11"]/div[1]/button[2]')))
                actions = ActionChains(driver)
                actions.move_to_element(element).click().perform()                                
                element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="_container_b4e6p_11"]/div[1]/div[@class="_container_srbwq_1"]')))
                while True:                    
                    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACABAMAAAAxEHz4AAAAFVBMVEVHcEz/3Jr/6ADjygD/AAC5AAAAAAB/sfDAAAAAAXRSTlMAQObYZgAAAJJJREFUeNrt2bEJBCEQQNFrYVqwhWnBFq6F338Jx4IiyIG76ez/iRjMiwyE+Zj9i0MC9QGA7yEAgarAGu6HJiJQHTgnICAgIFAbAHgGrARqAACZmROIiAC4zt573+8TaK01gWLA6O5DyswUqAVcMXoCzGGBCsBqAjGCVYz2D4ZAbWBP4EXA6AQACJQB3LEImO39AJS0GBsvGYIKAAAAAElFTkSuQmCC"]')))
                    actions = ActionChains(driver)
                    actions.move_to_element(element).click().perform()
                    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@class="_button_j77dp_27 _fast_type_button_j77dp_49 _shop_button_j77dp_44 _fast_mode_button_enabled_j77dp_72"]')))
                    break
                while True:
                    element = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '//button[@class="_button_lwgvy_147"]/div[1]/div[1]/div[2]/span[2]')))
                    soLuot1 = element.text
                    if soLuot1== "0":
                        time.sleep(1)
                        break
                    else:
                        soLuotChamBi = int(soLuot1)
                        for clickPaint in range(soLuotChamBi):
                            random_x = random.randint(-50, 50)
                            random_y = random.randint(-50, 15)
                            if -12 < random_x < 12 and -12 < random_y < 12:
                                print(f"<{tenProfile}>thử lại !!!!")
                            else:
                                actions = ActionChains(driver)
                                actions.move_to_element_with_offset(canvas, random_x, random_y).click().perform()
                                valueWait = random.randint(5,18)/10
                                time.sleep(valueWait)                
            except:pass           
        time.sleep(5)
    except Exception as e:
        print(f"Acc {tenProfile} FAIL-saving info to file note !!!! Error: {str(e)}")
        with open(linkNoteAccFail, 'a+') as noteAccFail:
            noteAccFail.write(f'{tenProfile}|{profile_id}|error #NOTPIXEL paint\n')
        time.sleep(1)
        close_url = api_url.format(action="close", id=profile_id)
        close_response = requests.get(close_url)
        if close_response.status_code == 200:
            close_data = close_response.json()
            print(f"Profile {tenProfile} closed, code:{close_data.get('message')}")
        else:
            print("Lỗi khi đóng profile. Status code:", close_response.status_code)
    finally:
        try:
            close_url = api_url.format(action="close", id=profile_id)
            close_response = requests.get(close_url)
            if close_response.status_code == 200:
                close_data = close_response.json()
                print(f"Profile {tenProfile} closed, code:{close_data.get('message')}")
            else:
                print("Lỗi khi đóng profile. Status code:", close_response.status_code)
        except:pass
def main():
    while True:
        try:
            for i in range(0, 5000, accPerTurn):              
                time.sleep(1)
                idBeginturnacc = str(fileExcelLoad.iloc[i, 1])
                print(f"Turn bắt đầu từ acc: {fileExcelLoad.iloc[i, 0]}")
                if len(idBeginturnacc) < 10:
                    break
                
                run_threads = []
                for x in range(accPerTurn):
                    t_run = threading.Thread(target=run, args=(x, i))
                    run_threads.append(t_run)
                    t_run.start()
                for t_run in run_threads:
                    t_run.join()

                print(">>ĐÃ QUẤT XONG TURN ACC !!!")
                print("Đang reset IP để chạy turn tiếp")
                requests.get(linkresetAll)
                print("----Reset IP thành công, Vui lòng đợi 20s !------")
                for fap69 in range(20, 1, -1):
                    print(f'Continue in {fap69}s !')
                    time.sleep(1)
        except:
            print(' ')
            print(f'Đã xong lô acc...')
if __name__ == "__main__":
    main()

