#!/usr/bin/env python3
"""Static self-consistency validator for visual-ppt-workflow project.json.

Gate markers are user/agent claims; this script cannot prove approval or visual quality.
"""
import argparse
import json
import sys
from pathlib import Path

STAGES_A = ('brief', 'styles', 'selected', 'pilot', 'artwork', 'approved', 'build', 'qa', 'delivered')
STAGES_B = ('image_generate', 'image_qa', 'image_delivered')
STAGES = ('route',) + STAGES_A + STAGES_B
MODES = ('editable', 'image', 'hybrid', 'review', 'pdf-only')
KINDS = ('background', 'native_text', 'native_shape', 'native_chart', 'native_table', 'independent_image', 'flattened_page')
QA_VALUES = ('not_tested', 'pass', 'fail', 'not_applicable', 'blocked')


def validate(project):
    errors = []
    for name in ('schema_version', 'project_id', 'workflow_branch', 'mode', 'stage', 'brief', 'gates', 'slides', 'artifacts'):
        if name not in project:
            errors.append(f'missing field: {name}')
    if errors:
        return errors
    if project['mode'] not in MODES:
        errors.append('unsupported mode')
    stage = project['stage']
    if stage not in STAGES:
        errors.append('unsupported stage')
    slides = project['slides']
    if not isinstance(slides, list) or not slides:
        errors.append('slides must be a nonempty array')
        return errors
    gates = project['gates']
    branch = project['workflow_branch']
    if branch not in ('A', 'B', None):
        errors.append('workflow_branch must be A or B (or null only at route stage)')
    if stage == 'route':
        if gates.get('branch_selected'):
            errors.append('route stage cannot claim branch_selected')
    elif branch not in ('A', 'B') or not gates.get('branch_selected'):
        errors.append('generation stages require explicit A/B selection and gates.branch_selected')
    if branch == 'A':
        if stage in STAGES_B:
            errors.append('A cannot enter image-only stages')
        if project['brief'].get('animation_requested') is not True:
            errors.append('A must have animation_requested=true')
        if stage in STAGES_A[2:] and not gates.get('style_selected') and project['mode'] not in ('review',):
            errors.append('A selected+ stage requires gates.style_selected, unless review')
        if stage in STAGES_A[5:] and not gates.get('artwork_approved') and project['mode'] not in ('review',):
            errors.append('A approved+ stage requires gates.artwork_approved, unless review')
        if gates.get('style_selected') and not project.get('selected_style_id'):
            errors.append('selected style gate requires selected_style_id')
        if gates.get('style_selected') and len(project.get('styleboards', [])) < 8 and not project.get('preview_waiver'):
            errors.append('style_selected requires 8 styleboards or explicit preview_waiver')
        if stage in STAGES_A[5:] and not all(s.get('reference_image') for s in slides) and project['mode'] not in ('review',):
            errors.append('A approved+ stage requires reference_image for every slide')
    if branch == 'B':
        if stage not in STAGES_B and stage != 'route':
            errors.append('B cannot enter A workflow stages')
        if project['mode'] != 'image':
            errors.append('B requires mode=image')
        if project['brief'].get('animation_requested') is not False:
            errors.append('B must have animation_requested=false')
        if gates.get('style_selected') or gates.get('artwork_approved'):
            errors.append('B must not claim A-only style/artwork gates')
        if stage == 'image_delivered':
            for item in slides:
                if not item.get('rendered_image'):
                    errors.append(f'B image_delivered requires rendered_image for {item.get("id")}')
                if item.get('qa', {}).get('static') != 'pass':
                    errors.append(f'B image_delivered requires static QA pass for {item.get("id")}')
    ids = set()
    for idx, slide in enumerate(slides, 1):
        name = f'slides[{idx}]'
        sid = slide.get('id')
        if not sid:
            errors.append(f'{name} id required')
        elif sid in ids:
            errors.append(f'duplicate slide id {sid}')
        ids.add(sid)
        eids = set()
        for element in slide.get('elements', []):
            eid = element.get('id')
            if not eid or eid in eids:
                errors.append(f'{name} element has missing/duplicate id')
            eids.add(eid)
            kind = element.get('kind')
            if kind not in KINDS:
                errors.append(f'{name}: invalid element kind {kind}')
            bbox = element.get('bbox')
            if not (isinstance(bbox, list) and len(bbox) == 4 and all(isinstance(v, (int, float)) for v in bbox) and bbox[2] > 0 and bbox[3] > 0):
                errors.append(f'{name} element {eid}: bbox must be [x,y,w,h], positive size')
            if branch == 'B' and (kind != 'flattened_page' or element.get('editable') is True):
                errors.append(f'{name} element {eid}: B only permits non-editable flattened_page')
            if kind == 'flattened_page' and project['mode'] == 'editable':
                errors.append(f'{name} element {eid}: flattened_page prohibited in editable mode without mode change')
        for dim, value in slide.get('qa', {}).items():
            if value not in QA_VALUES:
                errors.append(f'{name} qa.{dim} unknown: {value}')
        if stage in ('delivered', 'image_delivered') and any(x == 'fail' for x in slide.get('qa', {}).values()):
            errors.append(f'{name}: stage delivered but QA contains fail')
    return errors


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('manifest', help='path to project.json')
    args = p.parse_args()
    try:
        project = json.loads(Path(args.manifest).read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1
    errors = validate(project)
    if errors:
        for issue in errors:
            print('FAIL:', issue, file=sys.stderr)
        return 1
    print(f'PASS: project manifest with {len(project["slides"])} slides, stage={project["stage"]}, mode={project["mode"]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
