"""Tests for meta_os (portfolio matrix, constants)."""

from __future__ import annotations

from auto_client_acquisition.meta_os import (
    META_FLYWHEEL_STAGES,
    META_SUBSYSTEMS,
    PortfolioMatrixBand,
    PortfolioMatrixInputs,
    portfolio_matrix_band,
)


def test_meta_subsystems_len() -> None:
    assert len(META_SUBSYSTEMS) == 9


def test_portfolio_scale_band() -> None:
    i = PortfolioMatrixInputs(80, 80, 80, 75)
    assert portfolio_matrix_band(i) == PortfolioMatrixBand.SCALE


def test_portfolio_kill_weak() -> None:
    i = PortfolioMatrixInputs(35, 35, 50, 45)
    assert portfolio_matrix_band(i) == PortfolioMatrixBand.KILL


def test_flywheel_stages() -> None:
    assert META_FLYWHEEL_STAGES[0] == "market_signal"
    assert "venture" in META_FLYWHEEL_STAGES
