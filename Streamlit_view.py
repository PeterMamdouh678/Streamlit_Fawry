# Libraries
import streamlit as st
import socket
import subprocess
import requests
from appium import webdriver
from appium.options.common import AppiumOptions
from typing import Any, Dict
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
import time

# appium_process = subprocess.Popen(['appium'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# 01223265388
# Initialize session state
if 'driver' not in st.session_state:
    st.session_state.driver = None
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'details' not in st.session_state:
    st.session_state.details = {}

# Streamlit UI
st.title("Phone Number Data Scraper")
Times = 1
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(("0.0.0.0",9999))
result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE)
output = result.stdout.decode("utf-8")

# Extract device names (usually the first column in the output)
device_lines = output.strip().split('\n')[1:] # Skip the first line 'List of devices attached'
devices = [line.split()[0] for line in device_lines if "emulator" in line]
print(devices[0])
# server.listen()

# while True:
#     client, addr = server.accept()
#     print("connection from", addr)
#     client.send("You are connected! \n".encode())

# Step 1: Input login phone number and password
if st.session_state.step == 1:
    step_1_container = st.empty()

    with step_1_container.container():

        login_phone_number = st.text_input("Login Phone Number")
        password = st.text_input("Password", type="password")
        start_button = st.button("Start Scraping")

        if start_button:
            if not login_phone_number or not password:
                st.error("Please provide both the phone number and password.")
            else:
                # URL to be used
                url = 'http://localhost:4723/wd/hub'
                # url = 'http://localhost:4723'

                # Add the needed capabilities to be connected with the phone and app
                cap: Dict[str, Any] = {
                    "platformName": "Android",
                    "platformVersion": "14.0",
                    # "deviceName": "emulator-5554",
                    "devuceName" : devices[0],
                    "automationName": "UiAutomator2",
                    "appActivity": "com.emeint.android.mwallet2.view.StartupActivity",
                    "appPackage": "com.fawry.myfawry",
                    "newCommandTimeout": 999999
                }

                # Start Appium session
                options = AppiumOptions()
                options.load_capabilities(cap)
                st.session_state.driver = webdriver.Remote(url, options=options)

                # Wait function to avoid errors
                wait1 = WebDriverWait(st.session_state.driver, 10, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, NoSuchElementException])

                time.sleep(4)

                # Locating the login button
                trials = 4
                for _ in range(trials):
                    try:
                        time.sleep(1)
                        login_button = st.session_state.driver.find_element(by=AppiumBy.ID, value="com.fawry.myfawry:id/2131367111")
                        login_button.click()
                        break
                    except:
                        continue
                else:
                    st.error("Login button not found")

                time.sleep(1)

                try:
                    confirm = st.session_state.driver.find_element(by=AppiumBy.ID, value="com.fawry.myfawry:id/2131362361")
                    confirm.click()
                except:
                    print("didn't show")

                # Enter phone number and password
                phone = st.session_state.driver.find_element(by=AppiumBy.ID, value="com.fawry.myfawry:id/2131363298")
                phone.click()
                phone.send_keys(login_phone_number)

                pass_xpath = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText"
                password_field = st.session_state.driver.find_element(by=AppiumBy.XPATH, value=pass_xpath)
                password_field.click()
                password_field.send_keys(password)
                
                time.sleep(2)

                login = st.session_state.driver.find_element(by=AppiumBy.ID, value="com.fawry.myfawry:id/2131362317")
                login.click()

                st.session_state.step = 2
                st.success("Phone number and password entered successfully.")
                time.sleep(1)
                step_1_container.empty()

# Step 2: Input OTP
if st.session_state.step == 2:
    step_2_container = st.empty()
    with step_2_container.container():

        time.sleep(1)
        otp = st.text_input("Please enter the OTP sent to your phone")
        otp_button = st.button("Submit OTP")
        time.sleep(2)

        if otp_button:
            if not otp:
                st.error("Please provide the OTP.")
            else:
                # Enter OTP
                time.sleep(7)
                otp_parent = st.session_state.driver.find_element(AppiumBy.ID, value="com.fawry.myfawry:id/2131365008")

                for index, num in enumerate(otp):
                    otp_box = otp_parent.find_elements(by=AppiumBy.XPATH, value=".//*")
                    otp_box[index + 1].click()
                    otp_box[index + 1].send_keys(num)
                
                time.sleep(4)
                st.session_state.step = 3
                st.success("OTP entered successfully.")

                # Skip pop ups
                time.sleep(13)
                try:
                    fingerprint = st.session_state.driver.find_element(by=AppiumBy.ID, value="com.fawry.myfawry:id/2131366630")
                    fingerprint.click()
                except:
                    print("Fingerprint option didn't show")

                time.sleep(2)
                try:
                    pop_up = st.session_state.driver.find_element(by=AppiumBy.ID, value="com.fawry.myfawry:id/2131362361")
                    pop_up.click()
                except:
                    print("Pop-up didn't show")

                time.sleep(2)
                try:
                    notification = st.session_state.driver.find_element(by=AppiumBy.ID, value="com.android.permissioncontroller:id/permission_deny_button")
                    notification.click()
                except:
                    print("Notification permission didn't show")

                time.sleep(2)
                try:
                    pop_up = st.session_state.driver.find_element(by = AppiumBy.ID, value="com.fawry.myfawry:id/2131362361")
                    pop_up.click()
                except:
                    print("pop_up didn't show") 

                time.sleep(2)
                try:
                    onboarding = st.session_state.driver.find_element(by=AppiumBy.ID, value="com.fawry.myfawry:id/2131363976")
                    onboarding.click()
                except:
                    print("Onboarding didn't show")

                time.sleep(2)

                finances = st.session_state.driver.find_element(by = AppiumBy.ID, value="com.fawry.myfawry:id/2131365564")
                print("finances ", finances)

                finance = finances.find_elements(by = AppiumBy.XPATH, value=".//*")
                print(finance[25].get_attribute("resource-id"))
                finance[25].click()

                step_2_container.empty() 

Again = True
# Times = 1
# Step 3: Input number to get its data
if st.session_state.step == 3:

    # while Again:
    time.sleep(2)

    step_3_container = st.empty()
    # st.session_state.driver.get_screenshot_as_base64() 
    with step_3_container.container():

        # Times = Times + 1
        time.sleep(2)
        # Find the needed service
        number_to_get_data = st.text_input(f'Please enter the number to get its data{Times}')
        number_button = st.button(f'Submit Number{Times}')
        Times = Times + 1

        time.sleep(4)
        if number_button:
            if not number_to_get_data:
                st.error("Please provide the number to get its data.")
            else:
                time.sleep(2)
                # if Times == 2:
                #     print("Entereed the If condition")
                #     print("Times : " , Times)

                #     finances = st.session_state.driver.find_element(by = AppiumBy.ID, value="com.fawry.myfawry:id/2131365564")
                #     print("finances ", finances)

                #     finance = finances.find_elements(by = AppiumBy.XPATH, value=".//*")
                #     print(finance[25].get_attribute("resource-id"))
                #     finance[25].click()
                #     Times = Times + 2

                #     print("Times : " , Times)
                #     print("Times Type : ", type(Times))

                time.sleep(2) 
                if number_to_get_data:
                    st.session_state.number_to_get_data = number_to_get_data

                # Click on Valu icon
                if st.session_state.number_to_get_data:
                    time.sleep(2)
                    valu_xpath = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.FrameLayout[1]/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]"
                    valu = st.session_state.driver.find_element(by = AppiumBy.XPATH, value=valu_xpath)
                    valu.click()
                    # Locate and enter the number to get its data
                    time.sleep(2)
                    phoone_xpath = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout/MwalletCustomTextInputLayout/android.widget.EditText"
                    phone_number_field = st.session_state.driver.find_element(by=AppiumBy.XPATH, value=phoone_xpath)
                    phone_number_field.clear()
                    phone_number_field.click()
                    time.sleep(2)
                    phone_number_field.send_keys(number_to_get_data)

                    # Submit to get data
                    goto_payment = st.session_state.driver.find_element(by=AppiumBy.ID, value="com.fawry.myfawry:id/2131362318").click()
                    time.sleep(5)

                    # Get Due and Total amount
                    try:
                        try:
                            due_amount = st.session_state.driver.find_element(by=AppiumBy.ID, value="com.fawry.myfawry:id/2131362959")
                            st.session_state.details["Due Amount"] = due_amount.get_attribute("text")
                        except:
                            st.session_state.details["Due Amount"] = "Due Amount not available"
                        try:
                            total_amount = st.session_state.driver.find_element(by=AppiumBy.ID, value="com.fawry.myfawry:id/2131362992")
                            st.session_state.details["Total Amount"] = total_amount.get_attribute("text")
                        except:
                            st.session_state.details["Total Amount"] = "Total amount not available"

                        st.success("Data scraped successfully")
                        st.write(st.session_state.details)
                        time.sleep(5)
                        
                        try:
                            time.sleep(2)
                            st.session_state.driver.find_element(by = AppiumBy.ID, value="com.fawry.myfawry:id/2131363414").click()

                        except:
                            time.sleep(2)
                            back_button = st.session_state.driver.find_element(by=AppiumBy.ID, value="com.fawry.myfawry:id/2131361931")
                            back_button.click()
                            st.session_state.number_to_get_data = ""
                            st.session_state.step = 3
                        # add_new_number = st.text_input(f'Please enter the number to get its data{Times}')
                        # new_number = st.button(f'Submit Number{Times}')
                        
                        # if add_new_number:
                        #     st.session_state.add_new_number = add_new_number

                        # if st.session_state.number_to_get_data:
                        # back_button = st.session_state.driver.find_element(by=AppiumBy.ID, value="com.fawry.myfawry:id/2131361931")
                        # back_button.click()
                        # st.session_state.number_to_get_data = ""
                        # st.session_state.step = 3
                        # step_3_container.empty()



                        # Ask user if they want to check another number
                        # another_check = st.radio("Do you want to check another number?", ("Yes", "No"), key="check_another_1")
                        # if another_check == "Yes":
                        #     # Click the back button and repeat the process
                        #     back_button = st.session_state.driver.find_element(by=AppiumBy.ID, value="com.fawry.myfawry:id/2131361931")
                        #     back_button.click()
                        #     st.session_state.number_to_get_data = ""
                        #     st.session_state.step = 3
                        #     step_3_container.empty()  # Clear current UI

                        #     # st.experimental_rerun()  # Refresh the page to allow the user to enter a new number
                        # else:
                        #     st.session_state.step = 4 
                        #     step_3_container.empty()  # Clear current UI

                    except:
                        st.error("Could not retrieve data for the provided number")
                        # add_new_number = st.text_input(f'Please enter the number to get its data{Times + 1}')
                        # new_number = st.button(f'Submit Number{Times + 1}')
                        
                        # if add_new_number:
                        #     st.session_state.add_new_number = add_new_number

                        # if st.session_state.number_to_get_data:
                        back_button = st.session_state.driver.find_element(by=AppiumBy.ID, value="com.fawry.myfawry:id/2131361931")
                        back_button.click()
                        st.session_state.number_to_get_data = ""
                        st.session_state.step = 3
                        # step_3_container.empty()

                        # # Ask user if they want to check another number
                        # another_check = st.radio("Do you want to check another number?", ("Yes", "No"), key="check_another_2")
                        # if another_check == "Yes":
                        #     # Click the back button and repeat the process
                        #     back_button = st.session_state.driver.find_element(by=AppiumBy.ID, value="com.fawry.myfawry:id/2131361931")
                        #     back_button.click()
                        #     st.session_state.number_to_get_data = ""
                        #     st.session_state.step = 3
                        #     step_3_container.empty()  # Clear current UI

                        #     # st.experimental_rerun()  # Refresh the page to allow the user to enter a new number
                        # else:
                        #     Again = False
                        #     st.session_state.step = 4  # Set a step to end session
                        #     step_3_container.empty()  # Clear current UI

        # step_3_container.empty()



# Step 4: End session
if st.session_state.step == 4:
    st.write("Thank you for using the scraper.")
    # Close the driver session
    if st.session_state.driver:
        st.session_state.driver.quit()
    st.session_state.step = 1

