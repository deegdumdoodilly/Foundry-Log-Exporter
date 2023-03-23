Requires python3 and the requests library.

Run the python script and supply the log as an argument. For example, if you put the log in the same directory (folder) as the python file, you can perform the following command to run the translation (on a Windows machine), replacing `foundry_log.txt` with the name of your chat log file:

`py translator.py foundry_log.txt`

The script expects a `preamble.txt` to be included in the same directory where it is run. In the last few lines, you can edit the image that usually accompanies the top of the log to something more suitable for your game.

The script will look for a `mappings.json` file in the same directory. If it exists, it will map the names of speakers to specific images. For example, the following mappings.json file:

```
{
    "Skeletor": "https://upload.wikimedia.org/wikipedia/en/8/8a/Skeletor-spoo.jpg",
    "Twilight Sparkle": "https://upload.wikimedia.org/wikipedia/en/b/b4/PrincessTwilightSparkle.png"
}
```

Will cause all messages written by someone named 'Skeletor' or 'Twilight Sparkle' to be represented with the respective images.

Reach out to me at deeg#4116 on discord if you encounter any issues or have feature requests.