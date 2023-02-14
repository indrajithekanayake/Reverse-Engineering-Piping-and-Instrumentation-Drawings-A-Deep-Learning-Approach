To install this application follow the steps.
1. You will need python installed in your system
    - Make sure you create your virtual environement before installing dependeiences for this application.
    - To create virtual environement you can use Conda or virtualenv whichever you prefer.
    - To know how to create virtual environement follow this link: https://www.geeksforgeeks.org/python-virtual-environment/

2. After creating virtual environement and activating it we need to install dependeiences
    Run this command after activating virtual environement

    ```bash
    pip install -r requirements.txt
    ```

3. After requirements are successfully installed we can run the server. 
    To run server use this command.
    
    ```bash
    python app.py
    ```

    or
    
    ```bash
    flask -app app.py --debug run
    ```

4. After starting the server you should be able to access **127.0.0.1:5000** where your application will be running.
