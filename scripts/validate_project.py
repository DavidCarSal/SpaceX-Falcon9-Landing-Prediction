from pathlib import Path
import hashlib, json, sys
import zipfile
import xml.etree.ElementTree as ET
import nbformat
import pandas as pd
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    sources = json.loads((ROOT / 'data/sources.json').read_text())
    for entry in sources:
        content = (ROOT / 'data' / entry['file']).read_bytes()
        assert hashlib.sha256(content).hexdigest() == entry['sha256'], entry['file']
    notebooks = sorted((ROOT / 'notebooks').glob('*.ipynb'))
    assert len(notebooks) == 7
    for path in notebooks:
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        if not path.name.startswith('01_'):
            record = json.loads((ROOT / 'reports' / (path.stem + '_execution.json')).read_text())
            assert record['status'] == 'passed', path.name
            code = [cell for cell in notebook.cells if cell.cell_type == 'code']
            assert all(cell.execution_count is not None for cell in code), path.name
            assert not any(out.output_type == 'error' for cell in code for out in cell.outputs), path.name
    df = pd.read_csv(ROOT / 'data/dataset_part_2.csv')
    expected = df['Outcome'].str.startswith('True ').astype(int)
    assert (df['Class'] == expected).all()
    assert set(df['Class']) == {0, 1}
    assert not df['PayloadMass'].isna().any()
    X = pd.read_csv(ROOT / 'data/dataset_part_3.csv')
    assert len(X) == len(df) and not X.isna().any().any()
    scores = pd.read_csv(ROOT / 'reports/model_scores.csv')
    assert len(scores) == 4
    assert scores['Validation accuracy'].between(0, 1).all()
    assert scores['Test accuracy'].between(0, 1).all()
    osm = (ROOT / 'data/osm_proximity.json').read_bytes()
    provenance = json.loads((ROOT / 'data/osm_provenance.json').read_text())
    assert hashlib.sha256(osm).hexdigest() == provenance['sha256']
    measurements = json.loads((ROOT / 'reports/proximity_measurements.json').read_text())
    assert len(measurements['features']) == 4
    source_ids = {item['id'] for item in json.loads(osm)['elements']}
    assert all(item['osm_id'] in source_ids and item['distance_km'] >= 0
               for item in measurements['features'])
    presentation = ROOT / 'presentation/Data Science Capstone Project Report.pptx'
    with zipfile.ZipFile(presentation) as package:
        slides = [name for name in package.namelist()
                  if name.startswith('ppt/slides/slide') and name.endswith('.xml')]
        assert len(slides) == 40
        core = ET.fromstring(package.read('docProps/core.xml'))
        assert core.find('{http://purl.org/dc/elements/1.1/}creator').text == 'David Carro Salinas'
    pdf = PdfReader(ROOT / 'presentation/Data Science Capstone Project Report.pdf')
    assert len(pdf.pages) == 40
    assert pdf.metadata.author == 'David Carro Salinas'
    text = '\n'.join(page.extract_text() or '' for page in pdf.pages)
    assert 'RUN REQUIRED' not in text and '[ADD' not in text and 'ADD YOUR' not in text
    assert 'Executive summary' in text and 'Conclusions' in text
    assert 'confusion matrix' in text and 'Dash results' in text
    links = [annotation.get_object().get('/A', {}).get('/URI')
             for page in pdf.pages for annotation in page.get('/Annots', [])]
    assert 'https://github.com/DavidCarSal/SpaceX-Falcon9-Landing-Prediction' in links
    import app
    client = app.app.server.test_client()
    assert client.get('/').status_code == 200
    assert client.get('/_dash-layout').status_code == 200
    assert client.get('/_dash-dependencies').status_code == 200
    for site in ['ALL', *app.df['Launch Site'].unique()]:
        for bounds in [[0, 10000], [2000, 5000], [9900, 10000]]:
            rows = app.filtered(site, bounds)
            pie, scatter = app.figures(site, bounds)
            assert sum(len(trace.x) for trace in scatter.data) == len(rows)
            if site != 'ALL':
                assert (rows['Launch Site'] == site).all()
            total = sum(pie.data[0].values) if len(pie.data) else 0
            assert total == (rows['class'].sum() if site == 'ALL' else len(rows))
    # Verify a real Dash callback request, in addition to direct function checks.
    callback = next(iter(app.app.callback_map))
    response = client.post('/_dash-update-component', json={
        'output': callback,
        'outputs': [{'id': 'pie', 'property': 'figure'}, {'id': 'scatter', 'property': 'figure'}],
        'inputs': [{'id': 'site', 'property': 'value', 'value': 'ALL'},
                   {'id': 'payload', 'property': 'value', 'value': [0, 10000]}],
        'state': [], 'changedPropIds': ['site.value']})
    assert response.status_code == 200
    assert {'pie', 'scatter'} <= set(response.json['response'])
    print('PASS: source hashes, seven notebook schemas, six complete executions, labels, feature data, four model scores, dashboard filters and HTTP callback, OSM provenance, 40-slide PPTX and PDF, author and repository link.')


if __name__ == '__main__':
    main()
