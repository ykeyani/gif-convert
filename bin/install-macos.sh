#!/usr/bin/env bash

# check for homebrew
if command -v brew > /dev/null; then
  echo "homebrew available..."
else
  echo "installing homebrew..."
  /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
fi

# update homebrew
brew update

# check for imagemagick convert
if command -v convert > /dev/null; then
  echo "imagemagick convert available"
else
  echo "installing imagemagick"
  brew install imagemagick
fi

# check for gifsicle
if command -v gifsicle > /dev/null; then
  echo "gifsicle available"
else
  echo "installing gifsicle"
  brew install gifsicle
fi
