#!/usr/bin/env python

"""
Plot an LAI map and a biome map

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (18.11.2020)"
__email__ = "mdekauwe@gmail.com"

import os
import sys

import xarray as xr
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import cartopy.crs as ccrs
import cartopy
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import sys
import matplotlib.ticker as mticker
from cartopy.mpl.geoaxes import GeoAxes
from mpl_toolkits.axes_grid1 import AxesGrid

def plot_LAI(ds):

    fig = plt.figure(figsize=(9, 6))
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams['font.size'] = "14"
    plt.rcParams['font.sans-serif'] = "Helvetica"

    #cmap = plt.cm.get_cmap('viridis', 6) # discrete colour map
    cmap = plt.cm.get_cmap('viridis') # discrete colour map
    #cmap = plt.cm.get_cmap('RdYlBu', 6) # discrete colour map

    projection = ccrs.PlateCarree()
    axes_class = (GeoAxes, dict(map_projection=projection))
    rows = 1
    cols = 1

    axgr = AxesGrid(fig, 111, axes_class=axes_class,
                    nrows_ncols=(rows, cols),
                    axes_pad=0.2,
                    cbar_location='right',
                    cbar_mode='single',
                    cbar_pad=0.5,
                    cbar_size='5%',
                    label_mode='')  # note the empty label_mode

    for i, ax in enumerate(axgr):
        # add a subplot into the array of plots
        #ax = fig.add_subplot(rows, cols, i+1, projection=ccrs.PlateCarree())
        #plims = plot_map(ax, ds.Total[90:160,580:670],cmap, i)
        plims = plot_map(ax, ds.Total[:,:], cmap, i)

    cbar = axgr.cbar_axes[0].colorbar(plims)
    cbar.ax.set_title("LAI (m$^{2}$ m$^{-2}$)", fontsize=16)


    fig.savefig( "LAI.png", dpi=150, bbox_inches='tight',
                pad_inches=0.1)

def plot_map(ax, var, cmap, i):
    vmin, vmax = 0., 6.
    top, bottom = 90, -90
    left, right = -180, 180
    img = ax.imshow(var, origin='lower',
                    transform=ccrs.PlateCarree(),
                    interpolation='nearest', cmap=cmap,
                    extent=(left, right, bottom, top),
                    vmin=vmin, vmax=vmax)
    ax.coastlines(resolution='10m', linewidth=1.0, color='black')
    #ax.add_feature(cartopy.feature.OCEAN)

    ax.set_xlim(112, 154)
    ax.set_ylim(-44, -10)

    if i == 0 or i >= 5:

        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                          linewidth=0.5, color='black', alpha=0.5,
                          linestyle='--')
    else:
        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False,
                          linewidth=0.5, color='black', alpha=0.5,
                          linestyle='--')

    #if i < 5:
    #    gl.xlabels_bottom = False
    if i > 5:
        gl.ylabels_left = False

    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlines = False
    gl.ylines = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER

    #gl.xlocator = mticker.FixedLocator([141, 145,  149, 153])
    #gl.ylocator = mticker.FixedLocator([-29, -32, -35, -38])

    return img

def plot_biomes(ds):

    #plt.imshow(ds.Total[90:160,580:670])
    #plt.colorbar()
    #plt.show()
    biome = ds.Total * np.nan

    total_tree = ds.BNE+ds.BNS+ds.TeNE+ds.TeBS+ds.IBS+ds.TeBE+\
                    ds.TrBE+ds.TrIBE+ds.TrBR

    boreal_tree = ds.BNE+ds.BNS+ds.IBS
    temperate_tree = ds.TeNE+ds.TeBS+ds.IBS+ds.TeBE+ds.IBS
    tropical_tree = ds.TrBE+ds.TrIBE+ds.TrBR
    grass = ds.C3G + ds.C4G

    # Boreal deciduous forest/woodland - BNS dominant
    biome = np.where((boreal_tree > total_tree * 0.8) &
                     (total_tree > 0.5) &
                     ( (ds.BNS>ds.BNE) &
                       (ds.BNS>ds.TeNE) &
                       (ds.BNS>ds.TeBS) &
                       (ds.BNS>ds.IBS) &
                       (ds.BNS>ds.TeBE) &
                       (ds.BNS>ds.TrBE) &
                       (ds.BNS>ds.TrIBE) &
                       (ds.BNS>ds.TrBR) ),
                      0, biome)

    # Boreal evergeeen forest/woodland - BNE or IBS (BBS) dominant
    biome = np.where((boreal_tree > total_tree * 0.8) &
                     (total_tree > 0.5) &
                     ( ((ds.BNE>ds.BNS) | (ds.IBS>ds.BNS)) &
                       ((ds.BNE>ds.TeNE) | (ds.IBS>ds.TeNE)) &
                       ((ds.BNE>ds.TeBS) | (ds.IBS>ds.TeBS)) &
                       ((ds.BNE>ds.TeBE) | (ds.IBS>ds.TeBE)) &
                       ((ds.BNE>ds.TrBE) | (ds.IBS>ds.TrBE)) &
                       ((ds.BNE>ds.TrIBE) | (ds.IBS>ds.TrIBE)) &
                       ((ds.BNE>ds.TrBR) | (ds.IBS>ds.TrBR)) ),
                      1, biome)

    # Temperate / boral mixed forest
    biome = np.where((total_tree * 0.2 < boreal_tree) &
                     (boreal_tree < total_tree * 0.8) &
                     (total_tree * 0.2 < temperate_tree) &
                     (temperate_tree < total_tree * 0.8),
                     2, biome)

    # Temperate conifer forest
    biome = np.where((temperate_tree > total_tree * 0.8) &
                     (total_tree > 0.5) &
                     ( (ds.TeNE>ds.BNE) &
                       (ds.TeNE>ds.BNS) &
                       (ds.TeNE>ds.TeBS) &
                       (ds.TeNE>ds.IBS) &
                       (ds.TeNE>ds.TeBE) &
                       (ds.TeNE>ds.TrBE) &
                       (ds.TeNE>ds.TrIBE) &
                       (ds.TeNE>ds.TrBR) ),
                      3, biome)

    # Temperate deciduous forest
    biome = np.where((temperate_tree > total_tree * 0.8) &
                     (total_tree > 2.5) &
                     ( (ds.TeBS>ds.BNE) &
                       (ds.TeBS>ds.BNS) &
                       (ds.TeBS>ds.TeNE) &
                       (ds.TeBS>ds.IBS) &
                       (ds.TeBS>ds.TeBE) &
                       (ds.TeBS>ds.TrBE) &
                       (ds.TeBS>ds.TrIBE) &
                       (ds.TeBS>ds.TrBR) ),
                      4, biome)

    # Temperate broadleaved evergreen forest
    biome = np.where((temperate_tree > total_tree * 0.8) &
                     (total_tree > 2.5) &
                     ( ((ds.TeBE>ds.BNS) | (ds.IBS>ds.BNS) | (ds.TeBS>ds.BNS)) &
                       ((ds.TeBE>ds.TeNE) | (ds.IBS>ds.TeNE) | (ds.TeBS>ds.TeNE)) &
                       ((ds.TeBE>ds.TeBS) | (ds.IBS>ds.TeBS) | (ds.TeBS>ds.TeBS)) &
                       ((ds.TeBE>ds.BNE) | (ds.IBS>ds.TeBE) | (ds.TeBS>ds.BNE)) &
                       ((ds.TeBE>ds.TrBE) | (ds.IBS>ds.TrBE) | (ds.TeBS>ds.TrBE)) &
                       ((ds.TeBE>ds.TrIBE) | (ds.IBS>ds.TrIBE) | (ds.TeBS>ds.TrIBE)) &
                       ((ds.TeBE>ds.TrBR) | (ds.IBS>ds.TrBR)| (ds.TeBS>ds.TrBR)) ),
                      5, biome)

    # Temperate mixed forest
    biome = np.where((temperate_tree > total_tree * 0.8) &
                     (total_tree > 2.5),
                      6, biome)

    # Tropical seasonal forest
    biome = np.where((tropical_tree > total_tree * 0.5) &
                     (total_tree > 2.5) &
                     ((ds.TrBE < total_tree * 0.6) & (ds.TrBR < total_tree * 0.6)),
                      7, biome)

    # Tropical rain forest
    biome = np.where((ds.TrBE > total_tree * 0.6) &
                     (total_tree > 2.5),
                      8, biome)

    # Tropical deciduous forest
    biome = np.where((ds.TrBR > total_tree * 0.6) &
                     (total_tree > 2.5),
                      9, biome)

    # Moist savannas
    biome = np.where((total_tree > 0.5) &
                     (total_tree < 2.5) &
                     (ds.Total > 3),
                      10, biome)

    # Dry savannas
    biome = np.where((total_tree > 0.5) &
                     (total_tree < 2.5) &
                     (ds.Total <= 3),
                      11, biome)

    # Tall grassland
    biome = np.where((total_tree < 0.5) &
                     (grass > 3.0),
                      12, biome)

    # Dry grassland
    biome = np.where((total_tree < 0.2) &
                     (grass > 0.5),
                      13, biome)

    # Xeric woodland/shrub
    biome = np.where((total_tree > 0.5) &
                     (total_tree < 2.5) &
                     (grass < total_tree),
                      14, biome)

    # Arid shrubland/steppe
    biome = np.where((total_tree < 0.5) &
                      (ds.Total > 0.2),
                      15, biome)

    # Arctic/alpine tundra - Lat > 54 or sum GDD5 < 350
    #biome = np.where((total_tree < 0.5) &
    #                  (ds.Total > 0.2),
    #                  16, biome)

    # Desert
    biome = np.where(ds.Total < 0.2, 16, biome)

    #plt.imshow(biome)
    #plt.colorbar()
    #plt.show()
    #sys.exit()

    fig = plt.figure(figsize=(9,6))
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams['font.sans-serif'] = "Helvetica"

    ax = plt.axes(projection=ccrs.PlateCarree())

    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=0.5,
                      color='black', alpha=0.5, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlines = False
    gl.ylines = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    ax.coastlines(resolution='10m', linewidth=1.0, color='black')

    ax.add_feature(cartopy.feature.OCEAN)

    bounds = np.arange(16)
    bounds = np.append(bounds, bounds[-1]+1)
    cmap = plt.cm.viridis
    norm = colors.BoundaryNorm(bounds, cmap.N)
    #labels = ["RAF", "WSF", "DSF", "GRW", "SAW"]
    labels = ["Boreal decid. for.",\
              "Boreal ever. for.", \
              "Tem/bor. mixed for.", \
              "Tem. conif. for.", \
              "Tem. decid. for.", \
              "Tem. broad.. for.", \
              "Tem. mixed for.", \
              "Tro. seasonal for.", \
              "Tro. rain for.", \
              "Tro. decid for.", \
              "Moist savannas", \
              "Dry savannas", \
              "Tall grass", \
              "Dry grass", \
              "Xeric wood.", \
              "Arid shrub", \
              "Desert"]

    top, bottom = 90, -90
    left, right = -180, 180
    img = ax.imshow(biome, origin='lower', transform=ccrs.PlateCarree(),
                    interpolation='nearest', cmap=cmap, norm=norm,
                    extent=(left, right, bottom, top))
    cbar = plt.colorbar(img, cmap=cmap, norm=norm, boundaries=bounds, ticks=bounds,
                        orientation='vertical', shrink=0.7, pad=0.04)
    cbar.set_ticklabels(labels)
    #tick_locs = np.arange(16)
    #cbar.set_ticks(tick_locs)
    cbar.ax.set_title("Vegetation\ntypes", fontsize=8)

    #ax.set_ylabel("Latitude")
    #ax.set_xlabel("Longtiude")
    ax.text(-0.10, 0.55, 'Latitude', va='bottom', ha='center',
            rotation='vertical', rotation_mode='anchor',
            transform=ax.transAxes)
    ax.text(0.5, -0.1, 'Longitude', va='bottom', ha='center',
            rotation='horizontal', rotation_mode='anchor',
            transform=ax.transAxes)
    #
    ax.set_xlim(112, 154)
    ax.set_ylim(-44, -10)

    fig.savefig("Aus_biomes.png", dpi=150, bbox_inches='tight',
                pad_inches=0.1)




    #plt.imshow(biome[90:160,580:670])
    #plt.colorbar()
    #plt.show()


if __name__ == "__main__":

    fname = "LPJ-GUESS_lai_1901_2015.nc"

    ds = xr.open_dataset(fname)
    # Get final year
    ds = ds.sel(Time="2015-01-01")

    #plot_LAI(ds)
    plot_biomes(ds)
