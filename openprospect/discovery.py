from __future__ import annotations
import json, urllib.parse, urllib.request

# OpenStreetMap tags are intentionally broad. Results depend on local mapping coverage.
PRESETS={
 "restaurant":'node["amenity"="restaurant"];way["amenity"="restaurant"];relation["amenity"="restaurant"];',
 "cafe":'node["amenity"="cafe"];way["amenity"="cafe"];relation["amenity"="cafe"];',
 "hotel":'node["tourism"="hotel"];way["tourism"="hotel"];relation["tourism"="hotel"];',
 "shop":'node["shop"];way["shop"];relation["shop"];',
 "beauty":'node["shop"="beauty"];way["shop"="beauty"];node["amenity"="beauty"];way["amenity"="beauty"];',
 "clinic":'node["amenity"="clinic"];way["amenity"="clinic"];node["healthcare"];way["healthcare"];',
 "dentist":'node["amenity"="dentist"];way["amenity"="dentist"];',
 "school":'node["amenity"="school"];way["amenity"="school"];node["amenity"="college"];way["amenity"="college"];',
 "gym":'node["leisure"="fitness_centre"];way["leisure"="fitness_centre"];',
 "supermarket":'node["shop"="supermarket"];way["shop"="supermarket"];',
 "any business":'node["office"];way["office"];node["shop"];way["shop"];node["amenity"~"restaurant|cafe|bank|clinic|dentist|school|hospital"];way["amenity"~"restaurant|cafe|bank|clinic|dentist|school|hospital"];'
}

def discover_osm(city:str,category:str="any business",limit:int=50):
    if not city.strip():raise ValueError("Enter a city or place.")
    key=category.lower().strip()
    selector=PRESETS.get(key,PRESETS["any business"])
    # Nominatim resolves the requested city, then Overpass searches a 10 km radius.
    q=urllib.parse.urlencode({"q":city,"format":"json","limit":1})
    req=urllib.request.Request("https://nominatim.openstreetmap.org/search?"+q,headers={"User-Agent":"OpenProspect/0.1 (open-source local business research)"})
    with urllib.request.urlopen(req,timeout=30) as r: places=json.loads(r.read())
    if not places:raise RuntimeError("Location not found by OpenStreetMap. Try a more specific city name.")
    lat=float(places[0]["lat"]);lon=float(places[0]["lon"])
    overpass=f'[out:json][timeout:45];( {selector} )(around:10000,{lat},{lon});out center tags;'
    data=urllib.parse.urlencode({"data":overpass}).encode()
    req=urllib.request.Request("https://overpass-api.de/api/interpreter",data=data,headers={"User-Agent":"OpenProspect/0.1"})
    with urllib.request.urlopen(req,timeout=60) as r: payload=json.loads(r.read())
    results=[]
    for el in payload.get("elements",[]):
        tags=el.get("tags",{});name=tags.get("name")
        if not name:continue
        lat2=el.get("lat",el.get("center",{}).get("lat"));lon2=el.get("lon",el.get("center",{}).get("lon"))
        website=tags.get("website") or tags.get("contact:website") or ""
        phone=tags.get("phone") or tags.get("contact:phone") or ""
        address=", ".join(x for x in [tags.get("addr:housenumber"),tags.get("addr:street"),tags.get("addr:city")] if x)
        results.append({"name":name,"website":website,"phone":phone,"category":tags.get("amenity") or tags.get("shop") or tags.get("tourism") or tags.get("office") or category,"address":address,"lat":lat2,"lon":lon2,"source_url":f"https://www.openstreetmap.org/{el['type']}/{el['id']}"})
    return results[:max(1,min(int(limit),200))]
