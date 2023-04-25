# LfB-Institute-Project
Implementation of a simple cheat detection system using face regconition techniques and audio processing. 

## How to Install 
<u> **Prerequisites:** </u> You need an personal access token when you clone the repo, follow this [link](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) to know how. I recommend also you [install git credential manager](https://github.com/git-ecosystem/git-credential-manager/blob/release/docs/install.md) so you don't have to enter this long ass token everytime you want to do something with the remote repo.

Go to your local directory that you guys want save the project in the terminal and enter this line: 
```
git clone https://github.com/l-nguyen03/LfB-Institute-Project.git .
```
The repo here **_include the dockerfile also_** so that we all have the same dockerfile and can receive updated one if any changes are made so please **don't save it with the directory that has the same dockerfile that Ankit sent.** **_If you are using MacOS with Apple Silicon then just delete the Dockerfile and rename the Dockerfile_arm64 to Dockerfile only._**

## Example on how to use Git and GitHub for collaboration on the project:

**_Example: Ali wants to implement face comparison_**

1. Ali will clone the repository to his local machine using the git clone command. This will create a local copy of the repository on his machine.
2. He then creates a branch for his functionality with ``git branch branch-name`` followed by name of the functionality, ex. 
```
git branch face_regconition.
```
3. He now goes to his branch by using the command ``git checkout -b branch-name`` followed by name of the newly created branch.
4. He can now write code like normal and save it in the same directory as the git repo.
5. After he is done with the code, he can go to the terminal, he can type this command ``git add`` followed by ``git commit -m "some message"`` where message should explain what he has done, like "implemented facial comparison", or "add message forwarding". (remember that if you guys start a new working session, remember to always go to your branch first by using ``git branch branch-name`` before ``git add)
6. He then pushes his changes to remote branch. Use the ``git push origin branch-name`` command to push your changes to the remote branch.
7. He will then go to GitHub and create a pull request. Then the team can review his code and give feedbacks, then I will merge the code to main branch.
8. Once the changes are merged, everyone in the team can pull the updated code to their local machine by using ``git pull origin main``.

## GitHub and Git basic commands: 
1. ``git clone <url>`` - Clone a repository to your local machine.
2. ``git pull`` - Pull changes from the remote repository.
3. ``git push`` - Push changes to the remote repository.
4. ``git branch`` - List all branches in the repository.
5. ``git branch <branch>`` - Create a new branch.
6. ``git checkout <branch>`` - Switch to the specified branch.
7. ``git merge <branch>`` - Merge the specified branch into the current branch.
8. ``git init`` - Initialize a new Git repository in the current directory.
9. ``git add <file>`` - Add changes to the specified file to the staging area.
10. ``git add .`` - Add all changes to the staging area.
11. ``git commit -m "<message>"`` - Commit changes with the specified message.
12. ``git status`` - Display the current status of the repository.
13. ``git log`` - Show the commit history.
14. ``git diff <file>`` - Show the difference between the working directory and the last commit for the specified file.
15. ``git fetch`` - Fetch changes from the remote repository without merging them.
