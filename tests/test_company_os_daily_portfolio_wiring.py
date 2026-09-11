from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RUNNER=ROOT/'scripts'/'commercial'/'run_company_os_daily.py'

def test_daily_runner_reuses_canonical_company_os_and_adds_portfolio_command():
    src=RUNNER.read_text(encoding='utf-8')
    assert 'run_self_operating_company_os.py' in src
    assert 'verify_dealix_operating_constitution.py' in src
    assert 'verify_dealix_arm_registry.py' in src
    assert 'run_president_portfolio_command_v1.py' in src
    assert 'verify_president_portfolio_command_v1.py' in src
    assert 'run_strategy_execution_orchestrator_v1.py' in src

def test_daily_runner_does_not_create_second_scheduler_or_live_effects():
    src=RUNNER.read_text(encoding='utf-8')
    forbidden=['systemctl','crontab','schedule.every','requests.post(','send_message(','gh pr merge','railway up','stripe.']
    assert all(token not in src for token in forbidden)
    assert 'parallel state store' in src
    assert 'permanent agent fleet' in src
