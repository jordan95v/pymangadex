<h1>pymanga</h1>

# Installation

To install pymanga, simply run:

```bash
you@yourmachine:~$ python -m venv venv
you@yourmachine:~$ source venv/bin/activate # or venv\Scripts\activate.bat on Windows
(venv) you@yourmachine:~$ pip install . # or pip install .[dev] for development dependencies
```

And you're good to go!

# Usage

The main entrypoint for pymanga is the `pymanga` command. You can use it to download manga from mangadex.

```bash
you@yourmachine:~$ python -m pymanga
```

For more information, run:

```bash
you@yourmachine:~$ python -m pymanga --help
```

For example, if you want to download `Jujutsu Kaisen`, you can do as follow:
    
```bash
# Download all chapters of Jujutsu Kaisen
you@yourmachine:~$ python -m pymanga download "Jujutsu Kaisen"

# Download chapters 1 to 10 of Jujutsu Kaisen
you@yourmachine:~$ python -m pymanga download "Jujutsu Kaisen" --from-chapter 1 --to-chapter 10
```

<h1>Thanks for reading.</h1>

<img src="https://media1.tenor.com/m/_Zc9LQ9QtBsAAAAC/naruto-kakashi.gif" width="100%">