# Militsioner Spawn Menu

## Description

Adds a spawn menu to Militsioner so you can freely spawn items into the game.

Press `F4` to open the menu, find the item you want, and select **Spawn**.

## Bookmarks
- [Steam — New Playtest](#steam--new-playtest)
  - [Uninstallation](#steam-uninstallation)
- [Patreon — Old Playtest](#patreon--old-playtest)
  - [Uninstallation](#patreon-uninstallation)

## Steam — New Playtest

### Installation

1. Install the [UE4SS nightly build](https://github.com/UE4SS-RE/RE-UE4SS/releases/tag/experimental-latest).
2. Launch the game once to generate the required directories.
3. Extract the spawn menu ZIP file.
4. Copy the `SpawnerMenu` folder into the UE4SS `Mods` directory:

   ```text
   <Game Folder>\TallProject\Binaries\Win64\ue4ss\Mods\
   ```

5. Open `mods.txt` in that directory and add the following line near the bottom of the list, above the keybinds entry:

   ```text
   SpawnerMenu : 1
   ```

### Steam Uninstallation

1. Delete the `SpawnerMenu` folder from:

   ```text
   <Game Folder>\TallProject\Binaries\Win64\ue4ss\Mods\
   ```

2. Remove the following line from `mods.txt`:

   ```text
   SpawnerMenu : 1
   ```

#### Optional: Remove UE4SS Entirely

If you no longer need UE4SS for other mods, delete these items from `<Game Folder>\TallProject\Binaries\Win64\`:

- `dwmapi.dll`
- `ue4ss` folder

> Removing UE4SS and its `Mods` folder also removes any other mods installed there.

## Patreon — Old Playtest

### Installation

1. Install [UE4SS](https://github.com/UE4SS-RE/RE-UE4SS).
2. Launch the game once to generate the required directories.
3. Extract the spawn menu ZIP file.
4. Copy the `SpawnerMenu` folder into the `Mods` directory:

   ```text
   <Game Folder>\TallProject\Binaries\Win64\Mods\
   ```

5. Open `mods.txt` in that directory and add the following line near the bottom of the list, above the keybinds entry:

   ```text
   SpawnerMenu : 1
   ```

### Patreon Uninstallation

1. Delete the `SpawnerMenu` folder from:

   ```text
   <Game Folder>\TallProject\Binaries\Win64\Mods\
   ```

2. Remove the following line from `mods.txt`:

   ```text
   SpawnerMenu : 1
   ```

#### Optional: Remove UE4SS Entirely

If you no longer need UE4SS for other mods, delete these items from `<Game Folder>\TallProject\Binaries\Win64\`:

- `dwmapi.dll`
- `UE4SS.dll`
- `UE4SS-settings.ini`
- `UE4SS.log`
- `Mods` folder

> Removing UE4SS and its `Mods` folder also removes any other mods installed there.

## Game Folder Location

Replace `<Game Folder>` with your game's installation directory, such as:

```text
SteamLibrary\steamapps\common\Militsioner Playtest
```

or:

```text
SteamLibrary\steamapps\common\Militsioner Demo
```
