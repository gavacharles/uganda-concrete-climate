"""Probabilistic carbonation model (fib Bulletin 34 / Model Code 2010) with time-varying climate.

Carbonation depth for a building cast in year t0, evaluated at year t:

    x_c(t) = sqrt( sum_{tau=t0}^{t} R(tau) * dt ) * W(t - t0)
    R(tau) = 2 * k_e(RH) * k_c * k_T(T) * (k_t * R_inv + eps_t) * C_S(tau)

k_e   environmental (RH) function, RH_ref = 65 %, f_e = 5.0, g_e = 2.5   (fib B34)
k_c   curing, (t_c / 7)^b_c, b_c ~ N(-0.567, 0.024)                      (fib B34)
k_t   test-method factor ~ N(1.25, 0.35); eps_t ~ N(1.0e-11, 0.15e-11)   (fib B34)
R_inv inverse carbonation resistance, mean by w/c for CEM I (fib B34 table),
      s = 0.69 * m^0.78 (units 1e-11 (m^2/s)/(kg/m^3)), scaled for blended cements
k_T   Arrhenius temperature factor, E = 40 kJ/mol, T_ref = 20 degC (Stewart et al. 2011)
C_S   CO2 mass concentration from ppm, corrected for site pressure (elevation) and an
      urban enhancement factor
W     weather function (t0/t)^w, w = (p_SR * ToW)^b_w / 2, b_w ~ N(0.446, 0.163);
      p_SR = 0 for elements sheltered from rain (W = 1)

Corrosion initiation when x_c >= cover.
"""
from dataclasses import dataclass, field

import numpy as np

SECONDS_PER_YEAR = 365.25 * 24 * 3600
R_GAS = 8.314
M_CO2 = 0.04401  # kg/mol

# fib Bulletin 34 mean R_ACC,0^-1 for CEM I 42.5 R, units 1e-11 (m^2/s)/(kg/m^3)
_WC = np.array([0.40, 0.45, 0.50, 0.55, 0.60])
_RINV = np.array([3.1, 5.2, 6.8, 9.8, 13.4])
_FIT = np.polyfit(_WC, np.log(_RINV), 1)  # log-linear, used to extrapolate to w/c 0.7


def rinv_mean_cem1(wc):
    """Mean inverse carbonation resistance for CEM I (1e-11 units); table interpolation, log-linear beyond."""
    wc = np.asarray(wc, dtype=float)
    inside = (wc >= _WC[0]) & (wc <= _WC[-1])
    out = np.exp(np.polyval(_FIT, wc))
    out[inside] = np.interp(wc[inside], _WC, _RINV)
    return out


def co2_kg_m3(ppm, temp_c, elevation_m):
    """CO2 mass concentration (kg/m^3) from mole fraction, using the barometric formula for site pressure."""
    p = 101325.0 * (1 - 2.25577e-5 * elevation_m) ** 5.25588
    return ppm * 1e-6 * M_CO2 * p / (R_GAS * (temp_c + 273.15))


def k_e(rh_pct):
    rh = np.clip(np.asarray(rh_pct) / 100.0, 0.0, 0.99)
    return ((1 - rh ** 5.0) / (1 - 0.65 ** 5.0)) ** 2.5


def k_T(temp_c, activation_j=40000.0, t_ref_c=20.0):
    return np.exp(activation_j / R_GAS * (1 / (t_ref_c + 273.15) - 1 / (np.asarray(temp_c) + 273.15)))


@dataclass
class ConcreteSpec:
    """Distributions describing a class of concrete as specified or as built."""
    name: str
    wc_low: float          # uniform w/c bounds
    wc_high: float
    cover_mean_mm: float   # normal cover, truncated at cover_min_mm
    cover_sd_mm: float
    curing_days_low: float  # uniform curing duration
    curing_days_high: float
    blend_factor_low: float = 1.0   # multiplier on R_inv relative to CEM I (lognormal-uniform)
    blend_factor_high: float = 1.0
    cover_min_mm: float = 5.0


@dataclass
class Exposure:
    sheltered: bool = True
    p_splash_rain: float = 0.0     # probability of driving rain on the element
    urban_co2_factor: float = 1.10  # urban CO2 enhancement over background
    activation_j: float = 40000.0   # activation energy in the Arrhenius factor (J/mol)


@dataclass
class Samples:
    n: int
    rng: np.random.Generator = field(default_factory=lambda: np.random.default_rng(1))

    def draw(self, spec: ConcreteSpec):
        r = self.rng
        n = self.n
        wc = r.uniform(spec.wc_low, spec.wc_high, n)
        m = rinv_mean_cem1(wc)
        sd = 0.69 * m ** 0.78
        # lognormal with matching mean and sd keeps R_inv positive
        sig = np.sqrt(np.log(1 + (sd / m) ** 2))
        rinv = r.lognormal(np.log(m) - sig ** 2 / 2, sig) * 1e-11
        blend = np.exp(r.uniform(np.log(spec.blend_factor_low), np.log(spec.blend_factor_high), n))
        cover = np.maximum(r.normal(spec.cover_mean_mm, spec.cover_sd_mm, n), spec.cover_min_mm)
        tc = r.uniform(spec.curing_days_low, spec.curing_days_high, n)
        bc = r.normal(-0.567, 0.024, n)
        kt = np.maximum(r.normal(1.25, 0.35, n), 0.1)
        eps = np.maximum(r.normal(1.0e-11, 0.15e-11, n), 0.0)
        bw = r.normal(0.446, 0.163, n)
        return dict(wc=wc, rinv=rinv * blend, cover_mm=cover, kc=(tc / 7.0) ** bc, kt=kt, eps=eps, bw=bw,
                    blend=blend, curing_days=tc)


def carbonation_depth_mm(p, years, temp_c, rh_pct, co2_ppm, elevation_m, exposure: Exposure,
                         tow=None):
    """Carbonation depth paths for one cohort.

    p        dict of sampled material parameters (arrays of length n)
    years    1-D array of calendar years from the casting year onwards (annual steps)
    temp_c, rh_pct, co2_ppm   arrays shaped (n, len(years)) or (len(years),)
    tow      time of wetness (fraction of days with >= 2.5 mm rain), same shape; only used if not sheltered
    Returns depth (n, len(years)) in mm, evaluated at the END of each year.
    """
    temp_c = np.broadcast_to(temp_c, (p["kc"].size, len(years)))
    rh_pct = np.broadcast_to(rh_pct, temp_c.shape)
    co2_ppm = np.broadcast_to(co2_ppm, temp_c.shape)
    cs = co2_kg_m3(co2_ppm, temp_c, elevation_m) * exposure.urban_co2_factor
    rate = (2 * k_e(rh_pct) * p["kc"][:, None] * k_T(temp_c, exposure.activation_j)
            * (p["kt"][:, None] * p["rinv"][:, None] + p["eps"][:, None]) * cs)
    x2 = np.cumsum(rate * SECONDS_PER_YEAR, axis=1)  # m^2
    age = np.arange(1, len(years) + 1, dtype=float)
    if exposure.sheltered or tow is None:
        weather = 1.0
    else:
        tow_mean = np.cumsum(np.broadcast_to(tow, temp_c.shape), axis=1) / age
        w = (exposure.p_splash_rain * tow_mean) ** p["bw"][:, None] / 2.0
        weather = (0.0767 / age) ** w  # t0 = 0.0767 yr (28 d), fib B34
    return np.sqrt(x2) * weather * 1000.0


def depth_variable_start_mm(p, years, temp_c, rh_pct, co2_ppm, elevation_m, cast_year,
                            exposure: Exposure):
    """Sheltered-member depth paths when each realisation has its own casting year.

    Rates before a realisation's casting year are zeroed, so x^2 accumulates from that year.
    Returns (n, len(years)) depth in mm at the end of each calendar year (0 before casting).
    """
    shape = (p["kc"].size, len(years))
    temp_c = np.broadcast_to(temp_c, shape)
    cs = co2_kg_m3(np.broadcast_to(co2_ppm, shape), temp_c, elevation_m) * exposure.urban_co2_factor
    rate = (2 * k_e(np.broadcast_to(rh_pct, shape)) * p["kc"][:, None] * k_T(temp_c, exposure.activation_j)
            * (p["kt"][:, None] * p["rinv"][:, None] + p["eps"][:, None]) * cs)
    rate = np.where(np.asarray(years)[None, :] >= cast_year[:, None], rate, 0.0)
    return np.sqrt(np.cumsum(rate * SECONDS_PER_YEAR, axis=1)) * 1000.0


def initiation_probability(depth_mm, cover_mm):
    """Fraction of realisations with depth >= cover, per year."""
    return (depth_mm >= cover_mm[:, None]).mean(axis=0)


# Blended-cement multiplier on R_inv, calibrated: in the NCP model (Ekolu & Solomon 2022, Table 1)
# depth ~ cem * f^g with g = -1.5 (CEM I) and -1.4 (CEM II/B, CEM IV/A). Ugandan kamafugite/carbonatite
# pozzolans give 75-89 % of CEM I strength at equal w/c (Buregyeya et al. 2018, SAI at 180 d, 20 %
# replacement; lower bound extrapolated to the 21-35 % of CEM II/B-P). For f(CEM I) = 25-30 MPa this gives
# depth ratios of 1.6-2.1, i.e. R_inv multipliers of 2.6-4.4 (depth ~ sqrt(R_inv)).
BLEND = (2.6, 4.4)

SPECS = {
    # design intent for a C25/30-C30/37 building element under BS 8110 / EN 1992 practice
    "design_CEM_I": ConcreteSpec("design, CEM I", 0.50, 0.55, 30.0, 5.0, 7, 7),
    "design_blended": ConcreteSpec("design, CEM II/B-P or CEM IV", 0.50, 0.55, 30.0, 5.0, 7, 7, *BLEND),
    # typical site-batched practice: higher w/c, short curing, cover shortfall
    "asbuilt_blended": ConcreteSpec("as built, CEM II/B-P or CEM IV", 0.55, 0.70, 22.0, 8.0, 1, 3, *BLEND),
}


if __name__ == "__main__":
    # fib reference check: CEM I, w/c 0.50, 7 d curing, 65 % RH, 20 degC, sea level, sheltered, 50 years
    n = 20000
    smp = Samples(n)
    spec = ConcreteSpec("check", 0.50, 0.50, 30, 0.001, 7, 7)
    p = smp.draw(spec)
    yrs = np.arange(50)
    ppm = 0.00082 / (1e-6 * M_CO2 * 101325 / (R_GAS * 293.15))  # fib C_S = 8.2e-4 kg/m3
    d = carbonation_depth_mm(p, yrs, 20.0, 65.0, ppm, 0.0, Exposure(urban_co2_factor=1.0))
    print(f"fib check: mean depth at 50 yr = {d[:, -1].mean():.1f} mm (hand calc of mean inputs ~15.7 mm)")
