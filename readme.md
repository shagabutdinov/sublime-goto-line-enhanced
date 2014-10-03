# Sublime GotoLineEnhanced plugin

Replacement for default sublime goto line.


### Demo

![Demo](https://raw.github.com/shagabutdinov/sublime-goto-line-enhanced/master/demo/demo.gif "Demo")


### WARNING

This plugin remap "goto line" functionality in unobvious way (because sublime
does not allow to bind to "enter" in quick search panel). When you need to go to
line hit "tab" instead of "enter".


### Reason

- Bright highlighting for line; even when typing fast it is always possible to
see to which line jump will be made

- Symbols mapping; it remaps keys from "n" to "p" to according "1" to "9", "n"
for "0"; it is faster to hit symbols keys than numeric keys; it is also possible
to enter line number with one hand (it is more comfortable for me)

- Go to first char of line instead of default go to beginning of line

- Does not allow to input symbols to avoid occasional keyhits

### Installation

This plugin is part of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
plugin set. You can install sublime-enhanced and this plugin will be installed
automatically.

If you would like to install this package separately check "Installing packages
separately" section of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
package.


### Features

Goto first character of given line with bright highlighting and not-numeric
keys.


### Usage

Hit keyboard shortcut to avoke panel, enter line number and hit "tab" to go to
this line. You also can use following keys to enter numbers:

| key | number |
|-----|--------|
| n   | 0      |
| m   | 1      |
| ,   | 2      |
| .   | 3      |
| j   | 4      |
| k   | 5      |
| l   | 6      |
| u   | 7      |
| i   | 8      |
| o   | 9      |

This values hard-binded to plugin and can be changed only thorugh source-code.


### Commands

| Description            | Keyboard shortcuts | Command palette                    |
|------------------------|--------------------|------------------------------------|
| Prompt goto line       | ctrl+g             | GotoLineEnhanced: Prompt goto line |
| Goto line              | tab                |                                    |


### Dependencies

- https://github.com/shagabutdinov/sublime-quick-search-enhanced