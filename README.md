<h1>pymanga</h1>

pymanga is a command-line tool to download manga from mangadex.<br>
It download manga in the form of a `.cbz` file, which is a comic book archive file.<br>
This is usefull if you got a e-reader or a tablet and you want to read manga on it.

<h1>Table of content</h1>

- [Installation](#installation)
- [Usage](#usage)
  - [Error handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

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

# Download all french chapters of Jujutsu Kaisen
you@yourmachine:~$ python -m pymanga download "Jujutsu Kaisen" --language fr

# Download all chapters of Jujutsu Kaisen in the ./jjk folder
you@yourmachine:~$ python -m pymanga download "Jujutsu Kaisen" --output ./jjk
```

## Error handling

The package raises the `MangadexClientError` when an error occurs while interacting with the mangadex API.

```python
from pymanga.exceptions import MangadexClientError

try:
    # Do something
except MangadexClientError as e:
    print(e)
```

# Contributing

Contributions to `pymanga` are welcome! If you encounter any issues or have suggestions for improvements, please open an issue on the project's GitHub repository.<br>
Before submitting a pull request, make sure to run the tests and ensure that your changes do not break the existing functionality. Add tests for any new features or fixes you introduce.

# License

`pymanga` is open-source software released under the [MIT License](https://opensource.org/license/mit/). Feel free to use, modify, and distribute it according to the terms of the license.

# Acknowledgements

This project was developed by [jordan95v](https://github.com/jordan95v).<br>
I would like to thank the Mangadex team for providing a powerful and comprehensive API, be sure to download only if you intend to read the manga and not to stockpile it and the books unread.


<h1>Thanks for reading.</h1>

<img src="https://media1.tenor.com/m/_Zc9LQ9QtBsAAAAC/naruto-kakashi.gif" width="100%">