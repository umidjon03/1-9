# 1-9
The project 1-9 contains all technical tasks as far:

1.	Task: Implement User Registration API
Description:  Create an API endpoint using Django Rest Framework that allows users to register by providing their username, email, and password. The endpoint should handle validation, generate a unique user token, and store the user information in the database.

MPV:
The user app does what mentioned in task 1. Register with certain fields and etc..

2.	Task: Create a Model Serializer 
Description:  Implement a Django Rest Framework serializer for a specific model. The serializer should handle both read and write operations, including field validation and data transformation as necessary. Ensure that the serializer supports nested relationships if applicable.

MPV:
For this task, I covered only required asking. I created serializers that can read and write but not views and endpoints as they are required for this task. However, I provided python shell scripts inside python file as a comment to test the serializers. A tester can give his/her vulue for the fields

3.	Task: Implement API Endpoints for CRUD Operations
Description:  Develop API endpoints using Django Rest Framework for creating, reading, updating, and deleting objects of a specific model. The endpoints should follow RESTful conventions, handle appropriate HTTP methods (POST, GET, PUT, DELETE), and include proper error handling and response status codes.

MPV:
For this (and upcomening ) task(s) I chose the topic of "Task" app from my variants. We have Task model and it contains Task related fields like "task_summary" etc.. Inside the app you can find CRUD operations as view or endpoint

4.	Task: Add Pagination and Filtering to an API Endpoint 
Description:  Enhance an existing DRF API endpoint by adding pagination support and filtering capabilities. Implement pagination to limit the number of results per page and include relevant pagination metadata. Enable filtering based on specific fields or criteria using query parameters

MPV:
For this task, I enhence the task app with django's internal and external packages/libs. I gave the backend logics for filter/order/searching in settings.py. I used 3 backend logics for this task.

5.	Task: Implement Authentication and Authorization
Description:  Integrate authentication and authorization mechanisms into a Django Rest Framework API. Utilize DRF's authentication classes to support token-based authentication or JWT authentication. Implement role-based access control (RBAC) or permission classes to restrict access to specific views or endpoints.

MPV:
All autherization operations are created in users app. As mentioned all logs in with their generated token and other logics for authentication can be found in the python codes.

6.	Task: Write Unit Tests for API Endpoints 
Description:  Create unit tests using Django Rest Framework's testing utilities to ensure the correctness of API endpoints. Write test cases to cover different scenarios, including success cases, error cases, and edge cases. Verify the behavior of the endpoints, request validation, and response formats.

MPV:
The test are written for CRUD operation of the Task app and inherented from DRF's APITestCase.
It checks success and error handlers as well

7.	Task: Implement File Upload and Download Endpoints
Description:  Extend an existing API by adding endpoints that handle file uploads and downloads. Configure the necessary serializers and views to enable users to upload files and store them on the server. Implement secure download endpoints that authenticate and authorize users before allowing access to files.

MPV:
As solving of this task, A user can upload attachment for his/her task. And can download his/her tasks' attechments as well. Other logics are in the code

8.	Task: Implement Caching for API Responses
Description:  Optimize the performance of an API by adding caching mechanisms. Identify the endpoints that could benefit from caching and implement caching decorators or middleware to store and serve cached responses. Consider using Django's built-in caching or external caching solutions like Redis.

MPV:
Usually, get methods are requested frequenlt. For example a user wants to see his/her recorded task,
so I implemented django build-in cache provides for getters, etc..

9.	Task: Integrate Third-Party API
Description:  Integrate a third-party API into an existing Django Rest Framework project. Implement the necessary views and serializers to consume and interact with the external API endpoints. Handle authentication, request/response formatting, and error handling as per the third-party API documentation.

MPV:
As a third-party API, I chose OpenAi API. When user is lack of help or support he/she can use AI suggestion generator for the task
Only required thing is that user should provide the values for the fields understandable and readable. Then, The ChatGPT 3.5 can generate support for his/her task.
note: Don't fotget provide your openai key in .env file, for testing

Note: For all view/viewset classes isAuthenticated is set as a default in settings.

You can test all endpoinds by using postman requests which I provided in this repo as "HTTP requests" directory
But don't forget to use your own generated tokens for authentication. You can generate by signing up/in.

Of course there are things to do, but the developer is running out of time/deadline :)

If something looks like error or strange, please let me know or create issue in github for it.
you can connect with me via email: shuxratovumidjon03@gmail.com


