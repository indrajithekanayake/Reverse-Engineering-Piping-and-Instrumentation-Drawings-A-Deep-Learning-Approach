### To install this application follow the steps.
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

<div align="center">
<img title="Web Interface" src="/images/Screenshot.png" width="600" height="300">
</div>

### References
This study use the dataset created by [@heyad](https://github.com/heyad/Eng_Diagrams). 

- If you use the dataset in this repository, please cite as follows:

E. Elyan, C.G. Moreno and P. Johnston, “Symbols in Engineering Drawings (SiED): An Imbalanced Dataset Benchmarked by Convolutional Neural Networks”, In 2020 International Joint Conference of the 21st EANN (Engineering Applications of Neural Networks), EANN 2020. Proceedings of the International Neural Networks Society, vol 2. Springer, Cham, DOI https://doi.org/10.1007/978-3-030-48791-1_16

- If you use/ refer the provided model or this web application, please cite as follows:

I. Ekanayake, J. Warnakula and S. Viswakula, "Reverse Engineering Piping and Instrumentation Drawings: A Deep Learning Approach," 2023 International Conference on Power, Instrumentation, Control and Computing (PICC), Thrissur, India, 2023, pp. 1-4, doi: 10.1109/PICC57976.2023.10142454.

### Comments / Questions
You can reach me on [linkedin](https://www.linkedin.com/in/indrajithek)
