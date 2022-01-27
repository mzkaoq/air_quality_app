import folium
import altair as alt
import pandas as pd


class DrawingMap:
    def __init__(self,mode,lista):
        self.mode = mode
        self.probe_list = lista
        pass
    def draw_map(self):
        map = folium.Map(location=[51.35, 19.25], zoom_start=5.5)
        for station in self.probe_list:
            #print(station.name, station.cord_x, station.cord_y, station.return_average())
            average24h = station.return_average()[self.mode]
            list_hours_data = station.return_list()[self.mode]
            list_hours_data = list(list_hours_data)
            print(list_hours_data[0])
            if list_hours_data[0] != []:
                source = pd.DataFrame(
                    {
                        'hours': list_hours_data[0],
                        'pm10': list_hours_data[1],
                        #'a': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
                        #'b': [28, 55, 43, 91, 81, 53, 19, 87, 52],
                    })
                #chart = alt.Chart(source).mark_bar().encode(x='hours', y='pm10[ug/m^3]')
                chart = alt.Chart(source).mark_bar().encode(x=alt.X('hours',sort=list_hours_data[0]), y='pm10').interactive()
                vis1 = chart.to_json()
            else:
                vis1 = None
            if average24h == 0.0:
                hue = "lightgray"
            elif average24h < 25:
                hue = "green"
            elif average24h < 50:
                hue = "lightgreen"
            elif average24h < 75:
                hue = "orange"
            elif average24h < 100:
                hue = "red"
            else:
                hue = "purple"
            if list_hours_data[0] != []:
                folium.Marker(
                    location=[station.cord_x, station.cord_y],
                    icon=folium.Icon(color=hue),
                    #popup= (station.name,"value=",station.return_average()[self.mode])
                    popup = folium.Popup(max_width=600).add_child(folium.VegaLite(data=vis1, width=600, height=200))
                ).add_to(map)
            else:
                folium.Marker(
                    location=[station.cord_x, station.cord_y],
                    icon=folium.Icon(color=hue),
                    popup= (station.name,"value=",station.return_average()[self.mode])
                ).add_to(map)
        return map._repr_html_()

    def draw_map2(self):
        map = folium.Map(location=[51.35, 19.25], zoom_start=5.5)
        for station in self.probe_list:
            # print(station.name, station.cord_x, station.cord_y, station.return_average())
            average24h = station.return_average()[self.mode]
            if average24h == 0.0:
                hue = "lightgray"
            elif average24h < 25:
                hue = "green"
            elif average24h < 50:
                hue = "lightgreen"
            elif average24h < 75:
                hue = "orange"
            elif average24h < 100:
                hue = "red"
            else:
                hue = "purple"
            folium.Marker(
                    location=[station.cord_x, station.cord_y],
                    icon=folium.Icon(color=hue),
                    popup=(station.name, "value=", station.return_average()[self.mode])
                ).add_to(map)
        return map._repr_html_()


