# TODO for Login Flow Implementation

- [x] Analyze current login logic in frontend/login.html and backend/app.py
- [x] Modify frontend/login.html to remove alerts for successful login and user not found, ensuring silent redirects
- [ ] Test the login flow:
  - Start the backend server (Flask app)
  - Open frontend/login.html in browser
  - Attempt login with existing user and correct password -> should redirect to index.html
  - Attempt login with existing user and wrong password -> should show alert and stay on login
  - Attempt login with non-existing user -> should redirect to register.html
- [ ] Verify register.html is accessible and functional
