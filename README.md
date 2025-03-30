# IntelligentTrader
## Intelligent Trader is an application that allows users to input a stock ticker, leverage its machine learning model(s), and observe the predicted change in financials of a given company a quarter in the future!


## Backend Structure
* Please dont roast me, this was before I learned about system modeling however I think it does the trick.
![Alt text]('user+profile_model_design.png')


## User Instructions
1. Download Python
2. `pip install django`
3. `pip install crispy-bootstrap4`
4. `pip install requests`
5. `pip install os`
6. `pip install joblib`
7. `pip install pandas`
8. `pip install scikit-learn`
9. `pip install Pillow`
10. Navigate to project directory
11. Setup EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in the settings.py file of the tutorial app. These constants are email credentials for the forgot email/password feature. Get Credentials using `https://myaccount.google.com/apppasswords`. 
12. Start her upp! `python manage.py server`

## Contributer Guide
Thank you for your interest in contributing to this project! Contributions are always welcome. Please follow the guidelines below to ensure that your contributions can be easily reviewed and merged.

## How to Contribute

1. **Fork the Repository**
   - Begin by forking the repository to your own GitHub account. This allows you to freely make changes without affecting the original codebase.

2. **Clone the Forked Repository**
   - Once you've forked the repository, clone it to your local machine:
     ```bash
     git clone https://github.com/your-username/project-name.git
     ```

3. **Create a New Branch**
   - Always create a new branch for your work. This makes it easier for maintainers to review and merge your changes. The branch name should be descriptive of the work you're doing:
     ```bash
     git checkout -b feature-name
     ```

4. **Make Your Changes**
   - Implement your feature, fix, or improvement. Make sure your code adheres to the project's coding standards and is well-documented. If you're working on a bug, ensure it is well-reported and fixed.

5. **Test Your Changes**
   - Run tests locally to ensure that your changes do not break any existing functionality. We use [pytest](https://pytest.org/) for testing:
     ```bash
     pytest
     ```

6. **Commit Your Changes**
   - Commit your changes with a clear, concise message that explains the purpose of the changes:
     ```bash
     git commit -m "Add feature or fix bug"
     ```

7. **Push Your Changes**
   - Push your changes to your forked repository:
     ```bash
     git push origin feature-name
     ```

8. **Create a Pull Request**
   - Go to the original repository on GitHub and create a pull request (PR). Select your branch and describe the changes you’ve made.
   - Please provide a clear description of the issue you're addressing and the solution you've implemented.

### Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). By participating in this project, you agree to abide by its terms. Please be respectful and considerate towards others in the community.

### Reporting Bugs

If you encounter a bug, please open an issue on the GitHub Issues page. When creating an issue:
- Provide steps to reproduce the issue.
- Include any relevant logs, error messages, or screenshots.
- Mention the version of Django and any other dependencies you're using.
- Ensure you read: 

#### Known Issues

- Has not been migrated to Postgres DB yet. (FOR Future)
- Every user can see all predictions made by all users. A user should only be able to see their own.
- All the financial data is stored but the Random Forest only needs one row - I know this is inefficent but have recently learned about CNN in my ML class and plan to change the model so keeping it as is for now is best

### Style Guide

To maintain consistency across the codebase, please follow these conventions:
- **Python**: PEP8 (use `black` for auto-formatting).
- **Django**: Follow [Django's coding style](https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/coding-style/).
- **Commit Messages**: Use clear and concise commit messages. Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification if possible.

### Get Involved

- Join the project’s discussions on GitHub to engage with other contributors.
- If you want to report an issue or suggest a feature, please check if the issue or feature request has already been raised to avoid duplicates.

### Thank You!

We appreciate your contributions to this project. Thank you for helping us improve the software!



