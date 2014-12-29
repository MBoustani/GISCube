from pydap.client import open_url
from netcdftime import utime
import numpy as np

from giscube.config import MEDIA_ROOT, MEDIA_URL

def load(url, variable, name=''):
    d = open_url(url)
    dataset = d[variable]

    dataset_dimensions = dataset.dimensions
    time = dataset_dimensions[0]
    lat = dataset_dimensions[1]
    lon = dataset_dimensions[2]

    times = np.array(_convert_times_to_datetime(d[time]))

    lats = np.array(dataset[lat][:])
    lons = np.array(dataset[lon][:])
    values = np.array(dataset[:])
    text_file = create_text(lats, lons, times, values, variable, name=variable)

    return text_file


def _convert_times_to_datetime(time):
    units = time.units
    parsed_time = utime(units)

    return [parsed_time.num2date(x) for x in time[:]]


def create_text(lats, lons, times, values, variable, name):
    with open('{0}{1}.txt'.format(MEDIA_ROOT + MEDIA_URL, name), 'w') as text_file:
        text_file.write('lats: {0}'.format(lats))
        text_file.write('lons: {0}'.format(lons))
        text_file.write('times: {0}'.format(times))
        text_file.write('values: {0}'.format(values))

    return text_file