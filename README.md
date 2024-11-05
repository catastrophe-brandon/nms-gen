# nms_gen

## Overview 

`nms_gen` is a cli tool used to inject pixel art into a No Man's Sky save file as base parts/geometry.

The process look like this:

1. Export the base data as JSON using NMS save editor.
2. Run `nms_gen` with the correct inputs to update the save data (see example use for how to do this).
3. Import the updated base data using NMS save editor.

## Example Use

`python main.py input_bases/bubble_base.json sprites/mega_man_standing.png 40 --o my_output_file.json`

In this example `input_bases/bubble_base.json` is the origin JSON file exported from NMS save editor.

`sprites/mega_man_standing.png` is the input sprite to inject into the base data.

The `40` is simply a z-up value to elevate the base geometry so that it doesn't get stuck in the terrain. You may need to experiment with this depending on the terrain around your base.

`--o my_output_file.json` is how you specify the updated save data.

If your import is successful you'll see something like this:

```
Tile coord: (100.0, 120.0, 40.0)
offset: 573 (21,24)
Tile coord: (105.0, 120.0, 40.0)
Writing output JSON file to my_output_file.json
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
```

Note: This program is only verified to work with the example sprites in the `sprites` directory. Enhancements are needed to support a broader variety of sprites.

