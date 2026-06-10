"""Meta-Operating System — portfolio matrix and structural constants (no I/O)."""

from auto_client_acquisition.meta_os.flywheel import META_FLYWHEEL_STAGES
from auto_client_acquisition.meta_os.portfolio_matrix import (
    PortfolioMatrixBand,
    PortfolioMatrixInputs,
    portfolio_matrix_band,
)
from auto_client_acquisition.meta_os.subsystems import META_SUBSYSTEMS

__all__ = [
    "META_FLYWHEEL_STAGES",
    "META_SUBSYSTEMS",
    "PortfolioMatrixBand",
    "PortfolioMatrixInputs",
    "portfolio_matrix_band",
]
