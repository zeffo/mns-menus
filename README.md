# mns-menus
Package to help create CLI, menu based applications. 

# Installation
`git clone https://github.com/zeffo/mns-menus.git`

# Example Program:

```py

from mnsmenus import Handler, MissingRequiredArguments

handler = Handler(prompt='Enter Command: ')

@handler.error_handler
def errors(ctx, exc):
    if isinstance(exc, MissingRequiredArguments):
        print(f"Missing Arguments!\n{ctx.command.usage}")
    else:
        raise exc

@handler.command(usage="sound (animal)")        # This decorator provides core functionality for creating CLI commands. You must specify the usage.
def sound(ctx, animal):                         # The command name will be taken from the function name.
    """Shows the sound of the given animal"""   # The command description will be obtained from the docstring.
    sounds = {'dog': 'woof', 'cat': 'meow'}     # When the command is used in the command line, this function will be called.
    print(sounds.get(animal))
    
    
# Start to listen for commands. *This will block the working thread*
handler.start()
    
```
Output:

![image](https://media.discordapp.net/attachments/734363926208184320/852818765384384512/unknown.png)
