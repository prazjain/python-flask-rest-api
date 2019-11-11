# Python Flask Rest Api
---

Programmed by praz.jain@gmail.com

A simple example to show how Rest Api can be written in Python using Flask micro-framework.

We will do CRUD operations on books repository. We expose this books data via Rest Api, 
and store this data in sql lite db files (to keep things focused on rest api), and also add 
authentication to our Apis.


#### Install Dependencies

    pip3 install Flask
    pip3 install sql_alchemy
    pip3 install pyjwt
    
#### Populate our database with some data

* Open Terminal, and enter below commands:

  * Start python shell

        python3
 
  * Add books data by running below commands, one at a time in python terminal

		from BookModel import *		
		db.create_all()		
		Book.add_book('The Tiger Who Came To Tea',4.00,9780007215997)	
		Book.add_book('Hippobottymus',2.00,9781848690516)
		Book.add_book('The Wonky Donkey',2.99,9781407195575)
		from UserModel import *
		db.create_all()
		User.create_user('user1','password')


### Use cases

#### Login

*Request*

POST	`http://127.0.0.1:5000/login`

Headers
    
    Content-Type: application/json
    
Body

    {
        "username" : "user1",
        "password" : "password"
    }

*Response*

An authenticated JWT token like below
	
    eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzM0OTE1MDN9.A9rSZITZJBuSHN2PDrd9FV27mFja2teCNWdyZcDlHn0


#### Get Books

*Request*

GET	`http://127.0.0.1:5000/books?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzM0OTE1MDN9.A9rSZITZJBuSHN2PDrd9FV27mFja2teCNWdyZcDlHn0`

Headers
    
    Content-Type: application/json

*Response*

Body

    {
        "books": [
            {
                "isbn": 9780007215997,
                "name": "The Tiger Who Came To Tea",
                "price": 4
            },
            {
                "isbn": 9781848690516,
                "name": "Hippobottymus",
                "price": 2
            },
            {
                "isbn": 9781407195575,
                "name": "The Wonky Donkey",
                "price": 4
            },
            {
                "isbn": 9780347215234,
                "name": "The Cat Sat On A Mat",
                "price": 2.99
            }
        ]
    }


#### Create new Book

*Request*

POST	`http://127.0.0.1:5000/books?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzM0OTE1MDN9.A9rSZITZJBuSHN2PDrd9FV27mFja2teCNWdyZcDlHn0`

Headers
    
    Content-Type: application/json

Body

    {
        "isbn": 9780347215234,
        "name": "The Cat Sat On A Mat",
        "price": 2.99,
        "test": "hello"
    }

*Response*

Status `201 CREATED`


For Other Operations download Postman requests from the repository
