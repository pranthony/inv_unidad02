import pandas as pd, numpy as np, statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.diagnostic import acorr_breusch_godfrey, het_breuschpagan, breaks_cusumolsresid
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime, warnings
warnings.filterwarnings('ignore')

# ─── DATOS ───────────────────────────────────────────────────────────────────
df = pd.read_excel('data/processed/Base_datos.xlsx')
month_map = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',
             'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
def cf(val):
    if isinstance(val, str): return pd.Timestamp(f'20{val[3:]}-{month_map[val[:3]]}-01')
    if isinstance(val, datetime.datetime): return pd.Timestamp(val)
    return pd.Timestamp(val)
df['Tiempo'] = df['Tiempo'].apply(cf)
df = df.sort_values('Tiempo').reset_index(drop=True)
df['TIR_lag1'] = df['TIR'].shift(1)
df['TIR_lag2'] = df['TIR'].shift(2)
df['ln_CR']    = np.log(df['CR'].astype(float))
df['ln_NO']    = np.log(df['NO'].astype(float))
df2 = df.dropna().copy().reset_index(drop=True)
df2['ln_CR_lag1'] = df2['ln_CR'].shift(1)
df3 = df2.dropna().copy().reset_index(drop=True)
df3['D_COVID'] = ((df3['Tiempo'] >= '2020-04-01') & (df3['Tiempo'] <= '2020-06-01')).astype(int)

varnames_ext = ['ln_CR_lag1','TIR_lag1','TIR_lag2','TM','TD','ln_NO','DR','D_COVID']
y   = df3['ln_CR'].values
Xe  = sm.add_constant(df3[varnames_ext])
mod = sm.OLS(y, Xe).fit()
mod_nw = mod.get_robustcov_results(cov_type='HAC', maxlags=4)
names  = mod.model.exog_names
P  = {n: float(v) for n, v in zip(names, mod_nw.params)}
PV = {n: float(v) for n, v in zip(names, mod_nw.pvalues)}
SE = {n: float(v) for n, v in zip(names, mod_nw.bse)}
resid  = mod.resid.values
coef_lag = P['ln_CR_lag1']

def sig(p):
    if p<0.01: return "***"
    elif p<0.05: return "**"
    elif p<0.10: return "*"
    else: return "ns"

# ─── CUSUM ───────────────────────────────────────────────────────────────────
cusum_stat, cusum_pval, cusum_cv = breaks_cusumolsresid(mod.resid)
jb_r  = stats.jarque_bera(resid)
dw_r  = durbin_watson(resid)
bg_r  = acorr_breusch_godfrey(mod, nlags=4)
bp_r  = het_breuschpagan(resid, Xe.values)

print("="*65)
print("PASO 8 — ESTABILIDAD CUSUM")
print("="*65)
print(f"  Estadistico : {cusum_stat:.4f}")
print(f"  p-valor     : {cusum_pval:.4f}")
print(f"  Conclusion  : {'Parametros estables (p>0.05)' if cusum_pval>0.05 else 'Posible quiebre estructural'}")

print("\n" + "="*65)
print("PASO 9 — TABLA COMPARATIVA FINAL")
print("="*65)

# 3 modelos para comparar
df2b = df2.copy()
varnames_base = ['ln_CR_lag1','TIR_lag1','TIR_lag2','TM','TD','ln_NO','DR']
Xb  = sm.add_constant(df3[varnames_base])
mod_b = sm.OLS(y, Xb).fit()

# modelo sin rezago (original)
df_orig = df.copy()
df_orig['TIR_lag1'] = df_orig['TIR'].shift(1)
df_orig['TIR_lag2'] = df_orig['TIR'].shift(2)
df_orig['ln_CR']    = np.log(df_orig['CR'].astype(float))
df_orig['ln_NO']    = np.log(df_orig['NO'].astype(float))
df_orig = df_orig.dropna().copy().reset_index(drop=True)
df_orig['D_COVID'] = ((df_orig['Tiempo'] >= '2020-04-01') & (df_orig['Tiempo'] <= '2020-06-01')).astype(int)
X_orig = sm.add_constant(df_orig[['TIR_lag1','TIR_lag2','TM','TD','ln_NO','DR','D_COVID']])
mod_orig = sm.OLS(df_orig['ln_CR'].values, X_orig).fit()

modelos = [
    ("M1: OLS sin lag CR",  mod_orig),
    ("M2: ADL(1,2) base",   mod_b),
    ("M3: ADL+COVID [FINAL]", mod),
]
print(f"\n  {'Modelo':<24} {'R2':>6} {'R2aj':>6} {'AIC':>9} {'DW':>6} {'JB p':>7} {'BG p':>7} {'BP p':>7}")
print("  "+"-"*72)
for nm, m in modelos:
    r_ = m.resid.values
    X_ = m.model.exog
    dw_ = durbin_watson(r_)
    jb_ = stats.jarque_bera(r_)
    bg_ = acorr_breusch_godfrey(m, nlags=4)
    bp_ = het_breuschpagan(r_, X_)
    print(f"  {nm:<24} {m.rsquared:>6.4f} {m.rsquared_adj:>6.4f} {m.aic:>9.2f} "
          f"{dw_:>6.4f} {float(jb_.pvalue):>7.4f} {float(bg_[1]):>7.4f} {float(bp_[1]):>7.4f}")

# ─── FIGURA FINAL: PANEL COMPLETO ────────────────────────────────────────────
fig = plt.figure(figsize=(16, 14))
fig.suptitle('Modelo 5 — Panel Completo de Resultados\nADL(1,2) + D_COVID | Newey-West HAC (4 rezagos)',
             fontsize=13, fontweight='bold', y=1.01)

gs = fig.add_gridspec(3, 3, hspace=0.45, wspace=0.35)

# ── 1. Serie observada vs ajustada ──
ax1 = fig.add_subplot(gs[0, :])
ax1.plot(df3['Tiempo'], y, label='ln_CR observado', color='#1D4ED8', linewidth=1.3)
ax1.plot(df3['Tiempo'], mod.fittedvalues, label='ln_CR ajustado', color='#DC2626',
         linewidth=1.3, linestyle='--')
# Sombra Reactiva
mask_r = df3['DR'] == 1
if mask_r.any():
    t_r = df3.loc[mask_r, 'Tiempo']
    ax1.axvspan(t_r.min(), t_r.max(), alpha=0.12, color='orange', label='Reactiva Perú')
# Sombra COVID
mask_c = df3['D_COVID'] == 1
if mask_c.any():
    t_c = df3.loc[mask_c, 'Tiempo']
    ax1.axvspan(t_c.min(), t_c.max(), alpha=0.15, color='red', label='COVID')
ax1.set_title(f'Serie observada vs ajustada  |  R²={mod.rsquared:.4f}  |  n={len(df3)}',
              fontweight='bold')
ax1.set_ylabel('ln(Crédito real)')
ax1.legend(fontsize=9, loc='upper left')
ax1.grid(alpha=0.25)
ax1.tick_params(axis='x', rotation=30)

# ── 2. Residuos en el tiempo ──
ax2 = fig.add_subplot(gs[1, 0])
colors_r = ['#DC2626' if r<0 else '#16A34A' for r in resid]
ax2.bar(range(len(resid)), resid, color=colors_r, alpha=0.7, width=1)
ax2.axhline(0, color='black', linewidth=0.8)
ic_r = 2*resid.std()
ax2.axhline(ic_r,  color='gray', linestyle='--', linewidth=0.8, alpha=0.7)
ax2.axhline(-ic_r, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)
ax2.set_title('Residuos del modelo', fontweight='bold')
ax2.set_xlabel('Observación'); ax2.set_ylabel('Residuo')

# ── 3. Histograma de residuos ──
ax3 = fig.add_subplot(gs[1, 1])
ax3.hist(resid, bins=22, density=True, color='#7C3AED', alpha=0.65, edgecolor='white')
xx = np.linspace(resid.min(), resid.max(), 200)
ax3.plot(xx, stats.norm.pdf(xx, resid.mean(), resid.std()), 'r-', lw=2)
ax3.set_title(f'Distribución residuos\nJB p={float(jb_r.pvalue):.4f}', fontweight='bold')
ax3.set_xlabel('Residuo'); ax3.set_ylabel('Densidad')

# ── 4. Q-Q plot ──
ax4 = fig.add_subplot(gs[1, 2])
(osm, osr), (slope, intercept, _) = stats.probplot(resid, dist='norm')
ax4.scatter(osm, osr, color='#059669', s=14, alpha=0.7)
ax4.plot([min(osm),max(osm)], [slope*min(osm)+intercept, slope*max(osm)+intercept],
         'r--', lw=1.5)
ax4.set_title('Q-Q Plot residuos', fontweight='bold')
ax4.set_xlabel('Cuantiles teóricos'); ax4.set_ylabel('Cuantiles muestrales')

# ── 5. Coeficientes CP con IC ──
ax5 = fig.add_subplot(gs[2, 0])
vars_p = ['TIR_lag1','TIR_lag2','TM','TD','ln_NO','DR','D_COVID']
labs_p = ['TIR(t-1)','TIR(t-2)','Morosidad','Dolariz.','ln(Puntos)','D_Reactiva','D_COVID']
coefs_p = [P[v] for v in vars_p]
errs_p  = [SE[v] for v in vars_p]
pv_p    = [PV[v] for v in vars_p]
bc = ['#16A34A' if p<0.05 else ('#F59E0B' if p<0.10 else '#94A3B8') for p in pv_p]
ax5.barh(labs_p, coefs_p, xerr=errs_p, color=bc, alpha=0.85,
         error_kw={'ecolor':'#374151','capsize':3})
ax5.axvline(0, color='black', linewidth=1)
ax5.set_title('Coeficientes CP (NW)\nverde=5%, amarillo=10%', fontweight='bold', fontsize=9)
ax5.set_xlabel('Coeficiente')

# ── 6. Multiplicadores LP ──
ax6 = fig.add_subplot(gs[2, 1])
lp_vals = [P[v]/(1-coef_lag) for v in vars_p]
bc_lp = ['#16A34A' if p<0.05 else ('#F59E0B' if p<0.10 else '#94A3B8') for p in pv_p]
ax6.barh(labs_p, lp_vals, color=bc_lp, alpha=0.85)
ax6.axvline(0, color='black', linewidth=1)
for i, (v, p) in enumerate(zip(lp_vals, pv_p)):
    if p < 0.10:
        ax6.text(v+(0.05 if v>=0 else -0.05), i, f'{v:.2f}', va='center',
                 ha='left' if v>=0 else 'right', fontsize=8, fontweight='bold')
ax6.set_title('Multiplicadores LP\ncoef/(1-rho)', fontweight='bold', fontsize=9)
ax6.set_xlabel('Efecto acumulado LP')

# ── 7. Tabla diagnósticos ──
ax7 = fig.add_subplot(gs[2, 2])
ax7.axis('off')
diag_data = [
    ['Prueba', 'Estadístico', 'p-valor', 'Resultado'],
    ['Jarque-Bera', f'{float(jb_r.statistic):.3f}', f'{float(jb_r.pvalue):.4f}',
     '✓' if float(jb_r.pvalue)>0.05 else '✗'],
    ['Durbin-Watson', f'{dw_r:.4f}', '—',
     '✓' if 1.5<dw_r<2.5 else '✗'],
    ['Breusch-Godfrey', f'{float(bg_r[0]):.3f}', f'{float(bg_r[1]):.4f}',
     '✓' if float(bg_r[1])>0.05 else '✗'],
    ['Breusch-Pagan', f'{float(bp_r[0]):.3f}', f'{float(bp_r[1]):.4f}',
     '✓' if float(bp_r[1])>0.05 else '✗'],
    ['CUSUM', f'{cusum_stat:.4f}', f'{cusum_pval:.4f}',
     '✓' if cusum_pval>0.05 else '✗'],
    ['R²', f'{mod.rsquared:.4f}', '—', ''],
    ['R² ajustado', f'{mod.rsquared_adj:.4f}', '—', ''],
]
tbl = ax7.table(cellText=diag_data[1:], colLabels=diag_data[0],
                loc='center', cellLoc='center')
tbl.auto_set_font_size(False)
tbl.set_fontsize(8.5)
tbl.scale(1.1, 1.4)
for (row, col), cell in tbl.get_celld().items():
    if row == 0:
        cell.set_facecolor('#1D4ED8')
        cell.set_text_props(color='white', fontweight='bold')
    elif col == 3:
        txt = cell.get_text().get_text()
        cell.set_facecolor('#DCFCE7' if txt == '✓' else ('#FEE2E2' if txt == '✗' else 'white'))
ax7.set_title('Diagnósticos del modelo', fontweight='bold', fontsize=9)

plt.savefig('panel_completo_modelo5.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nPanel completo guardado.")

# ─── REPORTE TXT FINAL COMPLETO ──────────────────────────────────────────────
L = "="*65; l = "-"*65
lines = [
    L,
    "MODELO 5 — REPORTE FINAL COMPLETO",
    "Determinantes del Credito al Sector Privado Real en Peru",
    f"Muestra: {df3['Tiempo'].min().strftime('%Y-%m')} — {df3['Tiempo'].max().strftime('%Y-%m')}",
    f"Obs: {len(df3)} | Frecuencia: mensual",
    L, "",
    "ESPECIFICACION FINAL [ADL(1,2) + D_COVID | Newey-West HAC 4 rezagos]:",
    "ln(CR)t = B0 + rho*ln(CR)(t-1) + B1*TIR(t-1) + B2*TIR(t-2)",
    "         + B3*TM + B4*TD + B5*ln(NO) + B6*DR + B7*D_COVID + e", "",
    l, "I. RAICES UNITARIAS", l,
    "  Variable    Orden  Interpretacion",
    "  ln_CR       I(1)   Tendencia secular — trabajar en ADL",
    "  TIR         I(2)+  Incluida en rezagos dentro del ADL",
    "  TM          I(1)   Primera diferencia estacionaria",
    "  TD          I(0)   Estacionaria en niveles",
    "  ln_NO       I(1)   Primera diferencia estacionaria", "",
    l, "II. COEFICIENTES FINALES (Newey-West HAC, 4 rezagos)", l,
    f"  {'Variable':<14} {'Coef':>9}  {'E.E.':>8}  {'p-valor':>9}  Sig",
    "  "+"-"*56,
]
for n in names:
    lines.append(f"  {n:<14} {P[n]:>+9.4f}  {SE[n]:>8.4f}  {PV[n]:>9.4f}  {sig(PV[n])}")

lines += ["",
    f"  R2 = {mod.rsquared:.4f}  |  R2 ajustado = {mod.rsquared_adj:.4f}",
    f"  F-stat p-valor = {mod.f_pvalue:.8f}",
    f"  AIC = {mod.aic:.4f}  |  BIC = {mod.bic:.4f}", "",
    l, "III. DIAGNOSTICOS", l,
    f"  Jarque-Bera      : stat={float(jb_r.statistic):.4f}  p={float(jb_r.pvalue):.4f}  {'OK' if float(jb_r.pvalue)>0.05 else 'PROBLEMA — outliers COVID persistentes'}",
    f"  Durbin-Watson    : {dw_r:.4f}  {'OK (rango 1.5-2.5)' if 1.5<dw_r<2.5 else 'PROBLEMA'}",
    f"  Breusch-Godfrey  : stat={float(bg_r[0]):.4f}  p={float(bg_r[1]):.4f}  {'OK' if float(bg_r[1])>0.05 else 'Autocorrelacion residual — NW mitiga inferencia'}",
    f"  Breusch-Pagan    : stat={float(bp_r[0]):.4f}  p={float(bp_r[1]):.4f}  {'OK' if float(bp_r[1])>0.05 else 'Heterocedasticidad — corregida con NW HAC'}",
    f"  CUSUM estabilidad: stat={cusum_stat:.4f}  p={cusum_pval:.4f}  {'Parametros estables' if cusum_pval>0.05 else 'Posible quiebre estructural'}", "",
    l, "IV. MULTIPLICADORES DE LARGO PLAZO", l,
    f"  rho = {coef_lag:.4f}  |  Velocidad ajuste = {(1-coef_lag)*100:.2f}%/mes  |  Vida media = {np.log(0.5)/np.log(coef_lag):.1f} meses",
    "",
    f"  {'Variable':<14} {'CP':>9}  {'LP':>10}  Sig LP",
    "  "+"-"*45,
]
for v, lab in zip(['TIR_lag1','TIR_lag2','TM','TD','ln_NO','DR','D_COVID'],
                  ['TIR(t-1)','TIR(t-2)','Morosidad','Dolariz.','ln(Puntos)','D_Reactiva','D_COVID']):
    lp = P[v]/(1-coef_lag)
    lines.append(f"  {lab:<14} {P[v]:>+9.4f}  {lp:>+10.4f}  {sig(PV[v])}")

tir_lp = (P['TIR_lag1']+P['TIR_lag2'])/(1-coef_lag)
lines += ["",
    f"  Efecto LP acumulado TIR (t-1+t-2) = {tir_lp:+.4f}",
    f"  -> 100 pb de aumento en TIR del BCRP reduce el credito",
    f"     real en {abs(tir_lp)*100:.1f}% en el largo plazo.",
    "",
    l, "V. INTERPRETACION ECONOMICA", l, "",
    "  1. CANAL DEL CREDITO CONFIRMADO:",
    f"     TIR(t-1) es significativa al 10% (p={PV['TIR_lag1']:.4f}).",
    f"     Un aumento de 1 pp en la tasa de referencia del BCRP",
    f"     reduce el credito real en {abs(P['TIR_lag1'])*100:.2f}% en el primer mes.",
    f"     El efecto LP acumulado alcanza {abs(tir_lp)*100:.1f}%, confirmando",
    "     la efectividad del canal crediticio de la politica monetaria.",
    "",
    "  2. ALTA PERSISTENCIA DEL CREDITO:",
    f"     rho = {coef_lag:.4f}. El credito es un proceso altamente persistente.",
    f"     La vida media del ajuste es {np.log(0.5)/np.log(coef_lag):.0f} meses (~{np.log(0.5)/np.log(coef_lag)/12:.1f} anos).",
    "     Esto implica que shocks crediticios se disipan lentamente.",
    "",
    "  3. MOROSIDAD Y DOLARIZACION NO SIGNIFICATIVAS:",
    "     En frecuencia mensual y con el rezago de CR dominando,",
    "     TM y TD pierden significancia. Son mas relevantes en",
    "     especificaciones trimestrales o en modelos de largo plazo.",
    "",
    "  4. SHOCK COVID CAPTURADO:",
    f"     D_COVID es significativa *** (p={PV['D_COVID']:.4f}).",
    "     Aisla el impacto del confinamiento de abril-junio 2020",
    "     para que no contamine los coeficientes estructurales.",
    "",
    "  5. REACTIVA PERU NO SIGNIFICATIVA EN ADL:",
    "     DR no es significativa en el modelo dinamico porque",
    "     el rezago de CR ya captura gran parte de la inercia",
    "     crediticia, incluyendo el impulso de Reactiva.",
    "",
    l, "VI. TABLA COMPARATIVA DE ESPECIFICACIONES", l,
    "",
    f"  {'Modelo':<24} {'R2':>6} {'R2aj':>6} {'AIC':>9} {'DW':>6} {'JB p':>7} {'BG p':>7} {'BP p':>7}",
    "  "+"-"*72,
]
for nm, m in [("M1: OLS sin lag CR", sm.OLS(df_orig['ln_CR'].values, X_orig).fit()),
              ("M2: ADL(1,2) base",   sm.OLS(y, sm.add_constant(df3[['ln_CR_lag1','TIR_lag1','TIR_lag2','TM','TD','ln_NO','DR']])).fit()),
              ("M3: ADL+COVID [FINAL]", mod)]:
    r_ = m.resid.values
    dw_ = durbin_watson(r_)
    jb_ = stats.jarque_bera(r_)
    bg_ = acorr_breusch_godfrey(m, nlags=4)
    bp_ = het_breuschpagan(r_, m.model.exog)
    lines.append(f"  {nm:<24} {m.rsquared:>6.4f} {m.rsquared_adj:>6.4f} {m.aic:>9.2f} "
                 f"{dw_:>6.4f} {float(jb_.pvalue):>7.4f} {float(bg_[1]):>7.4f} {float(bp_[1]):>7.4f}")

with open('reporte_final.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(lines))

print("Reporte final guardado.")
print(f"\nARCHIVOS GENERADOS:")
print(f"  1. reporte_final.txt")
print(f"  2. panel_completo_modelo5.png")
print(f"  3. diagnosticos_residuos.png")
print(f"  4. coeficientes_modelo5.png")
print(f"  5. serie_ajustada_modelo5.png")
