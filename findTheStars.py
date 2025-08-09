def findTheStars(science_file, star_list_file, wcs_file, want_star_list=True, edge_buffer=200, use_mask=False, cx=0, cy=0, r=0):

    import os
    from astropy.io import fits
    from astropy.stats import sigma_clipped_stats
    from photutils.detection import DAOStarFinder
    import numpy as np
    from photutils.aperture import CircularAperture
    from astropy.table import Table, Column
    from astropy.wcs import WCS


    if os.path.exists(science_file) == False:

        print(f"Science file {science_file} does not exist!")
        return

    ###Defines tuples to encode image and header data
    (science, science_header) = fits.getdata(science_file, header=True)


    ###Obtain std for starfinder
    (mean, median, std) = sigma_clipped_stats(data=science, sigma=3.0)
    starFind = DAOStarFinder(fwhm=7.5, threshold = 5*std)  # fullwidthhalfmax of 10 over 5sigma

    ###Apply mask if need
    if use_mask:

        mask = np.zeros(science.shape, dtype=bool)
        (yy, xx) = np.indices(science.shape)
        cluster_mask = (xx - cx) ** 2 + (yy - cy) ** 2 < r ** 2
        mask[cluster_mask] = True

        sources = starFind(science, mask=mask)

    else:

        sources = starFind(science)


    ###Dont search for stars on the edge
    (h , w) = science.shape
    sources = sources[
        (sources['xcentroid'] > edge_buffer) &
        (sources['xcentroid'] < w - edge_buffer) &
        (sources['ycentroid'] > edge_buffer) &
        (sources['ycentroid'] < h - edge_buffer)
    ]

    ###Also save date and time of event
    date = str(science_header['DATE'].split('T')[0])
    time = science_header['DATE'].split('T')[1]

    # Make lists of date and time same length as sources
    sources_size = len(sources)

    date_list = []
    time_list = []


    for i in range(sources_size):

        date_list.append(str(date))
        time_list.append(str(time))


    ###Put columns with date and time for each star
    date_column = Column(date_list , name = "Date")
    time_column = Column(time_list , name = "Time")

    sources.add_column(date_column) #Adds date column to csv
    sources.add_column(time_column) #Adds time column to csv

    for col in sources.colnames:
        if col not in ('id', 'npix', 'Date', 'Time'):
            sources[col].info.format = '%.2f'

    sources.pprint(max_width=76)

    ###Lets get sky positions too
    positions = np.transpose((sources['xcentroid'], sources['ycentroid']))
    apertures = CircularAperture(positions, r=10)


    ###Load in astrometry.net WCS object
    wcs_header = fits.getheader(wcs_file)
    telescope = WCS(wcs_header)

    sky_apertures = apertures.to_sky(telescope)
    sky_positions = sky_apertures.positions

    RAcolumn = Column(sky_positions.ra.deg, name="RA")
    DECcolumn = Column(sky_positions.dec.deg, name="DEC")

    sources.add_column(RAcolumn)
    sources.add_column(DECcolumn)

    ###Writes star_list as a csv file.
    if want_star_list:
        sources.write(star_list_file, delimiter=',', format='ascii', overwrite=True)

    ###Lets take the data from the astropy table and turn it into positions

    ###Return a tuple the star positions and apertures
    return positions, apertures
