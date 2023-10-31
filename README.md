# CommandSuite5 Task Automation System

---
## Overview
The CommandSuite5 Scheduler/Task Automation System is a Python-based application that allows users to schedule and automate video uploads to TikTok. It provides a graphical user interface (GUI) for easy task management, video scheduling, and interaction with Content Posting APIs.

## Features
- **Task Scheduler**: Schedule video uploads at specific times and dates.
- **Calendar Display**: View, add, edit, and remove scheduled tasks using a calendar interface.
- **API Integration**: Seamlessly connect to TikTok's Content Posting API for video uploads.
- **Video Preview**: Preview scheduled videos before posting.
- **User Authentication**: Authenticate TikTok users to access their accounts.
- **Task Automation**: Automate the posting of videos based on the schedule.

## Getting Started
Follow these steps to set up and run CommandSuite5:

### Prerequisites
- Python 3.7 or higher installed.
- Pip package manager installed.
- TikTok Developer account with API access credentials.

### Installation
1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/ailerosoft/CommandSuite5.git` 

2. Navigate to the project directory:
    
    bashCopy code
    
    `cd CommandSuite5` 
    
3. Install the required dependencies:
    
    bashCopy code
    
    `pip install -r requirements.txt` 
    

### Configuration

1. Obtain TikTok API access credentials from your TikTok Developer account.
    
2. Create a `.env` file in the project root directory and add the following:
    
    dotenvCopy code
    
    `TIKTOK_API_KEY=your_api_key
    TIKTOK_API_SECRET=your_api_secret` 
    

### Usage

1. Run the application:
    
    bashCopy code
    
    `python main.py` 
    
2. The GUI interface will open. Use it to schedule and manage video uploads.
    

### User Guide

- Detailed instructions and usage guidelines can be found in the [User Guide](https://chat.openai.com/c/USER_GUIDE.md).

## Directory Structure

- `GUI/`: Contains the graphical user interface components.
- `Core/`: Houses the core functionality, including API integration and task automation.
- `Tests/`: Unit tests and test cases for the application.
- `README.md`: This file.
- `requirements.txt`: Lists the project's dependencies.

## Contribution

Contributions to this project are welcome! If you'd like to contribute, please follow the [Contribution Guidelines](https://chat.openai.com/c/CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](https://chat.openai.com/c/LICENSE) file for details.

## Acknowledgments

- Special thanks to the TikTok Developer platform for providing access to their API.

## Contact

For questions or support, please contact [ailerosoft@gmail.com](mailto:ailerosoft@gmail.com).

