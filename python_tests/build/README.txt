# Python

# Instructions for installing Python and Dependencies

### Install PYENV
1. Open your terminal, and run:
    - `curl https://pyenv.run | bash`
2. After installed, in your terminal you will get a message saying you have not added pyenv to your load path, and telling you to add the following to your ~/.bashrc:
    - `export PATH="/Users/<username>/.pyenv/bin:$PATH"`
    - `eval "$(pyenv init -)"`
    - `eval "$(pyenv virtualenv-init -)"`
    - ^^^ your username will be in place of `<username>` here.
3. Copy those three lines, and then open your ~/.bash_profile (not .bashrc) using nano:
    - `nano ~/.bash_profile`
4. Paste the lines you copied underneath whatever is currently in your .bash_profile, as well as these two lines:
    - `export PATH="$PYENV_ROOT/shims:$PATH"`
    - `export PATH="$PYENV_ROOT/bin:$PATH"`
5. So your .bash_profile should now have this (there is an additional mysql command at the top):
    - `export PATH=$PATH:/usr/local/mysql/bin`
    - `export PATH="/Users/<username>/.pyenv/bin:$PATH"`
    - `export PATH="$PYENV_ROOT/shims:$PATH"`
    - `export PATH="$PYENV_ROOT/bin:$PATH"`
    - `eval "$(pyenv init -)"` (if you are on Big Sur, you need to do this instead: eval "$(pyenv init --path)")
    - `eval "$(pyenv virtualenv-init -)"`
6. If you used nano to edit your .bash_profile, save your changes by clicking Ctrl + O, return, then Ctrl + X.
7. Reboot Terminal by quitting the app and then reopening it
8. After reopening, run the command:
    - `pyenv version`
    - The shell should now recognize the `pyenv` command and print the current python version set by pyenv.
    - If it gives you '-bash: pyenv: command not found', double check your .bash_profile, because your path is probably wrong.

### Install Python
1. Install python version 3.8.2 and set it as your global python version:
    - `pyenv install 3.8.2`
    - `pyenv global 3.8.2`
2. Run `pyenv version` again to ensure that 3.8.2 is the current python version.

### Install pipenv
- We will use pipenv for package management.
- run "pip3 --version" to ensure that pip3 is installed on your machine
- Keep in mind since we just installed Python 3, in your terminal you will likely need to use 'pip3' instead of 'pip'
- Once inside a Virtual Environment, you will be able to just use 'pip' for installs
- To install pipenv globally, run:
    - `sudo -H pip3 install -U pipenv`
- after doing this, you will need to update your PATH.  Navigate to your bash_profile:
    - `nano ~/.bash_profile`
- add the following lines to your bash_profile:
    - `PYTHON_BIN_PATH="$(python3 -m site --user-base)/bin"`
    - `export PATH="$PATH:$PYTHON_BIN_PATH"`
- then do CTRL + 0, Enter, CTRL + X
- Set the pipenv python version with the following:
    - `pipenv install --python 3.8.2`
- Go ahead and close your terminal



### Install & Configure PyCharm
1. Search for 'pycharm' on google and download the community edition.
2. Open PyCharm, and select 'Check out from VCS' on the right.
3. Log in to GitLab, get the 'Clone' repo URL, paste it in, and enter your git credentials.
4. Click PyCharm -> Preferences -> Project name -> Interpreter -> Add Interpreter (gear sign to the right) and select Pipenv Environment on the left.
   In the drop down, select Python 3.8
5. Next you need to put in the path for your pipenv executable, which should be the same as the path you added to your `.bash_profile` when installing pipenv (/Users/<username>/.local/bin/pipenv).
   If it autodetected your executable, then congratulations, just click Ok.
   If this does not recognize the pipenv executable, try this one: `/Users/<username>/Library/Python/3.8/bin/pipenv`.
   If that still does not find it, then in your terminal run: 'type pipenv'.  This will give you your executable path.
6. Uncheck the checkbox that says 'install packages' and then click OK. This should set up your Pipenv virtual environment and create the interpreter.
   Once finished, make sure the Pipenv interpeter is listed as your current interpreter (bottom-right).
7. If you have your Terminal open in PyCharm, close and reopen it and you should see your virtual environment name to the right of the Terminal line.

### Install Project Packages
1. In your PyCharm Terminal, run `pipenv install` to make sure everything from the Pipfile is installed.
2. If you run into an error with mysql, run `pipenv install mysqlclient`
3. If you run into an issue with step 2, open your Pycharm Terminal and run this `export PATH=$PATH:/usr/local/mysql/bin`,
   and repeat step 2.
4. Then run `pipenv install` again.  This should install mysql if you had trouble with it before.

### Configure Pytest
1. In PyCharm, open Preferences -> Tools -> Python Integrated Tools -> and change your Testing option to PyTest.
2. Click OK.
3. Then go to Run (in the top toolbar) -> Edit configurations.
4. If there is a default test runner for 'Python' highlight it and click the minus sign to remove it.
5. Click the `+` sign, select pytest, click the Script Path bubble next to Target, and set it to this: `/Users/<username>/PycharmProjects/python/tests/*.py`.
6. Click apply and OK.

### Test it
- At this point, you should be up and running.
- Go ahead and run a test and make sure it opens, runs, and closes.