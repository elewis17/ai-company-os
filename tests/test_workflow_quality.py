import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

os.environ.setdefault('OPENAI_API_KEY', 'test-placeholder-no-network')
from runtime.engine import run_workflow as engine
from runtime.agents.run_agent_step import _build_changed_files_bundle
from scripts import run_agent


def result(role, status='ready for next stage', next_owner='qa_analyst', operations=None):
    return {'agent': role, 'status': status,
            'workflow_outcome': 'completed' if status == 'completed' else 'blocked' if status == 'blocked' else 'continue',
            'handoff': {'next_owner': next_owner}, 'file_operations': operations or []}


class QualityTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.old_cwd = Path.cwd()
        os.chdir(self.root)
        self.addCleanup(os.chdir, self.old_cwd)
        self.env = patch.dict(os.environ, {'LEASE_LENS_REPO_ROOT': str(self.root)})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.runs_patch = patch.object(run_agent, 'RUNS_DIR', self.root / 'runtime/runs')
        self.runs_patch.start()
        self.addCleanup(self.runs_patch.stop)

    def test_engineer_manager_qa_keeps_exact_files(self):
        operation = {'action': 'write_file', 'path': 'docs/note.md', 'content': '# Valid note\n'}
        outputs = [result('software_engineer', next_owner='project_manager', operations=[operation]),
                   result('project_manager', next_owner='software_engineer'),
                   result('qa_analyst', 'completed')]
        def agent(role, task, previous_output=None):
            if role == 'qa_analyst':
                bundle = _build_changed_files_bundle(previous_output)
                self.assertEqual(bundle['changed_paths'], ['docs/note.md'])
                self.assertEqual(bundle['files'][0]['content'], '# Valid note\n')
            return outputs.pop(0)
        with patch.object(engine, 'run_agent_step', side_effect=agent):
            final = engine.run_workflow({'workflow': 'process_change'}, start_role_override='software_engineer')
        self.assertEqual(final['status'], 'completed')

    def test_artifact_uses_configured_target_root(self):
        (self.root / 'note.md').write_text('actual target')
        child = self.root / 'runner'
        child.mkdir()
        os.chdir(child)
        bundle = engine.build_changed_files_artifact([{'path': 'note.md'}])
        self.assertEqual(bundle['files'][0]['content'], 'actual target')

    def test_blocked_qa_fails(self):
        with patch.object(run_agent, 'run_workflow', return_value=result('qa_analyst', 'blocked')):
            with self.assertRaisesRegex(RuntimeError, 'QA did not approve'):
                run_agent.run_with_bounded_retry({'workflow': 'process_change'})
        self.assertFalse(json.loads((self.root / 'runtime/runs/workflow_result.json').read_text())['passed'])

    def test_completed_non_qa_fails(self):
        with patch.object(run_agent, 'run_workflow', return_value=result('software_engineer', 'completed')):
            with self.assertRaises(RuntimeError):
                run_agent.run_with_bounded_retry({'workflow': 'process_change'})

    def test_missing_result_fails(self):
        with patch.object(run_agent, 'run_workflow', return_value=None):
            with self.assertRaises(RuntimeError):
                run_agent.run_with_bounded_retry({'workflow': 'process_change'})

    def test_approved_qa_passes(self):
        with patch.object(run_agent, 'run_workflow', return_value=result('qa_analyst', 'completed')):
            self.assertTrue(run_agent.run_with_bounded_retry({'workflow': 'process_change'})['passed'])

    def test_exhausted_retry_fails_and_preserves_evidence(self):
        revision = result('qa_analyst', 'requires revision')
        revision['changed_file_operations'] = [{'path': 'docs/note.md'}]
        with patch.object(run_agent, 'run_workflow', side_effect=[revision, revision]) as run:
            with self.assertRaises(RuntimeError):
                run_agent.run_with_bounded_retry({'workflow': 'process_change'})
        self.assertEqual(run.call_count, 2)
        self.assertEqual(run.call_args.args[0]['changed_file_operations'], revision['changed_file_operations'])

    def test_retry_approval_passes(self):
        revision = result('qa_analyst', 'requires revision')
        revision['changed_file_operations'] = [{'path': 'docs/note.md'}]
        with patch.object(run_agent, 'run_workflow', side_effect=[revision, result('qa_analyst', 'completed')]):
            self.assertEqual(run_agent.run_with_bounded_retry({'workflow': 'process_change'})['retries_used'], 1)


if __name__ == '__main__':
    unittest.main()
