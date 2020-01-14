#!/usr/bin/env bash
#  Copyright (c) 2020. Yasin Keyani
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

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
