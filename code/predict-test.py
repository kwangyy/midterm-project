import requests
url = 'http://localhost:9696/predict'

salary_id = '31363'
salary = {'title': 'Software Engineer',
          'yearsofexperience': 3.0,
          'yearsatcompany': 2.0,
          'gender': 'Male',
          'dmaid': 0.0,
          'Masters_Degree': 0,
          'Bachelors_Degree': 1,
          'Doctorate_Degree': 0,
          'Highschool': 0,
          'Some_College': 0,
          'Race_Asian': 0,
          'Race_White': 0,
          'Race_Two_Or_More': 0,
          'Race_Black': 0,
          'Race_Hispanic': 0,
          'area': 543,
          'country': 10,
          'is_faang': 0}


response = requests.post(url, json=salary).json()
print(response)