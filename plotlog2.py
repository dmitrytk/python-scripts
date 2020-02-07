'''
Create .rb9 file from layers table.
Формат входного файла plotlog.xlsx:
Sheet 1: 'LAYERS'
WELL	ZKA	ZPA
1W	-839.3	-840.5
1W	-840.5	-841.9

Sheet 2: 'WELLS'
WELL	ALT	X	Y
18P	95.8	3543229	726515
1W	107.7	3543302	722886

Sheet 3: 'ZONES'
WELL	ZONE	ZKA	ZPA
18P	УВАТСКАЯ	-844.2	-1583.6
23R	УВАТСКАЯ	-846.8	-1579.2
'''

import os
import sys
import time
import pandas as pd
import time


class Well:
    def __init__(self, name, alt, md, x, y):
        self.name = name
        self.alt = alt
        self.x = x
        self.y = y
        self.md = md
        self.zone_top = []
        self.zone_bot = []
        self.zk = []
        self.zp = []

    def __str__(self):
        return f'"{self.name}" {self.alt} {self.x} {self.y} {self.md}'


def write_file(file_name, content):
    with open(file_name, 'w') as file:
        file.write(content)


def main():
    input_file = "plotlog.xlsx"
    output_rb1 = "_.rb1"
    output_rb3 = "_.rb3"
    output_rb9 = "_.rb9"

    # LOAD EXCEL FILE
    df_layers = pd.read_excel(input_file, sheet_name='LAYERS')
    df_wells = pd.read_excel(input_file, sheet_name='WELLS')
    df_zones = pd.read_excel(input_file, sheet_name='ZONES')


    # LOAD WELLS
    well_names = list(dict.fromkeys(df_wells.WELL).keys())
    wells = []

    for index, row in df_wells.iterrows():
        well = Well(row['WELL'], row['ALT'], row['MD'], round(row['X']/1000,3), round(row['Y']/1000,3))
        wells.append(well)


    # LOAD ZONES
    zone_names = list(dict.fromkeys(df_zones.ZONE).keys())
    zone_names.append(zone_names[-1] + '_bot')


    for well in wells:
        df_temp_well = df_zones[df_zones['WELL'] == well.name]
        if df_temp_well.empty:
            input(f'ERROR! well {well.name} not in zones list.')
            sys.exit()
        else:
            well.zone_top += [-1*i+well.alt for i in df_temp_well.ZKA]
            well.zone_bot += [-1*i+well.alt for i in df_temp_well.ZPA]


    # LOAD LAYERS
    for well in wells:
        df_temp_well = df_layers[df_layers['WELL'] == well.name]
        if df_temp_well.empty:
            input(f'ERROR! well {well.name} not in zones list.')
            sys.exit()
        else:
            well.zk += [-1*i+well.alt for i in df_temp_well.ZKA]
            well.zp += [-1*i+well.alt for i in df_temp_well.ZPA]


    # WRITE FILES
    # RB1
    rb1 = f'РАЗРЕЗ \n{len(well_names)} \n{len(zone_names)} \n'
    for zone in zone_names:
        rb1 += f' {zone} \n'

    write_file(output_rb1, rb1)


    # RB3
    rb3 = ''
    for well in wells:
        rb3 += str(well) + ' \n'
        for zone_top in well.zone_top:
            rb3 += str(zone_top) + ' \n'
        rb3 += str(well.zone_bot[-1]) + ' \n'

    write_file(output_rb3, rb3)


    # RB9
    rb9 = ''
    for well in wells:
        rb9 += f'"{well.name}" \n {well.zk[0]} {well.zp[-1]} 0.0 {len(well.zk)} \n'
        for index, layer in enumerate(well.zk):
            rb9 += f'{layer} {round((well.zp[index] - layer),2)} 0.7 \n'
    write_file(output_rb9, rb9)


if __name__ =='__main__':
    try:
        main()
        print('Done!')
        time.sleep(2)
    except Exception as e:
        print(e)
        input("Error! Press enter to continue")