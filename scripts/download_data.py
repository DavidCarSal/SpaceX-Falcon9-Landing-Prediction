from pathlib import Path
import urllib.request, json, hashlib, datetime, shutil

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
BASE = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/'
SOURCES = {name: BASE + 'datasets/' + name for name in [
    'dataset_part_1.csv', 'dataset_part_2.csv', 'dataset_part_3.csv',
    'spacex_launch_geo.csv', 'spacex_launch_dash.csv', 'API_call_spacex_api.json']}
SOURCES['Spacex.csv'] = BASE + 'labs/module_2/data/Spacex.csv'


def main():
    snapshots = DATA / 'source'
    snapshots.mkdir(parents=True, exist_ok=True)
    manifest = []
    for name, url in SOURCES.items():
        content = urllib.request.urlopen(url, timeout=40).read()
        (snapshots / name).write_bytes(content)
        if name not in ['dataset_part_2.csv', 'dataset_part_3.csv'] or not (DATA / name).exists():
            shutil.copyfile(snapshots / name, DATA / name)
        manifest.append({'file': 'source/' + name, 'url': url,
                         'retrieved_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                         'sha256': hashlib.sha256(content).hexdigest(), 'bytes': len(content)})
        print(name, len(content), flush=True)
    (DATA / 'sources.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
