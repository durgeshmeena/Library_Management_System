# Library_Management_System
__Library Management System__ - A Web Application to ease the work of librarians. 
The library management system allows a librarian to track books and their quantity, books issued to members, book fees.<br>
Application functionalities includes -


### Base Library System
__Librarians must be able to maintain__:

  - Books with stock maintained
  - Members
  - Transactions
  
 
__The use cases included here are to__:

- Perform general CRUD operations on Books and Members
- Issue a book to a member
- Issue a book return from a member
- Search for a book by name and author
- Charge a rent fee on book returns
- Make sure a member’s outstanding debt is not more than Rs.80
- The librarian  able to import books into the system using the Frappe API and create book records.

Hosted Link : https://library-management-system29.herokuapp.com/

# To Run the project:

## step 1 : 
  Clone this repo by `git clone https://github.com/durgeshmeena/Library_Management_System`<br>
 
## step 2 :  
In root directry create `.env` file containg <br>
```  
  SECRET_KEY=''
  MONGO_URI='mongodb+srv://'
```    
  
# References



  
## step 2 : 
  Download required libraries by `pip install -m requirements.txt`<br>
  
## step 3 : 
  Start project using batchfile
  in `cmd` enter `run`
