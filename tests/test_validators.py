import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SkillValidationTest(unittest.TestCase):
    def test_skill(self):
        self.assertEqual(load('validate_skill').validate(ROOT), [])

    def test_project_template(self):
        manifest = json.loads((ROOT / 'assets/project-template.json').read_text(encoding='utf8'))
        self.assertEqual(load('validate_project').validate(manifest), [])

    def test_image_branch_template_has_no_a_gates(self):
        manifest = json.loads((ROOT / 'assets/image-branch-template.json').read_text(encoding='utf8'))
        self.assertEqual(load('validate_project').validate(manifest), [])

    def test_missing_route_selection_is_flagged(self):
        manifest = json.loads((ROOT / 'assets/project-template.json').read_text(encoding='utf8'))
        manifest['gates']['branch_selected'] = False
        self.assertTrue(any('A/B selection' in x for x in load('validate_project').validate(manifest)))

    def test_image_branch_cannot_enter_a_stages(self):
        manifest = json.loads((ROOT / 'assets/image-branch-template.json').read_text(encoding='utf8'))
        manifest['stage'] = 'build'
        self.assertTrue(any('B cannot enter A' in x for x in load('validate_project').validate(manifest)))

    def test_image_branch_delivered_requires_real_images_and_qa(self):
        manifest = json.loads((ROOT / 'assets/image-branch-template.json').read_text(encoding='utf8'))
        manifest['stage'] = 'image_delivered'
        self.assertTrue(load('validate_project').validate(manifest))
        for slide in manifest['slides']:
            slide['rendered_image'] = f"images/{slide['id']}.png"
            slide['qa']['static'] = 'pass'
        self.assertEqual(load('validate_project').validate(manifest), [])

    def test_a_animation_requirement_mismatch(self):
        manifest = json.loads((ROOT / 'assets/project-template.json').read_text(encoding='utf8'))
        manifest['brief']['animation_requested'] = False
        self.assertTrue(any('animation_requested' in x for x in load('validate_project').validate(manifest)))

    def test_b_animation_requirement_mismatch(self):
        manifest = json.loads((ROOT / 'assets/image-branch-template.json').read_text(encoding='utf8'))
        manifest['brief']['animation_requested'] = True
        self.assertTrue(any('animation_requested' in x for x in load('validate_project').validate(manifest)))

    def test_fake_approval_is_flagged(self):
        manifest = json.loads((ROOT / 'assets/project-template.json').read_text(encoding='utf8'))
        manifest['stage'] = 'approved'
        self.assertTrue(load('validate_project').validate(manifest))

    def test_faux_editability_is_flagged(self):
        manifest = json.loads((ROOT / 'assets/project-template.json').read_text(encoding='utf8'))
        manifest['slides'][0]['elements'][0]['kind'] = 'flattened_page'
        self.assertTrue(any('flattened_page' in x for x in load('validate_project').validate(manifest)))


if __name__ == '__main__':
    unittest.main()
