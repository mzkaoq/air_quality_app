import requests
import json
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask.views import MethodView
from datetime import datetime
from data import  ProbeManager, ConreteProbe
import folium
import datetime
from drawings import DrawingMap

app = Flask(__name__)
app.secret_key = "pk"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test2.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    cord_x = db.Column(db.Integer, nullable=False)
    cord_y = db.Column(db.Integer, nullable=False)
    city_code = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    voivodeship = db.Column(db.String(50), nullable=False)
    stationprobes = db.relationship('StationProbe', backref='station', lazy=True)


class StationProbe(db.Model):
    id_station = db.Column(db.Integer, db.ForeignKey('station.id'))
    id_probe = db.Column(db.Integer, primary_key=True)
    probes = db.relationship('Probe', backref='stationprobe', lazy=True)


class Probe(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # rok miesiac dzien godzina id_probe
    id_probe = db.Column(db.Integer, db.ForeignKey(StationProbe.id_probe), nullable=False)
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))


if not path.exists("test2.db"):
    db.create_all()

db.create_all()


class Root(MethodView):
    def get(self):
        return render_template('index.html')

    def post(self):
        if request.form["updateBtn"] == 'submit':
            response = requests.get('https://api.gios.gov.pl/pjp-api/rest/station/findAll').text
            converted_response = json.loads(response)
            # print(converted_response)
            for stations in converted_response:
                new_station = Station(id=stations["id"], name=stations["stationName"], cord_x=stations["gegrLat"],
                                      cord_y=stations["gegrLon"], city_code=stations["city"]["id"],
                                      city=stations["city"]["name"],
                                      voivodeship=stations["city"]["commune"]["provinceName"])
                if Station.query.filter_by(id=stations["id"]).first():
                    pass
                else:
                    db.session.add(new_station)
                    db.session.commit()
            for station_id in Station.query.all():
                number = station_id.id
                number = str(number)
                link = "https://api.gios.gov.pl/pjp-api/rest/station/sensors/" + number
                r = requests.get(link).text
                converted_link = json.loads(r)
                if converted_link == []:
                    # ten sam numer do bazy get_data(number)
                    new_stationprobe = StationProbe(id_station=int(number), id_probe=int(number))
                    if StationProbe.query.filter_by(id_station=int(number)).first():
                        pass
                    else:
                        db.session.add(new_stationprobe)
                        db.session.commit()
                else:
                    for elem in converted_link:
                        if elem["param"]["paramFormula"] == "PM10":
                            number2 = str(elem["id"])
                            new_stationprobe = StationProbe(id_station=int(number), id_probe=int(number2))
                            if StationProbe.query.filter_by(id_station=int(number)).first():
                                pass
                            else:
                                db.session.add(new_stationprobe)
                                db.session.commit()
                        else:
                            pass

            flash("Stations has been updated", "alert")
            return render_template('index.html')
        elif request.form["updateBtn"] == 'submit2':
            for probe in StationProbe.query.all():
                number = str(probe.id_probe)
                response2 = requests.get('https://api.gios.gov.pl/pjp-api/rest/data/getData/' + number).text
                # print(response2)
                if response2 != "":
                    converted_response2 = json.loads(response2)
                    values2 = []
                    values = []
                    if converted_response2["key"] == "PM10":
                        values = converted_response2["values"]
                    for elem in values:
                        if elem["value"] != None:
                            values2.append(elem)
                    if values2 != []:
                        for elem in values2:
                            date = elem["date"].split("-")
                            hours = date[2].split(" ")
                            date[2] = hours[0]
                            hours = (hours[1].split(":"))[0]
                            date.append(hours)
                            code = date[0] + date[1] + date[2] + date[3] + str(number)
                            for i in range(4):
                                date[i] = int(date[i])
                            x = datetime.datetime(date[0], date[1], date[2], date[3])
                            new_probe = Probe(id=int(code), id_probe=number, value=elem["value"], date=x)
                            if Probe.query.filter_by(id=int(code)).first():
                                pass
                            else:
                                db.session.add(new_probe)
                                db.session.commit()

                    else:
                        print("nothing there")
                else:
                    print("nothing there")
            create_points()
            flash("PM10 data has been updated 2", "alert")
            return render_template('index.html')
        else:
            pass


app.add_url_rule('/', view_func=Root.as_view("root"))


class Table(MethodView):
    def get(self):
        station = Station.query
        return render_template('table.html', station=station);

    def post(self):
        station = Station.query
        return render_template('table.html', station=station);


app.add_url_rule('/table/', view_func=Table.as_view("table"))


class ConcreteStation(MethodView):
    def get(self, id):
        concrete_probe = probe_manager.return_concrete_probe(id)
        start_coords = (concrete_probe.cord_x, concrete_probe.cord_y)
        folium_map = folium.Map(location=start_coords, zoom_start=10)
        folium.Marker(
            location=[concrete_probe.cord_x, concrete_probe.cord_y],
            icon=folium.Icon(color="blue")
        ).add_to(folium_map)
        folium_map.save('templates/map.html')
        all_data = concrete_probe.return_all_data()
        all_data2 = []
        for key, value in all_data.items():
            key2 = str(key)
            new_key = datetime.datetime(int(key2[0:4]), int(key2[4:6]), int(key2[6:8]), int(key2[8:10]))
            all_data2.append([new_key, value])
        return render_template('concrete_station.html', station_name=concrete_probe.name,
                               average24h=concrete_probe.average_24h, average72h=concrete_probe.average_72h,
                               station=all_data2);

    def post(self, id):
        concrete_probe = probe_manager.return_concrete_probe(id)
        start_coords = (concrete_probe.cord_x, concrete_probe.cord_y)
        folium_map = folium.Map(location=start_coords, zoom_start=10)
        folium.Marker(
            location=[concrete_probe.cord_x, concrete_probe.cord_y],
            icon=folium.Icon(color="blue")
        ).add_to(folium_map)
        folium_map.save('templates/map.html')
        all_data = concrete_probe.return_all_data()
        all_data2 = []
        for key, value in all_data.items():
            key2 = str(key)
            new_key = datetime.datetime(int(key2[0:4]), int(key2[4:6]), int(key2[6:8]), int(key2[8:10]))
            all_data2.append([new_key, value])
        return render_template('concrete_station.html', station_name=concrete_probe.name,
                               average24h=concrete_probe.average_24h, average72h=concrete_probe.average_72h,
                               station=all_data2);


app.add_url_rule('/table/<id>/', view_func=ConcreteStation.as_view("concretestation"))


class Table2(MethodView):
    def get(self):
        probe = Probe.query.order_by(Probe.id_probe).all()
        return render_template('table2.html', probe=probe);

    def post(self):
        probe = Probe.query.order_by(Probe.id_probe).all()
        return render_template('table2.html', probe=probe);


app.add_url_rule('/table2/', view_func=Table2.as_view("table2"))


class Map24(MethodView):
    def get(self):
        draw = DrawingMap(0, probe_manager.return_list())
        """
        for station in probe_manager.return_list():
            print(station.name, station.cord_x, station.cord_y, station.return_average())
        """
        return draw.draw_map()

    def post(self):
        draw = DrawingMap(0, probe_manager.return_list())
        return draw.draw_map()
        # return render_template('map.html',czujnik = map._repr_html_());


app.add_url_rule('/map24/', view_func=Map24.as_view("map24"))


class Map72(MethodView):
    def get(self):
        draw = DrawingMap(1, probe_manager.return_list())
        return draw.draw_map2()

    def post(self):
        draw = DrawingMap(1, probe_manager.return_list())
        return draw.draw_map2()
        # return render_template('map.html',czujnik = map._repr_html_());


app.add_url_rule('/map72/', view_func=Map72.as_view("map72"))


data_selected = db.session.query(Station, Probe).select_from(Station).join(StationProbe).join(Probe) \
    .filter(Station.id == StationProbe.id_station).filter(StationProbe.id_probe == Probe.id_probe).filter(
    Probe.id_probe == 92)
data_selected = data_selected.all()

"""
for elem in data_selected:
    print(elem.Station.name,elem.Probe.id,elem.Station.cord_x,elem.Station.cord_y,elem.Probe.value,elem.Probe.date)
"""

probe_manager = ProbeManager()
def create_points():
    probe_manager.erase_data()
    all_stations = Station.query.all()
    for station in all_stations:
        probe_manager.add_probe(ConreteProbe(station.id, station.name, station.cord_x, station.cord_y, station.voivodeship))
    for station in probe_manager.return_list():
        st_id = station.id
        data_selected = db.session.query(Station, Probe).select_from(Station).join(StationProbe).join(Probe) \
            .filter(Station.id == StationProbe.id_station).filter(StationProbe.id_probe == Probe.id_probe).filter(
            Station.id == st_id)
        data_selected = data_selected.all()
        # print(data_selected)
        for elem in data_selected:
            station.add_new_data(elem.Probe.id, elem.Probe.value)
        station.update_averages()

create_points()

if __name__ == "__main__":
    app.run(debug=True)
