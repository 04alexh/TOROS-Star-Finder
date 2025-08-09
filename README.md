# TOROS-Star-Finder
This function finds stars in a calibrated TOROS image.

## What code is doing
The user inputs the calibrated TOROS image as well as a WCS solution for the field, and this program will use DAOStarFinder from *photutils* to find stellar sources in the image. It will then put all of these sources into a list which can be saved directly to disk or returned into another function. There is masking capabilities as well for crowded fields.

## Use
This section will explain the function parameters. (**function_parameter** [data type]: Explanation of parameter.) \
\
\
**science_file** [str]: Path to the calibrated image from which you want to identify stars.
\
\
**star_list_file** [str]: Path to the csv the program will create containing information about the found stars.
\
\
**wcs_file** [str]: Path to the WCS solution of your frame.
\
\
**want_star_list** [bool]: If true, program will save the list of stellar sources as a csv to *star_list_file*. Set to TRUE by default.
\
\
**edge_buffer** [int]: Due to vignetting, edges of images can sometimes contain artifacts that get misidentified as stars. This parameter allows for a buffer away from the image edges that the star finder will not detect stars in. Set to 200 by default.
\
\
**use_mask** [bool]: If true, program will mask an area of the image and not detect any stars within the mask. Set to FALSE by default.
\
\
**cx** [float]: X-Pixel center of mask. Set to 0.0 by default.
\
\
**cy** [float]: Y-Pixel center of mask. Set to 0.0 by default.
\
\
**r** [float]: Radius of mask. Set to 0.0 by default.

