# **OVERVIEW**
This is a web application that provides a list of items within a variety of categories
and integrates  third party user registration and authentication system (Google OAUTH2 API).
Authenticated users have the ability to post, edit, and delete their own items.
This project was developed in Python and uses the Flask framework. SQLalchemy is used
as an Object Relational Mapper.



## **QUICKSTART**
1. Install [Python](https://www.python.org/downloads/), and [PostgreSQL](https://www.postgresql.org/download/).
2. Install the following packages with ```pip install [package]```(replace [package] with the required package name);
...1. Flask
...2. SQLalchemy
...3. oauth2client
3. Download the files and place them in their respective folders.
4. Open a terminal and run ```python database_setup.py ``` to setup the database.
5. On the terminal run ```python populate_database.py ``` to populate the database with default items.
6. Finally, run ```python project.py ``` to run the server.
7. Open your browser and go to ```http://localhost:5000/category/``` to open the home page.
8. Create an account with Google to be able to Create, Update and delete Items.
9. To view the API endpoints


## **LICENSE**
MIT License

Copyright (c) [2017] [Chike Ezeh]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
