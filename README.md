SublimeKnifeSolo
==========================================

This plugin provides some [knife solo](http://matschaffer.github.com/knife-solo/) command.

+ knife solo prepare
+ knife solo cook


OS Support
----------------------------
+ Mac OS only

Installation
----------------------------
You need to pre-install [knife solo](http://matschaffer.github.com/knife-solo/)

### with package controlle (recommended)
If you have the [Package Control package](http://wbond.net/sublime_packages/package_control) installed, you can install from inside Sublime Text itself.

1. Open the Command Palette (command + shift + p)
2. select "Package Control: Install Package"
3. Search for ""KnifeSolo" and you're done!

### with git
    git clone https://github.com/amazedkoumei/SublimeKnifeSolo.git ~/Library/Application\ Support/Sublime\ Text 2/Packages/SublimeKnifeSolo
    

Usage
-----

### configration

1. open controll panel ( command + shift + p )
2. type "knifesolo"
3. choose "Preference: SublimeKnifeSolo settings - User"

You can see sample config file

1. open controll panel ( command + shift + p )
2. type "knifesolo"
3. choose "Preference: SublimeKnifeSolo settings - Default"


### knife solo prepare

On the file that is in same directory as solo.rb or in lower level

1. open controll panel ( command + shift + p )
2. type "knifesolo"
3. choose "SublimeKnifeSolo prepare"
4. choose your host

### knife solo cook

On the file that is in same directory as solo.rb or in lower level

1. open controll panel ( command + shift + p )
2. type "knifesolo"
3. choose "SublimeKnifeSolo cook"
4. choose your host
