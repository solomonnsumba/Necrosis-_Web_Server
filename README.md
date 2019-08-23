**Necrosis API Sample**

----
This repository has files for the necrosis detect API. 
The API is python based using the Django Rest Framework



**Requirements**

*All requirements are included in requirements.txt file. Main requirements are:*
*  Django == 1.11.9
*  Pillow
*  Opencv-python
*  Scikit-learn
*  Scikit-image
*  Requests(for client.py only)


1.  **Installation**
    *  `pip install -r requirements.txt`(tested in python3 virtual environment)
2.  **Running the API**
  
    *  python manage.py runserver 
        *(Runs on localhost:8000 by default. Can specify port by using runserver host:port e.g. localhost:5000)*
3.  **Running the client**
    *  Sample python
    *  `python client.py   "path-to-image"    "url-to-post"`(e.g. `python client.py   test_images/image58.jpg  http://18.219.45.102/necrosis/api2/`)
    *  sample server with browsable API is hosted at http://18.219.45.102/necrosis/api2/ and sample images in test_images folder
    *  Test images in test_images folder
    *  Reults are stored in analyzed_images folder 
4.  **API Output**  
    *  Output is the name of the analysed image, the necrosis score and link to the analysed image in JSON format.
    *  `{'image_name': '1063984_Root1_1_2019-04-12-10-57-01_QaImZqV_analysed.jpg', 'cbsd_score': '7.48 %', 'image_link': 'http://18.219.45.102/static/results/1063984_Root1_1_2019-04-12-10-57-01_QaImZqV_analysed.jpg'}`
