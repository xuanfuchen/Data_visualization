<div id="top"></div>

<!-- TABLE OF CONTENTS -->

## Index
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>




<!-- ABOUT THE PROJECT -->
## About The Project

It's a personal data visualization project

Data from: [WSJ.com](https://www.wsj.com/)

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Django](https://www.djangoproject.com/)
* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

This project requires python 3 and mySQL


### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/xuanfuchen/data_visualization.git
   ```
2. Add xnas_stock_price.sql in ```data_visualization\data\``` into your local database
3. Modify DATABASES in ```data_visualization\stock_visualization\stock_visualization\settings.py``` to match your local database USER and PASSWORD  <br>
4. Enter the virtual environment
   ```sh
   C:\data_visualization> env\Scripts\activate.bat
   ```
   success if there is (env) in front of the drive letter
   ```sh
   (env) C:\data_visualization>
   ```
5. Enter directory "data_visualization\stock_visualization"
   ```sh
   (env) C:\data_visualization> cd stock_visualization\
   ```
6. issue the following command to run the server
   ```sh
   (env) C:\data_visualization\stock_visualization> python manage.py runserver
   ```
7. Visit the page at "http://127.0.0.1:8000/nasdaq/main/"


<p align="right">(<a href="#top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Xuanfu Chen - sean.xfc@gmail.com

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

<!-- Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off! -->

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Readme Template](https://github.com/othneildrew/Best-README-Template)
* [WSJ.com](https://www.wsj.com/)

<p align="right">(<a href="#top">back to top</a>)</p>
