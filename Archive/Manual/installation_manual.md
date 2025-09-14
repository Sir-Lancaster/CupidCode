# Cupid Code User Manual

## Table of Contents
1. [Installation](#installation)
2. [Using](#using)
3. [Common Issues](#common-issues)
4. [FAQ](#faq)

## Installation

#### How to host the Cupid Code server on your local machine:


1. Clone the Cupid Code repository from GitLab:
```
git clone https://gitlab.cs.usu.edu/cs3450-team2/cupid_code.git
```
2. Navigate to the Cupid Code directory:
```
cd cupid_code
```
3. Install the required dependencies:
- Python
  - Download and install Python from the following URL: https://www.python.org/downloads/
- Poetry
  - Follow the directions based on your machine from the following URL: https://python-poetry.org/docs/#installation  
- Python Dependencies
  - Inside the Code directory, run these commands:
  ```
  poetry install
  ```
  Note: This will take some time to run due to the nvidia packages 
- NVM
  - For Windows, follow this guide: https://github.com/coreybutler/nvm-windows#readme
  - For Mac and Linux, run one of these in your terminal 
  ```
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
  OR
  wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
  ```
  - Note that it depends on your machine if it uses curl or wget. If one fails, run the other one.
- Node and NPM
  - A quick and easy way to get both Node and npm is with using nvm as such.
  - Install Node and npm using the following commands:
    ```
    nvm install node 
    nvm use node
    ```
- Javascript Dependencies
  - Inside the client directory just run:
  ```
  npm install 
  ```
4. Read the README.md file for instructions on how to set up the Cupid Code server.

## Using

1. Follow the instructions in this [README file](https://gitlab.cs.usu.edu/cs3450-team2/cupid_code/-/blob/development/Code/README.md?ref_type=heads) to set up the Server.
2. Open a web browser and navigate to the following URL:
```
http://localhost:8000
```

## Common Issues
Poetry Install is saying no such file exists
  - Just run `poetry shell` first and then run `poetry install`

## FAQ
- Do I need to have a server to run Cupid Code?
  - Yes, you will need to have a server to run Cupid Code. You can host the server on your local machine or use a cloud service like AWS, Azure, or Google Cloud.
  - If you would like to connect to a server that is already running, you can use the following URL:
    ```
    https://cupidcode.com
    ```
- Why is the server not running?
  - There could be a few reasons why the server is not running. Check the following:
    - Make sure you have installed all the required dependencies.
    - Make sure you have followed the instructions in the README.md file.
    - Make sure you have started the server.
    - Make sure you are using the correct URL to access the server.
    - Make sure you have migrated the server correctly.
