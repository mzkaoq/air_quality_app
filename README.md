# air_quality_app

I created a simple web application using Python + Flask + SQLAlchemy, 
Using REST API my app pulls the data in JSON from Polish Chief Inspectorate Of Environmental Protection 
https://powietrze.gios.gov.pl/pjp/content/api?lang=pl

updating data is not automated and i have to do manually 

![menu](https://user-images.githubusercontent.com/72728316/151355313-6ebfc581-b650-463c-9a26-4fbd7936f030.PNG)

data can be listed, app can also generate map using folium module, 
to create charts i used altair and pandas modules

![lista](https://user-images.githubusercontent.com/72728316/151355371-61214713-e55c-48e6-a3e0-80eb2d333e7b.PNG)
![probes](https://user-images.githubusercontent.com/72728316/151355377-80467ee5-4266-448d-b818-2dcdec0f8f87.PNG)

we can see information about concrete station (location on the map) and its data listed below

![concrete_probe](https://user-images.githubusercontent.com/72728316/151355389-3408c888-ba7e-4435-ba81-0f47aa937931.PNG)

based on the average pollution of the pm10 from e.g. the last day, 
the pin on the map has a different color,
- gray are the points that do not collect data about pm10
- dark green means that the air quality, e.g. from the last 24 hours, is perfect

![map](https://user-images.githubusercontent.com/72728316/151355405-c5330131-b606-4b9e-965f-f584f372530d.PNG)
![chart](https://user-images.githubusercontent.com/72728316/151355412-e9317fff-1e6b-4505-a9bb-34b5a4ba71e8.PNG)

db model

![db_model](https://user-images.githubusercontent.com/72728316/151355213-bc59df38-6f55-4589-b6bd-ea8006b5bb16.PNG)


