# WeightTracker 

## ***An app to prevent unintentional weight loss in health care facilities***  <br><br>

# Application Overview  

>In a health care setting, unintentional weight loss is associated with adverse clinical outcomes and decline, especially in the elderly. Therefore, it is an important quality indicator for long term care and some skilled nursing/rehab facilities. Although the facility’s registered dietitian (RD) is commonly responsible for this quality indicator, interventions to prevent or treat weight loss are often multifaceted and require an interdisciplinary approach. 

>WeightTracker is a full-stack application I created as my final capstone project for Nashville Software School. The app is designed to be used in conjunction with a facility's EMR to allow the RD to obtain patient weights timely and systematically. It is also designed to identify patients at risk, display weight trends over time, and allow fast and efficient communication between disciplines.

>To demonstrate this application, a fictitious rehab and long term care facility called Gaffney Scranton Rehab and Healing (GSHR) was created. Users of WeightTracker include trained Certified Nursing Assistants (CNAs), RDs, Registered Nurses(RNs) and Licensed Practical Nurses (LPNs), Nurse Practitioners(NPs), and MDs. 

# Features
There are three primary types of users that can register and log in to their account: (CNA, RD, and RN/NP/MD).<br>
Responsive design allows for use on most screen sizes.<br>

Each user has different responsibilities:  
1. From their dashboard, CNAs can:
    - check and send messages to multiple users
    - view the current census list
    - create a new weight sheet for the week and enter in data for each patient
    - view previous weight sheets
    - save and update entered data at any time before the weight sheet is finalized by the RD
2. From their dashboard, RDs can:
    - check and send messages to multiple users
    - view the current census list
    - view, edit, save and finalize a weight sheet
    - view previous weight sheets
    - submitted weight sheet highlights missing or concerning data for RD to investigate
    - search for individual patients by name and view a table and graph of weight trends over a 6 month period to monitor significant weight changes
3. From their dashboard, RNs/NPs/MDs can:
    - check and send messages to multiple users
    - view current census list
    - view finalized weekly weight sheets 

# User Experience
## Register a new user and sign in to view  CNA dashboard

![](gifs/register.gif)

## CNA creates a new weekly weight sheet and saves data

![](gifs/create_wt_sheet.gif)

## CNA completes weight sheet and sends message to RD and RN
![](gifs/completed_wt_sheet.gif)

## RD checks messages, finalizes weight sheet, and notifies MD and NP of resident at risk
![](gifs/RD_wt_sheet.gif)

## RD searches by resident to view 6 month summary of weight history
![](gifs/RD_summary.gif)

## RN/LPN/NP/MD can check messages and view finalized weight sheets from dashboard
![](gifs/MD_dashboard.gif)

## Responsive layout using Tailwind CSS
![](gifs/responsive.gif)

# Technologies

![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
 ![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
 ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)


## Installation Instructions

Requirements: 
* Python 3.11.0
* pipenv

1. If you haven't already, visit [https://github.com/mvdutta/weight-tracking-client](https://github.com/mvdutta/weight-tracking-client) and follow the instructions in the readme there to set up the client side of the application
1. In the terminal, run  ```git clone https://github.com/mvdutta/weight-tracking-api.git``` to clone the repository
2. Move into the folder you just created ```cd weight-tracking-api```
3. Run ```pipenv install``` to install the dependencies into the virtual environment
4. Run ```pipenv shell``` to run the virtual environment
5. Run ```sh seed.sh``` Set up the sql database with the starting data
6. Run ```python manage.py runserver``` to start the server or use the debugger in your code editor
7. Once the backend is running, you can explore the app by registering a new user in any of the available roles (CNA, RD, LPN, RN, NP, MD) 

## Author
### Maia Dutta
[<img alt="Github" src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white">](https://github.com/mvdutta)[<img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white">](https://www.linkedin.com/in/maia-v-dutta/)








