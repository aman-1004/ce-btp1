import os
import imdlib as imd
from datetime import datetime
from scipy.interpolate import RegularGridInterpolator
import numpy as np


class ImdRain:
    start: int = None
    end: int = None
    grid_dir: str = None
    variable: str = None
    data = None
    rgi = None

    def __init__(self, start: int, end: int, variable: str = "rain", grid_dir: str = "./grid" , force_download = False):
        self.variable = variable
        self.start = start
        self.end = end
        self.grid_dir = grid_dir
        var_grid_dir = os.path.join(self.grid_dir, self.variable)
        needs_download = False
        for year in range(start, end+1):
            if not os.path.exists(os.path.join(var_grid_dir, f"{year}.grd")): needs_download = True

        if needs_download or force_download:
            imd.get_data(self.variable, start, end, fn_format='yearwise', file_dir=grid_dir)

        data = imd.open_data(self.variable, start, end, 'yearwise', grid_dir).get_xarray()
        self.data = data.where(data['rain'] != -999.)
        dates = np.arange(0, len(data['time']))
        self.rgi = RegularGridInterpolator((dates, data['lat'].data,
                                            data['lon'].data), data['rain'])


    @staticmethod
    def degree_to_decmial(coordinates_in_degree: str):
        nos = list(map(float,
                       coordinates_in_degree
                       .replace("°", " ")
                       .replace("'", " ")
                       .replace('"', " ")
                       .split()[:3]))

        return nos[0] + nos[1]/60 + nos[2]/3600

    # date should be YYYY-MM-DD format
    def get_date_index(self, year, month, day):
        year = int(year)
        month = int(month)
        day = int(day)
        return (datetime(year, month, day) - datetime(self.start, 1, 1)).days

    def get_ind(self, time: str, lat: float, lon: float):
        data = self.data
        lat_diff = data['lat'][1] - data['lat'][0]
        lon_diff = data['lon'][1] - data['lon'][0]
        indx = int((lat - data['lat'][0]) / lat_diff)
        indy = int((lon - data['lon'][0]) / lon_diff)
        date_ind = self.get_date_index(*time.split('-'))
        return (date_ind, indx, indy)

    def get_data2(self, time: str, lat: float, lon: float):
        data = self.data
        lat_diff = data['lat'][1] - data['lat'][0]
        lon_diff = data['lon'][1] - data['lon'][0]
        indx = int((lat - data['lat'][0]) / lat_diff)
        indy = int((lon - data['lon'][0]) / lon_diff)
        assert len(time.split('-')) == 3
        date_ind = self.get_date_index(*time.split('-'))
        rain_dat = data['rain'][date_ind]
        return rain_dat[indx][indy]

    def get_data(self, time: str, lat: float, lon: float):
        date_ind = self.get_date_index(*time.split('-'))
        return self.rgi(np.array([date_ind, lat, lon]))

    def get_n_days_data(self, no_of_days: int, time: str, lat: float, lon: float):
        date_ind = self.get_date_index(*time.split('-'))
        res = []
        while no_of_days and date_ind:
            tn = self.rgi(np.array([date_ind, lat, lon]))[0]
            res.append(tn)
            date_ind -= 1
            no_of_days -= 1
        res.reverse()
        return res


def main():
    a = ImdRain(2019, 2022)
    print(
        a.get_data('2019-06-12', 32.47, 76.19)
    )


if __name__ == "__main__":
    main()
