## PREGIT V1

### Fucntionalities
- init - create .pregit/ directory
- add - stage files with the same hashed with Git
- commit - commit files with the same hashed and structure with Git
- log - view commit log the structure is relatively similar to Git

### 1. Init
> Create .pregit/ directory
```python
    python3 main/pregit.python init --help # show help
    python3 main/pregit.python init --path . # create .pregit/ at the current directory
    python3 main/pregit.python init -p <your_path> # create .pregit/ at the current directory
```
### 2. Add
> create blob files and save to .pregit/objects/<first_2_hashed_character>/<the_last_38_characters>
```python
    python3 main/pregit.python add --help # show help
    python3 main/pregit.python add --file . # add all files in the directory t
    python3 main/pregit.python add -f <file_1> <file_2> <file_3> # add several files to staging
```
### 3. Commit
> create tree + commit files and save to .pregit/objects/<first_2_hashed_character>/<the_last_38_characters>
```python
    python3 main/pregit.python commit --help # show help
    python3 main/pregit.python commit --message <your_msg>  # create commit with message
    python3 main/pregit.python commit -m  <your_msg> # create commit with message
```
### 4. Log
> Show commit log
```python
    python3 main/pregit.python log --help # show help
    python3 main/pregit.python log  # show log
    python3 main/pregit.python log --oneline  # show log in oneline each
```
### 5.Checkout
> checkout at commit
```python
    python3 main/pregit.python commit --help # show help
    python3 main/pregit.python commit --sha1 <commit>  # checkout at commit
    python3 main/pregit.python commit --branch <branch> # checkout at branch ( at latest commit )
```

### Example

> create .pregit/
```python
    main/pregit.py init -p . # create at current directory
```
> create some files
```python
    echo "hello" > index.js
    echo "mimi" > index2.js

```
> add + commit file
```python
    # add + commit index.js
    main/pregit.py add -f  index.js # add index.js to .pregit/index
    # when we check the .pregit/objects/ we will see 1 blob file
    main/pregit.py commit -m  'add index.js' # # create tree file and commit file
    # in total at this stage we have 3 files

    # continue with index2.js
    main/pregit.py add -f  index2.js # add index.js to .pregit/index
    # when we check the .pregit/objects/ we will see 1 blob file
    main/pregit.py commit -m  'add index2.js' # # create tree file and commit file
    # in total at this stage we have 3 files
```
> log
```python
    main/pregit.py log # show log
    # Commit: fa27fe3b243c5a7206f05a0457e3cae7a33fc10d
    # Author: <yourname> - <yourname@email.com>
    # Date: Sat Feb 19 16:22:07 2022

    #         commit:add index2.js

    # ========================================
    # Commit: 906a4210c6836869ae845c5e7764b53b05a00f24
    # Author: <yourname> - <yourname@email.com>
    # Date: Sat Feb 19 16:21:26 2022

    #         commit(initial):add index.js

    # ========================================
```

> checkout
```python
    # modify index.js
    echo "+ world!" >> index.js
    main/pregit.py add -f index.js
    main/pregit.py commit -m 'modify index.js'
    # total we have 9 files
    # check log we have
    main/pregit.py log --oneline
    # Commit: ba06f71106967a2e9e45f3dc656f487c167540e0
    # Author: <yourname> - <yourname@email.com>
    # Date: Sat Feb 19 16:42:38 2022

    #         commit:modify index.js

    # ========================================
    # Commit: fa27fe3b243c5a7206f05a0457e3cae7a33fc10d
    # Author: <yourname> - <yourname@email.com>
    # Date: Sat Feb 19 16:22:07 2022

    #         commit:add index2.js

    # ========================================
    # Commit: 906a4210c6836869ae845c5e7764b53b05a00f24
    # Author: <yourname> - <yourname@email.com>
    # Date: Sat Feb 19 16:21:26 2022

    #         commit(initial):add index.js

    # ========================================

    # checkout from the second commit
    main/pregit.py checkout --sha1 fa27fe3b243c5a7206f05a0457e3cae7a33fc10d

    # check log
    main/pregit.py log --oneline
    # fa27fe - add index2.js
    # 906a42 - add index.js
    cat index.js
    # hello
    # checkout master
    main/pregit.py checkout -b master
    # check log
    # ba06f7 - modify index.js

    # fa27fe - add index2.js

    # 906a42 - add index.js

```