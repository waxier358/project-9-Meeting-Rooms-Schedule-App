I developed a Meeting Schedule Application using Tkinter and SQLite.

To create pictures from my app, I utilized the Sweet Home 3D application (https://www.sweethome3d.com). 
Additionally, I employed several libraries found on the Sweet Home 3D website under the section Suport/3D models (https://www.sweethome3d.com/importModels.jsp).

This is my app User Login page:

![1](https://github.com/waxier358/project9-Meeting-Rooms-Schedule-App/assets/105735620/4c627687-77a6-4915-bb6d-e8752fba99b4)

The user login page features two input fields for the username and password, along with a button to hide or show the password entry. This page also provides links to the 'Forgot Password' page and the 'Create New Account' page.

![2](https://github.com/waxier358/project9-Meeting-Rooms-Schedule-App/assets/105735620/5d002702-f8e7-49a8-b962-1e1c343467c8)

After the user enters their username and password and presses the 'Login' button, they are directed to the 'Rooms Schedule' page.

![15](https://github.com/waxier358/project9-Meeting-Rooms-Schedule-App/assets/105735620/d14b246d-9871-4e91-ad4a-c24cbea6dede)

This is the main page of my application. From here, you can schedule a new room for a specific day and also view all the schedules that have already been made.
The page features a room name label (referred to as 'Classroom' in the above pictures) and a picture label, where five images associated with each room can be viewed.
Both labels are paired with back and forward navigation buttons. Each set of these navigation buttons controls a Circular Doubly Linked List (CDLL).
When the user changes the room's name label, the CDLL associated with the room's pictures also changes.

Additionally, a calendar is displayed on this page, with its default date set to the current date. When a date is selected from the calendar, the application queries the database and displays all the schedules associated with the selected date at specific hours.
If any time interval is free, the user can create a new schedule. This new schedule is then inserted into the database and the user is notified by email about their scheduled appointment.

![16](https://github.com/waxier358/project9-Meeting-Rooms-Schedule-App/assets/105735620/0e65bd57-ddfd-4471-b67a-275448767327)

![17](https://github.com/waxier358/project9-Meeting-Rooms-Schedule-App/assets/105735620/421fc9c8-af0f-4ad0-a9b9-dd64dc38270b)

A new account can be created on this page by filling out the required fields, which typically include user information such as name, email address and a password. 

![3](https://github.com/waxier358/project9-Meeting-Rooms-Schedule-App/assets/105735620/b373da86-f9bb-4943-85e6-352cc6c69842)

This application offers a password reset feature using a token. Initially, the user must enter the email address associated with their account.

![4](https://github.com/waxier358/project9-Meeting-Rooms-Schedule-App/assets/105735620/e5c31b05-5eb8-425e-8840-9bdca4907f17)

The user will receive a token via email:

![12](https://github.com/waxier358/project9-Meeting-Rooms-Schedule-App/assets/105735620/b1fb4fad-4540-4235-a806-630c5e7db496)

![5](https://github.com/waxier358/project9-Meeting-Rooms-Schedule-App/assets/105735620/a388a794-b94b-4756-9c0d-3db6614631bf)

Once the token is verified, the user is then allowed to enter a new password.

![6](https://github.com/waxier358/project9-Meeting-Rooms-Schedule-App/assets/105735620/780b5f58-8abb-4a1b-afe9-0f1286940b8f)

This database is the backbone of my application. It stores essential data such as user information, room schedules and password tokens.
The database design is structured to ensure efficient data retrieval and secure storage of sensitive information like passwords and personal details.
It plays a crucial role in supporting the functionalities of the app, from user authentication to schedule management.

![database](https://github.com/waxier358/project9-Meeting-Rooms-Schedule-App/assets/105735620/9ea337dc-a8e3-4e19-aea4-e168c699aa3a)


