# School Report System

![Website Mockup](assets/images/readme/mockup.png)

[This is a link to the live website]()


## Table Of Contents
- [Introduction](#introduction)
- [Design](#design) 
  * [User Feedback](#user-feedback)
- [Application Features](#application-features)
  * [Data/APIs Used](#dataapis-used)
- [UX (User Experience)](#user-experience)
- [Accessibility](#accessibility)
- [Future Features](#future-features)
- [Testing](#testing)  
- [Deployment](#deployment)
- [Technologies](#technologies)
- [Code](#code)  
- [Credits for images](#credits-for-images) 
- [Acknowledgements](#acknowledgements) 


## Introduction
The Savanna Hotel Booking System is a web-based application that allows users to search for available rooms, view room details, and make bookings. The system provides a seamless experience for hotel guests and administrators, offering features such as room availability checking, booking management, and dynamic pricing calculations. The Savanna Hotel system is designed to make the hotel booking process easy and efficient.


  ### User Feedback
- Booking Confirmation: “Your booking has been confirmed! Your room is reserved.”
- Login Success: “Welcome back! Login successful.”
- Booking Error: “Booking failed. Please check the details and try again.”

## Application Features
## Backend Logic
The Savanna Hotel Booking System leverages powerful backend features to ensure a smooth booking process:
- User Authentication:
Secure login system using Django for both admin and guest access.
- Room Details:
Each room's details, such as pricing, capacity, and availability, are displayed to the user for easy selection.
- Total Cost Calculation:
The system calculates the total cost based on room price and stay duration, and displays it in real time.
- Admin Management:
Admin can view all bookings, edit booking details, and cancel bookings. This ensures that the system is always up-to-date.
- Booking Confirmation and Email Notification:
Upon booking confirmation, the user receives a notification email with all booking details.

## Data/APIs Used
- Django ORM:
Django’s Object-Relational Mapping (ORM) is used for handling room and user data on the backend efficiently.

## User Experience
### As a first time user:

1. **Login Process:**
  - Securely log in with your username and password.
  - Receive immediate feedback on login status.

2. **Booking Process:**
  - Select your desired room, enter personal details, and review your booking information.
  - The system calculates the total cost based on your selected dates and room type.

3. **Booking Confirmation:**
  - Receive a confirmation message and email with all booking details.

### As a Returning User:
1. **Report Generation:**

  -Generate booking summaries and reports for administrative purposes.

2. **Admin Panel:**
  - Generate booking summaries and reports for administrative purposes.

## Accessibility
- Color Contrast: The system ensures proper color contrast for readability, especially for users with visual impairments.
-  Keyboard Navigation: All functionality can be accessed via keyboard for users with mobility challenges.
- Screen Reader Compatibility: All critical content is accessible via screen readers to ensure inclusivity for users with disabilities.
- Error Messages: Detailed error messages are provided to guide users in correcting any issues with their input.

## Future Features
- Payment Gateway Integration: Allow users to pay for bookings directly through the system.
- Multi-Room Booking: Enable guests to book multiple rooms in one transaction.
- Email Notifications: Automatically send booking confirmations and updates to users.
- Mobile Application: Develop a mobile version of the platform for on-the-go booking.
- Admin Dashboard Enhancements: Add graphs and detailed statistics for room occupancy and revenue tracking.

## Testing
### User story Testing
- Login: Testing valid and invalid login attempts.
- Booking Process: Confirming that total costs are calculated correctly and that bookings are saved.
- Admin Access: Ensuring that admin can view and modify bookings without issues.

### Feature Testing
- Room Selection: Ensured that the system correctly filters rooms by availability and displays relevant details.

[CI Python Linter](https://pep8ci.herokuapp.com/#)

![python validation](assets/images/readme/python_validation.png)

## Deployment
### Heroku

1. Sign into [Heroku](https://dashboard.heroku.com/apps)
2. On the right side click **New** and select **Create new app**
3. Create a new Heroku app with a unique name. Heroku will generate a random name if you don't specify one and select your region.
4. Click **Create app**
5. Close to the top select **Settings**, click on *Reveal Config Vars**
  - On **Key** and **Value** input fields enter PORT and Paste everything copied from the **creds.json** folder in your gitpod workspace(respectively).
6. Click **add** to create another set of KEY and VALUE.
  - In the input fields add KEY: PORT, VALUE: 8000
7. At the bottom, click **Add buildpack**, from the options select **python** and **nodejs** + **add buildpack** after selecting each.
8. Close to the top where you clicked **Settings** this time click **Deploy**, click **connect to github**.
  - search for the name of the repository you want to deploy and click **connect**
9. Click **deploy branch**

## Technologies
- Github for the source code.
- Gitpod for creating the website.
- Django: Web framework for backend logic and server-side functionality.
- Code Institute's Gitpod Template
- Heroku for deployment
- Code institute learnings
- Techsini to create a mockup of the website
- Unsplash for images
- PostgreSQL: Database for storing user and booking data.
- HTML/CSS/JavaScript: Frontend design and interactivity.

## Code
- [Code Institute](https://learn.codeinstitute.net/dashboard)
- Tutorial videos- Programming with Mosh [YouTube](https://www.youtube.com/@programmingwithmosh)

## Credits for images
** All images came from [Unsplash](https://unsplash.com/)
- ikhale
- Alex Tyson
- Lisa Anna
- abdul Raheem Kannath
- Olexandr Ignatov
- Lotus Design N Print
- Chastity Corjijo
- Mark champs
- Devon Janse Van Rensburg
- Reisetop
- Despina-galani
- GERAGOS YAGHLIAN

## Acknowledgement
- I would like to thank my Mentor Mr Precious for his guidance and advice.

- A big thanks to Slack Community for for always being someone willing to answer my questions.

- A big thank you to the Code Institute team for their constant support and resources that made this project possible.