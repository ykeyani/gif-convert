#gif-convert
A simple gif conversion tool with a multiplatform GUI.

## Dependencies
- Python 3.7?
- Imagemagick
- Gifsicle

## Dependency Installation
### macOS
You can manually install [homebrew](https://brew.sh), [imagemagick](https://formulae.brew.sh/formula/imagemagick#default) and [gifsicle](https://formulae.brew.sh/formula/gifsicle#default) or you can run the installer script provided.
#### Use the Installer
```shell script
cd <gif-convert directory>
chmod +x install-macos.sh
./install-macos.sh
```
#### Manual Installation with homebrew
```shell script
brew install imagemagick
brew install gifsicle
```

### Debian/Ubuntu
Using the package manager
```shell script
sudo apt update && sudo apt install -y gifsicle imagemagick
```

### Windows (amd64)
The app will use the bundled binaries but you will still need a working [python 3.7+](https://www.python.org/downloads/windows/) Installed on your system.


## Usage
### Linux / macOS
`python3 gif-convert.py`

### Windows
`python gif-convert.py`