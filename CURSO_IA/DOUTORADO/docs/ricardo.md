# Inspecao de Features - results_hydrogen_v2.csv

> Documento gerado por `src/inspecionar_results_hydrogen_v2.py`. Etapa somente de
> leitura/documentacao: nenhuma limpeza definitiva ou selecao de features foi
> feita aqui. Serve de base para a proxima etapa de EDA.

## Arquivos verificados

- CSV: `dados_amostra/results_hydrogen_v2.csv` (usado nesta inspecao)
- XLSX: `dados_amostra/results_hydrogen_v2.xlsx` -> **NAO encontrado**
  (nenhuma alteracao foi feita nele; verificacao de celulas mescladas nao se
  aplica pois o arquivo nao existe na pasta)

## Estrutura do arquivo

- Linha 1: nomes das features
- Linha 2: unidades
- Linha 3 em diante: dados experimentais (83 linhas)
- Separador: `;` | Decimal: `,` | Encoding: UTF-8 com BOM

## Validacoes

| Verificacao | Resultado |
|---|---|
| Total de colunas | 260 |
| Total de linhas de dados | 83 |
| Nomes duplicados | 11 -> ['(dP/dCA)max', '(dP/dt)max', 'CA_(dP/dCA)max', 'Comb_Dur3', 'ECU_Lambda', 'MAPO', 'MP', 'Missfire', 'PTP', 'RI', 'SEPO'] |
| Colunas sem nome | 1 -> posicoes [16] |
| Unidades ausentes | 5 -> posicoes [1, 2, 3, 4, 16] |
| Colunas 100% vazias | 11 -> posicoes [16, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234] |

Observacao: nomes duplicados ocorrem porque o arquivo repete um bloco de
features "resumo" no inicio e depois apresenta a tabela completa de medicoes
(ideia ja documentada em `src/leitura_dados.py`). Unidades ausentes/marcadas
como `-` ou `[?]` foram mantidas exatamente como estao na fonte; nenhuma
unidade foi inferida ou inventada.

## Lista de features e unidades

| Posicao | Nome | Unidade | Tipo | Observacoes |
|---|---|---|---|---|
| 1 | Descrição | _(ausente)_ | text | sem unidade |
| 2 | MP | _(ausente)_ | int | nome duplicado, sem unidade |
| 3 | Knock | _(ausente)_ | int | sem unidade |
| 4 | Valido | _(ausente)_ | int | sem unidade |
| 5 | RC | - | float | - |
| 6 | Missfire | [%] | float | nome duplicado |
| 7 | ECU_Lambda | [-] | float | nome duplicado |
| 8 | Comb_Dur3 | [deg] | float | nome duplicado |
| 9 | CA_(dP/dCA)max | [deg aTDCf] | float | nome duplicado |
| 10 | (dP/dCA)max | [bar/deg] | float | nome duplicado |
| 11 | (dP/dt)max | [MPa/ms] | float | nome duplicado |
| 12 | SEPO | [bar².deg] | float | nome duplicado |
| 13 | RI | [MW/m²] | float | nome duplicado |
| 14 | PTP | [bar] | float | nome duplicado |
| 15 | MAPO | [bar] | float | nome duplicado |
| 16 | _(sem nome)_ | _(ausente)_ | vazio (sem dados) | sem nome, sem unidade, 100% vazia |
| 17 | MP | [-] | int | nome duplicado |
| 18 | Fuel1 | [-] | text | - |
| 19 | Fuel2 | [-] | int | - |
| 20 | n_m_BS | [1/min] | float | - |
| 21 | MFR_f1 | [g/s] | float | - |
| 22 | MFR_f1.1 | [kg/h] | float | - |
| 23 | p_a_ENV | [bar] | float | - |
| 24 | p_o_MOG | [bar] | float | - |
| 25 | T_a_ENV | [?] | float | - |
| 26 | T_a_INTM | [?] | float | - |
| 27 | T_a_EXHM | [?] | float | - |
| 28 | T_o_MOG | [?] | float | - |
| 29 | T_f_aHPP | [?] | float | - |
| 30 | T_w_bENG | [?] | float | - |
| 31 | T_w_aENG | [?] | float | - |
| 32 | h_a_ENV | [%] | float | - |
| 33 | h_a_TBR | [%] | int | - |
| 34 | ECU_n_m_BS | [1/min] | float | - |
| 35 | ECU_TPS | [%] | float | - |
| 36 | ECU_Lambda | [-] | float | nome duplicado |
| 37 | ECU_AINJ_f1 | [deg bTDCf] | int | - |
| 38 | ECU_TINJ_f1 | [ms] | float | - |
| 39 | ECU_AIGN | [deg bTDCf] | float | - |
| 40 | ECU_p_o_MOG | [bar] | float | - |
| 41 | cAHC | [ppm] | float | - |
| 42 | cBTOH | [ppm] | int | - |
| 43 | cC2H2 | [ppm] | float | - |
| 44 | cC2H4 | [ppm] | float | - |
| 45 | cC2H6 | [ppm] | float | - |
| 46 | cC3H6 | [ppm] | float | - |
| 47 | cC3H8 | [ppm] | int | - |
| 48 | cC4H6 | [ppm] | float | - |
| 49 | cCH4 | [ppm] | float | - |
| 50 | cCO | [ppm] | float | - |
| 51 | cCO2 | [ppm] | float | - |
| 52 | cCOS | [ppm] | float | - |
| 53 | cETOH | [ppm] | float | - |
| 54 | cH2O | [ppm] | float | - |
| 55 | cHCD | [ppm] | float | - |
| 56 | cHCE | [ppm] | float | - |
| 57 | cHCG | [ppm] | float | - |
| 58 | cHCHO | [ppm] | float | - |
| 59 | cHCN | [ppm] | int | - |
| 60 | cHCOOH | [ppm] | int | - |
| 61 | cHNCO | [ppm] | int | - |
| 62 | cIC5 | [ppm] | float | - |
| 63 | cIC8 | [ppm] | int | - |
| 64 | cMCOOH | [ppm] | int | - |
| 65 | cMECHO | [ppm] | float | - |
| 66 | cMEOH | [ppm] | int | - |
| 67 | cN2O | [ppm] | float | - |
| 68 | cNC5 | [ppm] | float | - |
| 69 | cNC8 | [ppm] | int | - |
| 70 | cNH3 | [ppm] | float | - |
| 71 | cNMHC | [ppm] | float | - |
| 72 | cNO | [ppm] | float | - |
| 73 | cNO2 | [ppm] | float | - |
| 74 | cNOX | [ppm] | float | - |
| 75 | SO2 | [ppm] | float | - |
| 76 | d_f1 | [kg/m3] | float | - |
| 77 | LHV_f1 | [MJ/kg] | int | - |
| 78 | AFR_f1 | [-] | float | - |
| 79 | M_f1 | [Atoms] | int | - |
| 80 | C_f1 | [Atoms] | int | - |
| 81 | H_f1 | [Atoms] | int | - |
| 82 | O_f1 | [Atoms] | int | - |
| 83 | N_f1 | [Atoms] | int | - |
| 84 | Working Cycle | [-] | text | - |
| 85 | NCYL | [-] | int | - |
| 86 | B | [mm] | int | - |
| 87 | I | [mm] | int | - |
| 88 | r | [mm] | float | - |
| 89 | rc | [-] | float | - |
| 90 | po | [mm] | int | - |
| 91 | co | [mm] | int | - |
| 92 | to | [mm] | int | - |
| 93 | IVO | [deg aTDCf] | int | - |
| 94 | IVC | [deg aTDCf] | int | - |
| 95 | IVL | [deg aTDCf] | int | - |
| 96 | EVO | [deg aTDCf] | int | - |
| 97 | EVC | [deg aTDCf] | int | - |
| 98 | EVL | [deg aTDCf] | int | - |
| 99 | Time | [-] | int | - |
| 100 | Operator Name | [-] | text | - |
| 101 | Wb | [J] | int | - |
| 102 | Wi | [J] | float | - |
| 103 | Wig | [J] | float | - |
| 104 | Wp | [J] | float | - |
| 105 | Wf | [J] | float | - |
| 106 | Qfuel | [J] | float | - |
| 107 | Qemiss | [J] | float | - |
| 108 | Qhr | [J] | float | - |
| 109 | Qht+exh | [J] | float | - |
| 110 | Qht | [J] | float | - |
| 111 | Qexh | [J] | float | - |
| 112 | Pb | [kW] | int | - |
| 113 | Pi | [kW] | float | - |
| 114 | Pig | [kW] | float | - |
| 115 | Pp | [kW] | float | - |
| 116 | Pf | [kW] | float | - |
| 117 | Pfuel | [kW] | float | - |
| 118 | Pemiss | [kW] | float | - |
| 119 | Phr | [kW] | float | - |
| 120 | Pht+exh | [kW] | float | - |
| 121 | Pht | [kW] | float | - |
| 122 | Pexh | [kW] | float | - |
| 123 | BMEP | [bar] | int | - |
| 124 | IMEPn | [bar] | float | - |
| 125 | IMEPg | [bar] | float | - |
| 126 | PMEP | [bar] | float | - |
| 127 | FMEP | [bar] | float | - |
| 128 | FuelMEP | [bar] | float | - |
| 129 | EmissMEP | [bar] | float | - |
| 130 | HrMEP | [bar] | float | - |
| 131 | HtExhMEP | [bar] | float | - |
| 132 | HtMEP | [bar] | float | - |
| 133 | ExhMEP | [bar] | float | - |
| 134 | Tb | [N.m] | int | - |
| 135 | Ti | [N.m] | float | - |
| 136 | Tig | [N.m] | float | - |
| 137 | bsfc | [g/kWh] | int | - |
| 138 | isfc | [g/kWh] | float | - |
| 139 | igsfc | [g/kWh] | float | - |
| 140 | SPb | [kW/L] | int | - |
| 141 | SPi | [kW/L] | float | - |
| 142 | SPig | [kW/L] | float | - |
| 143 | SPFb | [kW/m²] | int | - |
| 144 | SPFi | [kW/m²] | float | - |
| 145 | SPFig | [kW/m²] | float | - |
| 146 | SVb | [L/kW] | int | - |
| 147 | SVi | [L/kW] | float | - |
| 148 | SVig | [L/kW] | float | - |
| 149 | CoV_IMEPn | [%] | float | - |
| 150 | LNV_IMEPn | [-] | float | - |
| 151 | STD_IMEPn | [bar] | float | - |
| 152 | Var_IMEPn | [bar] | float | - |
| 153 | CoV_IMEPg | [%] | float | - |
| 154 | LNV_IMEPg | [-] | float | - |
| 155 | STD_IMEPg | [bar] | float | - |
| 156 | Var_IMEPg | [bar] | float | - |
| 157 | CoV_Pmax | [%] | float | - |
| 158 | LNV_Pmax | [-] | float | - |
| 159 | STD_Pmax | [bar] | float | - |
| 160 | Var_Pmax | [bar] | float | - |
| 161 | eff_v | [%] | float | - |
| 162 | eff_c | [%] | float | - |
| 163 | eff_tm | [%] | float | - |
| 164 | eff_ge | [%] | float | - |
| 165 | eff_m | [%] | int | - |
| 166 | eff_ig | [%] | float | - |
| 167 | eff_in | [%] | float | - |
| 168 | eff_b | [%] | int | - |
| 169 | eff_i | [%] | float | - |
| 170 | Pmax | [bar] | float | - |
| 171 | CA_Pmax | [deg aTDCf] | float | - |
| 172 | Tmax | [K] | float | - |
| 173 | CA_Tmax | [deg aTDCf] | float | - |
| 174 | Tumax | [K] | float | - |
| 175 | CA_Tumax | [deg aTDCf] | float | - |
| 176 | Tbmax | [K] | float | - |
| 177 | CA_Tbmax | [deg aTDCf] | float | - |
| 178 | Missfire | [%] | float | nome duplicado |
| 179 | AHR | [J] | float | - |
| 180 | AHRRmax | [J/deg] | float | - |
| 181 | CA_AHRRmax | [deg aTDCf] | float | - |
| 182 | (dAHRR/dCA)max | [J/deg²] | float | - |
| 183 | CA_(dAHRR/dCA)max | [deg aTDCf] | float | - |
| 184 | (d²AHRR/dCA²)max | [J/deg³] | float | - |
| 185 | CA_(d²AHRR/dCA²)max | [deg aTDCf] | float | - |
| 186 | SOC | [deg aTDCf] | float | - |
| 187 | CA01 | [deg aTDCf] | float | - |
| 188 | CA02 | [deg aTDCf] | float | - |
| 189 | CA05 | [deg aTDCf] | float | - |
| 190 | CA10 | [deg aTDCf] | float | - |
| 191 | CA45 | [deg aTDCf] | float | - |
| 192 | CA50 | [deg aTDCf] | float | - |
| 193 | CA55 | [deg aTDCf] | float | - |
| 194 | CA75 | [deg aTDCf] | float | - |
| 195 | CA90 | [deg aTDCf] | float | - |
| 196 | CA95 | [deg aTDCf] | float | - |
| 197 | CA98 | [deg aTDCf] | float | - |
| 198 | CA99 | [deg aTDCf] | float | - |
| 199 | EOC | [deg aTDCf] | float | - |
| 200 | ID_SI_t1 | [deg] | float | - |
| 201 | ID_SI_t2 | [deg] | float | - |
| 202 | ID_SI_t3 | [deg] | float | - |
| 203 | ID_SI_t4 | [deg] | float | - |
| 204 | ID_SI_t5 | [deg] | float | - |
| 205 | ID_DI1_t1 | [deg] | float | - |
| 206 | ID_DI1_t2 | [deg] | float | - |
| 207 | ID_DI1_t3 | [deg] | float | - |
| 208 | ID_DI1_t4 | [deg] | float | - |
| 209 | ID_DI1_t5 | [deg] | float | - |
| 210 | ID_DI2_t1 | [deg] | float | - |
| 211 | ID_DI2_t2 | [deg] | float | - |
| 212 | ID_DI2_t3 | [deg] | float | - |
| 213 | ID_DI2_t4 | [deg] | float | - |
| 214 | ID_DI2_t5 | [deg] | float | - |
| 215 | Comb_Dur1 | [deg] | float | - |
| 216 | Comb_Dur2 | [deg] | float | - |
| 217 | Comb_Dur3 | [deg] | float | nome duplicado |
| 218 | CA_(dP/dCA)max | [deg aTDCf] | float | nome duplicado |
| 219 | (dP/dCA)max | [bar/deg] | float | nome duplicado |
| 220 | (dP/dt)max | [MPa/ms] | float | nome duplicado |
| 221 | SEPO | [bar².deg] | float | nome duplicado |
| 222 | RI | [MW/m²] | float | nome duplicado |
| 223 | PTP | [bar] | float | nome duplicado |
| 224 | MAPO | [bar] | float | nome duplicado |
| 225 | IMPO | [bar.deg] | vazio (sem dados) | 100% vazia |
| 226 | AEPO | [bar] | vazio (sem dados) | 100% vazia |
| 227 | DKI | [-] | vazio (sem dados) | 100% vazia |
| 228 | AEFD | [kPa²/Hz] | vazio (sem dados) | 100% vazia |
| 229 | IMPG | [bar] | vazio (sem dados) | 100% vazia |
| 230 | MAHRO | [J/deg] | vazio (sem dados) | 100% vazia |
| 231 | SEHRO | [J²/deg] | vazio (sem dados) | 100% vazia |
| 232 | AEHRO | [J²/Hz] | vazio (sem dados) | 100% vazia |
| 233 | DMP | [bar/deg] | vazio (sem dados) | 100% vazia |
| 234 | CNL | [dB] | vazio (sem dados) | 100% vazia |
| 235 | CO10SEPO | [%] | float | - |
| 236 | CO100SEPO | [%] | float | - |
| 237 | CO8RI | [%] | float | - |
| 238 | CO10RI | [%] | float | - |
| 239 | CO5(dP/dt)max | [%] | float | - |
| 240 | CO10(dP/dCA)max | [%] | float | - |
| 241 | CO025PTP | [%] | float | - |
| 242 | CO05MAPO | [%] | float | - |
| 243 | a_sound | [m/s] | float | - |
| 244 | Cycle time | [ms] | float | - |
| 245 | EGR | [%] | float | - |
| 246 | m_f1 | [mg] | float | - |
| 247 | m_f2 | [mg] | int | - |
| 248 | m_a | [mg] | float | - |
| 249 | m_mix | [mg] | float | - |
| 250 | M_exh | [mol] | int | - |
| 251 | d_ai | [kg/m³] | float | - |
| 252 | MPS | [m/s] | float | - |
| 253 | MPA | [m/s²] | float | - |
| 254 | Leq | [mm] | float | - |
| 255 | rc_eff | [-] | float | - |
| 256 | Overlap | [deg] | int | - |
| 257 | Comp_Dur | [deg] | float | - |
| 258 | Exp_Dur | [deg] | float | - |
| 259 | CA_Vmax | [deg aTDCf] | int | - |
| 260 | CA_Vmin | [deg aTDCf] | float | - |

## Features selecionadas para o projeto

_(a preencher em etapa futura - nenhuma feature foi selecionada automaticamente)_
