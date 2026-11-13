from pathlib import Path
import json
import math

# Recompute approximate straight-line distances from the preserved OSM geometry.
root = Path(__file__).resolve().parents[1]

lat,lon=28.562302,-80.577356
R=6371.0088

def hav(a,b):
 p1,p2=map(math.radians,[a[0],b[0]]);dp=p2-p1;dl=math.radians(b[1]-a[1]);return R*2*math.asin(math.sqrt(math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2))

def nearest(points):
 # Equirectangular projection for segment interpolation in this small local area.
 scale=math.cos(math.radians(lat));best=None
 for a,b in zip(points,points[1:]):
  ax=(a['lon']-lon)*scale;ay=a['lat']-lat;bx=(b['lon']-lon)*scale;by=b['lat']-lat;dx=bx-ax;dy=by-ay
  t=max(0,min(1,-(ax*dx+ay*dy)/(dx*dx+dy*dy))) if dx*dx+dy*dy else 0
  pt=(lat+ay+t*dy,lon+(ax+t*dx)/scale);km=hav((lat,lon),pt)
  if best is None or km<best[0]:best=(km,pt)
 return best
features=json.loads((root/'data/osm_proximity.json').read_text(encoding='utf-8'))['elements'];picked=[]
for label,predicate in [('Coastline',lambda t:t.get('natural')=='coastline'),('Railway',lambda t:t.get('railway')=='rail'),('Road',lambda t:'highway' in t),('Town/city centre',lambda t:t.get('place') in ['city','town'])]:
 candidates=[]
 for e in features:
  if not predicate(e.get('tags',{})):continue
  result=nearest(e['geometry']) if 'geometry' in e else (hav((lat,lon),(e['lat'],e['lon'])),(e['lat'],e['lon']))
  if result:candidates.append((result[0],result[1],e))
 km,pt,e=min(candidates,key=lambda x:x[0]);picked.append({'feature':label,'latitude':pt[0],'longitude':pt[1],'distance_km':km,'name':e.get('tags',{}).get('name',e.get('tags',{}).get('ref','Unnamed mapped feature')),'osm_type':e['type'],'osm_id':e['id'],'tags':e.get('tags',{}),'source_url':f'https://www.openstreetmap.org/{e["type"]}/{e["id"]}'})
proximity={'launch_site':'CCAFS SLC-40','latitude':lat,'longitude':lon,'method':'Nearest point on returned way segments using local projection, then spherical great-circle distance (R=6371.0088 km). Town uses mapped centre node. Not a travel distance. Mapped roads/rail/coastlines searched within 15 km, towns/cities within 50 km.','features':picked}
(root/'reports/proximity_measurements.json').write_text(json.dumps(proximity,indent=2)+'\n')

print(json.dumps(proximity, indent=2))
