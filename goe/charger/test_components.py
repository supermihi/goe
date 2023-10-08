from goe.charger.components import ChargingEnergies
from goe.components.common import PerPhase, PerPhaseWithN


def test_energies_from_nrg():
    nrg = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    energies = ChargingEnergies.from_nrg(nrg)

    expected = ChargingEnergies(voltage=PerPhaseWithN(1, 2, 3, 4),
                                current=PerPhase(5, 6, 7),
                                power=PerPhaseWithN(8, 9, 10, 11),
                                power_total=12,
                                power_factor=PerPhaseWithN(13, 14, 15, 16))

    assert energies == expected

