# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ================= CONFIGURAÇÃO DE FONTES =================
plt.rcParams.update({
    "font.size": 14,
    "axes.titlesize": 18,
    "axes.labelsize": 16,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 14,
})

# ================= SCIPY =================
# Tenta importar as funções butter e filtfilt da biblioteca scipy.signal.
# Elas serão usadas para filtrar o sinal de pressão com filtro Butterworth.
try:
    from scipy.signal import butter, filtfilt
    SCIPY_OK = True
except Exception:
    SCIPY_OK = False


# ================= UTILIDADES =================
def _to_numeric_series(s: pd.Series) -> pd.Series:
    """Converte coluna numérica ou string com vírgula decimal."""
    """ Converte uma coluna do pandas para número. Funciona tanto para valores 
    já numéricos quanto para strings com vírgula decimal, por exemplo: '22,5'.
    """
    if pd.api.types.is_numeric_dtype(s):
        return s.astype(float)
    
     # Se a coluna vier como texto:
    # 1) converte para string
    # 2) troca vírgula por ponto
    # 3) remove espaços
    # 4) tenta converter para número
    # 5) se não conseguir, coloca NaN
    
    return pd.to_numeric(
        s.astype(str).str.replace(",", ".", regex=False).str.strip(),
        errors="coerce"
    )


def butterworth_filtfilt_angle(x, theta_deg, order=4, cutoff_cyc_per_deg=0.08):
    #Aplica um filtro passa-baixa Butterworth no sinal x em função do ângulo do virabrequim (theta_deg).
    #Parâmetros:
    # x: sinal a ser filtrado
    # theta_deg: vetor de ângulo do virabrequim em graus
    # order: ordem do filtro
    # cutoff_cyc_per_deg: frequência de corte em ciclos por grau

    if not SCIPY_OK:
         # Se o SciPy não estiver disponível, interrompe a execução.
        raise ImportError("SciPy não disponível.")

    theta = np.asarray(theta_deg, float)
    # Garante que theta seja array NumPy de float.
    x = np.asarray(x, float)

    dtheta = np.mean(np.diff(theta))
    # Calcula o passo angular médio entre pontos consecutivos.
    if dtheta <= 0:
         # O ângulo precisa ser crescente para o cálculo fazer sentido.
        raise ValueError("Theta deve ser crescente.")

    fs = 1.0 / dtheta
     # "Frequência de amostragem" em pontos por grau de virabrequim.
    nyq = 0.5 * fs
     # Frequência de Nyquist.
    wn = cutoff_cyc_per_deg / nyq
     # Frequência de corte normalizada para o filtro digital.

    b, a = butter(order, wn, btype="low")
    # Cria os coeficientes do filtro Butterworth passa-baixa.
    return filtfilt(b, a, x)
    # Aplica o filtro em ida e volta, evitando defasagem no sinal.



# ================= HRR =================
def compute_hrr(
    theta_deg,
    V_m3,
    P_Pa,
    gamma=1.28,
    filter_pressure=True,
    bw_order=4,
    cutoff_cyc_per_deg=0.08,
    baseline_window=(-360, -220),
):
    """
    Calcula o HRR aparente a partir de:
    - theta_deg: ângulo do virabrequim [graus]
    - V_m3: volume do cilindro [m³]
    - P_Pa: pressão no cilindro [Pa]

    Também permite:
    - filtrar a pressão
    - definir gamma
    - aplicar correção de linha de base (baseline)
    """

    theta = np.asarray(theta_deg, float) # Converte ângulo para array NumPy float.
    V = np.asarray(V_m3, float) # Converte volume para array NumPy float.
    P = np.asarray(P_Pa, float) # Converte pressão para array NumPy float

    if filter_pressure: # Se o usuário desejar, filtra o sinal de pressão antes de derivar.
        P_f = butterworth_filtfilt_angle(
            P, theta,
            order=bw_order,
            cutoff_cyc_per_deg=cutoff_cyc_per_deg
        )
    else:
        P_f = P.copy()  # Caso contrário, usa a pressão original.

    dV_dth = np.gradient(V, theta)  # Calcula a derivada dV/dθ do volume em relação ao ângulo:
    dP_dth = np.gradient(P_f, theta) # Calcula a derivada da pressão dP/dθ filtrada em relação ao ângulo:

    hrr = (gamma / (gamma - 1.0)) * P_f * dV_dth \
        + (1.0 / (gamma - 1.0)) * V * dP_dth
    # Equação clássica do apparent heat release rate:
    # dQ/dθ = [γ/(γ-1)] * P * dV/dθ + [1/(γ-1)] * V * dP/dθ
    # onde:
    # γ = razão de calores específicos
    # P = pressão
    # V = volume
    # θ = ângulo do virabrequim

    if baseline_window is not None:         # Se foi definida uma janela de baseline, corrige o nível médio do HRR.
        t0, t1 = baseline_window            # t0 e t1 definem o intervalo angular usado para calcular a média.
        m = (theta >= t0) & (theta <= t1)   # Máscara booleana: seleciona apenas os pontos dentro da janela.
        if np.any(m):                       # Se houver pontos válidos nessa janela...
            hrr -= np.nanmean(hrr[m])       # Subtrai a média do HRR nessa região. Isso desloca a linha de base para perto de zero.

    return theta, P_f, hrr
    # Retorna:
    # theta -> ângulo
    # P_f   -> pressão filtrada
    # hrr   -> taxa de liberação de calor aparente



# ================= PIPELINE PRINCIPAL =================
def run_hrr_from_xlsx(
    xlsx_path,
    sheet_name=0,
    gamma=1.28,
    rpm=2000.0,
    theta_col="Theta",
    vol_col="Volume (cm3)",
    pressure_cols=(),
    filter_pressure=True,
    bw_order=4,
    cutoff_cyc_per_deg=0.08,
    baseline_window=(-360, -220),
    xlim=(-60, 120),
    plot_pressure=True,
    pressure_use_filtered=False,
):
    """
    Função principal do programa.
    Ela:
    1) lê os dados do Excel
    2) converte colunas para formato numérico
    3) calcula o HRR para cada caso de pressão
    4) plota HRR e pressão
    5) imprime um resumo dos picos de HRR
    """

    df = pd.read_excel(xlsx_path, sheet_name=sheet_name) # Lê a planilha Excel.
    theta = _to_numeric_series(df[theta_col]).to_numpy() # Lê a coluna do ângulo do virabrequim e converte para vetor NumPy.
    V_cm3 = _to_numeric_series(df[vol_col]).to_numpy()   # Lê a coluna de volume em cm³.

    V_m3 = V_cm3 * 1e-6  # Converte volume de cm³ para m³.

    pressures = {}                                    # Dicionário para armazenar as colunas de pressão.
    mask = np.isfinite(theta) & np.isfinite(V_m3)     # Máscara inicial: só aceita pontos em que theta e V sejam finitos.


    for c in pressure_cols:
        pbar = _to_numeric_series(df[c]).to_numpy()     # Lê cada coluna de pressão em bar.
        pressures[c] = pbar * 1e5                       #Converte bar para Pascal:1 bar = 100000 Pa = 1e5 Pa
        mask &= np.isfinite(pressures[c])               #Atualiza a máscara para manter apenas linhas válidas em todas as colunas necessárias.

    theta = theta[mask]
    V_m3 = V_m3[mask]                       # Aplica a máscara ao vetor de ângulo e volume.
    for c in pressure_cols:
        pressures[c] = pressures[c][mask]    # Aplica a mesma máscara a todas as pressões.

    idx = np.argsort(theta)                 # Obtém os índices que ordenam theta em ordem crescente.
    theta = theta[idx]                      # Reorganiza theta e volume em ordem crescente de ângulo.
    V_m3 = V_m3[idx]
    for c in pressure_cols:
        pressures[c] = pressures[c][idx]     # Reorganiza também as pressões na mesma ordem.

    style = {
        pressure_cols[0]: dict(color="blue",  linestyle="-", linewidth=2),
        pressure_cols[1]: dict(color="red",   linestyle="-", linewidth=2),
        pressure_cols[2]: dict(color="green", linestyle="-", linewidth=2),
        pressure_cols[3]: dict(color="blue",  linestyle=":", linewidth=2),
        pressure_cols[4]: dict(color="red",   linestyle=":", linewidth=2),
        pressure_cols[5]: dict(color="green", linestyle=":", linewidth=2),
    }

    results = {}
    P_for_plot_bar = {}

    fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # -------- HRR --------                                
    for c in pressure_cols:
        th, P_f, hrr = compute_hrr(
            theta, V_m3, pressures[c],
            gamma=gamma,
            filter_pressure=filter_pressure,
            bw_order=bw_order,
            cutoff_cyc_per_deg=cutoff_cyc_per_deg,
            baseline_window=baseline_window
        )
         # Calcula o HRR para cada caso.

        results[c] = {"theta": th, "hrr_J_per_deg": hrr}   # Salva os resultados em um dicionário.

        if pressure_use_filtered:                          # Se desejar, usa a pressão filtrada no gráfico.
            P_for_plot_bar[c] = P_f / 1e5
        else:
            P_for_plot_bar[c] = pressures[c] / 1e5       # Caso contrário, usa a pressão bruta original.Divide por 1e5 para voltar de Pa para bar.
         
        hrr_kw = hrr * (rpm * 6.0) / 1000.0
        axs[0].plot(th, hrr_kw, label=c, **style[c])
        # Converte HRR de J/deg para kW.
        #
        # A multiplicação por (rpm * 6.0) vem da conversão angular
        # para taxa temporal.
        # Depois divide por 1000 para passar de W para kW.


    axs[0].set_ylabel("HRR (kW)")
    axs[0].set_title("(a) Apparent Heat Release Rate")
    axs[0].grid(True)

    # -------- PRESSÃO --------
    if plot_pressure:                                         # Só plota pressão se o usuário desejar.
        for c in pressure_cols:
            axs[1].plot(theta, P_for_plot_bar[c], **style[c])

        axs[1].set_xlabel("θ (°CA)")
        axs[1].set_ylabel("Pressure (bar)")
        axs[1].set_title("(b) In-cylinder Pressure")
        axs[1].grid(True)

    if xlim is not None:
        axs[1].set_xlim(*xlim)

    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=3, frameon=False)

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    plt.show()

    # -------- RESUMO HRR --------
    print("\n=== HRR: resumo por caso ===")
    for c in pressure_cols:
        hrr = results[c]["hrr_J_per_deg"]
        peak_kw = np.nanmax(hrr) * (rpm * 6.0) / 1000.0
        print(f"{c:>20s} : {peak_kw:6.2f} kW")

    return results


# ================= EXECUÇÃO =================
if __name__ == "__main__":
    run_hrr_from_xlsx(
        xlsx_path = r"C:\Users\enggi\IA_CURSO\COMBUSTAO\dados_HRR.xlsx",
        sheet_name=0,
        gamma=1.28,
        rpm=2000.0,
        theta_col="Theta",
        vol_col="Volume (cm3)",
        pressure_cols=(
            "Methane_SA=22,5_IMEP=1,32",
            "Methane_SA=25_IMEP=1,40",
            "Methane_SA=27,5_IMEP=1,37",
            "Biogas_SA=22,5_IMEP=0,72",
            "Biogas_SA=25_IMEP=0,93",
            "Biogas_SA=27,5_IMEP=1,25",
        ),
        filter_pressure=True,
        bw_order=4,
        cutoff_cyc_per_deg=0.08,
        baseline_window=(-360, -220),
        xlim=(-60, 120),
        plot_pressure=True,
        pressure_use_filtered=False,
    )
