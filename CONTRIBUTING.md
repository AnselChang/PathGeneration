# Issues

I will be keeping an active list of current issues/features that need to be worked on in the WPI Vex discord, with assignments, timeline estimates, and updates there.

If you are interested in contributing, I would recommend picking up one of those features to work on.

# Setting up a new branch

To contribute to the code base, first clone this project into the repo and install the necessary libraries, as directed in the README. If you've already done this in the past, type 'git pull' to sync your local repo to the remote repository.

The main branch is protected from direct modifications. To make changes, create a new branch with `git checkout -b [branch-name]`

This will give you free reign to write and test experimental code. To add new files, make sure to `git add [file-name]` to stage those new files. Commit frequently with  `git commit -am "[message]"`, and be sure to write a descriptive message that includes the issue number like so: `#4`

# Merging your changes into the remote respository

If you're ready to have your changes reviewed and integrated into the main branch, type `git push origin [branch-name]`. This will push your branch with it's code changes onto the remote respository.

Then, go to the github website, select your branch, and look for a "Create Pull Request" button. Click on it to request merging onto the main branch. There is a short approval process where a different contributor must review and accept your changes for them to be merged into the main branch.

If your request gets denied, try to improve your code from the provided comments, or reach out to me (Ansel) for further clarification.

Thank you for bringing this huge project one step closer to the light at the end of the tunnel!
