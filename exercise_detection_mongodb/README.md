
Practice Physical Therapy (GUI)
=====================================

## Step manage this repo

### Clone 👇

1. Clone this repo
    ```bash
    git clone https://github.com/KimmyLps/exercise_detection.git
    ```
2. ```bash
   cd exercise_detection
   ```
3. Set up virtual environment
   ```bash
   python -m virtualenv <your-env-name>
   <your-env-name>/Scripts/activate
   ```
4. Install all libraries
   ```bash
   pip install -r requirements.txt
   ```
5. Run the project
   ```bash
   python3 main.py
   ```
6. Complete 👍

### Edit code 👇

1. Create new branch for develop this repo
    ```bash
    git checkout -b <your-new-branch-for-develop>
    ```
2. Edit code in editor
3. Add change code to git repo
    ```bash
    git add <your-file-change> or .
    ```
4. Comment for change code to git repo
    ```bash
    git commit -m "<your-comment>"
    ```
5. Push to repo
    ```bash
    git push origin <your-branch>
    ```

### Update your local repo from new update github repo 👇

  - With fetch all of the branches from the repository. This also downloads all of the required commits and files from the other repository. 
    1. Fetch all branchs
       ```bash
       git fetch origin
       ```
    2. See all branchs in your local
       ```bash
       git branch -r
       ```
    3. Checkout to branch you want develop
       ```bash
       git checkout <your-branch-to-checkout>
       ```
    4. Complete 👍
  
  - With executing the default invocation of git pull will is equivalent to `git fetch origin HEAD` and `git merge HEAD` where `HEAD` is ref pointing to the current branch.
    1. Checkout to branch you want update or pull
       ```bash
       git checkout <branch-you-want-update-or-pull>
       ```
    2. Pull the current branch.
       ```bash
       git pull origin <current-branch>
       ```
    3. Complete 👍

## If the default branch has been renamed!, If you have a local clone, you can update it by running the following commands. 👇

> ```<old-default-branch>``` is named to ```<new-default-branch>```
> ```bash
> git branch -m <old default branch> <new-default-branch>
> git fetch origin
> git branch -u origin/<new-default-branch> <new-default-branch>
> git remote set-head origin -a
>  ```

## GUI frames

#### Sign in page 👇

  ![Capture](https://github.com/KimmyLps/exercise_detection/assets/94822460/2f428349-c72a-48db-b095-944fdf501e97)

#### Sign up page 👇

  ![Capture1](https://github.com/KimmyLps/exercise_detection/assets/94822460/36f3a774-8057-40fd-a950-36c04c7a0782)

#### Dashboard page 👇

  ![image](https://github.com/KimmyLps/exercise_detection/assets/94822460/ad9d72ec-9ace-44c3-875b-5a82999d2cf9)

#### Database design diagram 👇

  ![Exercise_detection](https://github.com/KimmyLps/exercise_detection/assets/94822460/1cdb5e08-1bc5-4fe1-958f-63eaac2ffe1c)
