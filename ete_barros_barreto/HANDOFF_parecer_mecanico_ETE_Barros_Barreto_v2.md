# HANDOFF: parecer técnico dos itens de engenharia mecânica
**Obra:** Requalificação e ampliação da ETE do Hospital Barros Barreto (Belém/PA) · **Orçamentista:** Sanigy Engenharia Sanitária · **Data-base:** 06/2025
**Arquivo gerado em:** 15/10/2026 · **Origem:** conversa anterior com Claude, resumida para ser retomada em outra conversa.
**Versão 2 (15/10/2026, sessão 2):** acrescenta a **seção 15** (guindaste, registros SEDOP, incêndio, comissionamento e lacunas de escopo, conferidos contra o SINAPI-PA 06/2025) e a **seção 16** (comparação item a item com o SINAPI-PA 09/2026), e atualiza as seções 5, 10, 11 e 12. Nas seções 1 a 9 e 12 a 14 só foi acrescentada uma nota no bloco B da seção 8 (guindaste). **Na sessão 2 a planilha do orçamento não foi anexada:** os valores do orçado usados na seção 15 vêm das seções 5 a 10.

---

## 0. Como usar este arquivo

1. Abra uma conversa nova e **anexe este arquivo**.
2. Anexe de novo os arquivos de origem (a conversa anterior os recebeu, a nova não os tem):
   - `ORÇAMENTO_ETE__BARROS_062025_VENTO_SUL.xlsx` (a planilha analisada);
   - `SINAPI_Referência_2025_06.xlsx`, `SINAPI_Manutenções_2025_06.xlsx`, `SINAPI_mao_de_obra_2025_06.xlsx`, `SINAPI_familias_e_coeficientes_2025_06.xlsx` (tabela da data-base);
   - opcional, só como comparação de inflação: os mesmos quatro arquivos de 09/2026.
3. Cole o **prompt da seção 1** e peça para continuar a partir das **pendências (seção 11)**.
4. Se a nova conversa não tiver os arquivos, tudo o que já foi apurado está nas seções 5 a 10 e pode ser usado como está. O que precisar de dado novo (tabelas SEDOP/ORSE/EMBASA, projeto, propostas) deve ser anexado.

---

## 1. Prompt de partida (copiar e colar)

```
Atue como engenheiro mecânico sênior, FISCAL TÉCNICO DA CONTRATANTE, responsável por dar o "de acordo"
nos itens de engenharia mecânica da aba "PLANILHA ORÇAMENTÁRIA" do orçamento da ETE do Hospital
Barros Barreto (Belém/PA), ANTES do início dos serviços.

Leia o arquivo HANDOFF anexo: ele traz todo o contexto, os critérios, os resultados já obtidos, as
correções que já fiz e as pendências. Não refaça o que já está feito. Continue a partir da seção 11
(Pendências). Mantenha o mesmo formato de status (OK / OK com ressalva / NÃO OK / NÃO VERIFICÁVEL).

Meu interesse central é responder, item a item: (1) o preço está ok? (2) o quantitativo está ok?
(3) está muito abaixo hoje (risco de prejuízo da contratada)? (4) está muito acima (lesa a
contratante)? E se o BDI aplicado (serviço ou aquisição) está correto.

Regras: separe fato verificado de hipótese; nunca invente preço, código, norma ou cláusula; se não
conseguir conferir, escreva "não verificável" e diga o que falta; ao pesquisar preço de mercado cite
fonte e data; não afirme adequação técnica de equipamento sem memorial ou projeto.
```

---

## 2. Papel, regras e entrega

**Papel:** fiscal técnico da contratante, dando o "de acordo" nos itens mecânicos (equipamentos, tubulações e acessórios, tanques em PRFV, içamento, comissionamento, proteção contra incêndio, elevatória).

**Foco do usuário:** a aba **PLANILHA ORÇAMENTÁRIA**. As demais abas servem só como evidência. As quatro perguntas centrais:
1. O preço do item está ok (contra a referência da data-base)?
2. O quantitativo está ok?
3. Está muito abaixo hoje (prejuízo da contratada)?
4. Está muito acima (lesa a contratante)?

**Critério importante (pergunta 3):** estar abaixo do preço de hoje só por causa da inflação desde 06/2025 **não é prejuízo**: isso se resolve com reajuste contratual (índice a confirmar no contrato). Prejuízo real é preço que já estava abaixo do custo **na data-base** (exemplo: guindaste e escada, que o SINAPI não precifica).

**Status usados:** OK · OK com ressalva · NÃO OK · NÃO VERIFICÁVEL.
**Testes por item:** P (preço), Q (quantidade), E (especificação e coerência com os itens vizinhos), B (BDI).

**Regras do pedido original:**
- Separar "fato verificado na planilha" de "hipótese a confirmar".
- Nunca inventar preço, código, norma ou cláusula; se não souber ou não conseguir conferir, escrever "não verificável" e dizer o que falta.
- Preço de mercado pesquisado na web: citar fonte e data.
- Não afirmar adequação técnica de equipamento sem memorial ou projeto.
- Normas a considerar, **com aplicabilidade ainda não confirmada com o usuário**: ABNT NBR 12209, 12208, 5580, 12693; NR-10, NR-12, NR-33, NR-35; Lei 14.133/2021 (art. 23, estimativa de valor; art. 41, marcas); Decreto 7.983/2013 se houver recursos federais.

**Formato final de entrega (quando o usuário pedir, em .xlsx ou Word):**
1. Parecer por item em tabela: código, descrição, situação, motivo, evidência (aba e célula), impacto estimado em R$ com BDI, ação recomendada.
2. Resumo executivo: o que aprovar, o que condicionar, o que não aprovar.
3. Pendências para o orçamentista e para o projetista.
4. Documentos que faltam.

**Etapas do roteiro original ainda NÃO feitas:** Etapa 6 (lacunas de escopo: montagem, partida, quadros de comando dos motores, bases, inoculação, recirculação de lodo, etc., sempre "a confirmar") e Etapa 7 (conformidade normativa, depois de confirmar a aplicabilidade das normas com o usuário).

---

## 3. O orçamento (fatos verificados na planilha)

| Parâmetro | Valor |
|---|---|
| Valor total | R$ 2.343.873,57 (16 grupos) |
| Data-base | 01/06/2025 (aba PLANILHA ORÇAMENTÁRIA, célula C6) |
| Bancos | SINAPI 06/2025 (Pará), ORSE 06/2025 (**Sergipe**), SEDOP **02/2025** (Pará), EMBASA 06/2025 (**Bahia**), SICRO3 (sem data no cabeçalho) |
| Encargos | Desonerado |
| BDI de serviço | 27,41% (fator M7 = 1,2741) |
| BDI de aquisição ("material") | 16,08% (fator M3 = 1,1608) |
| Prazo | Cronograma físico-financeiro de **6 meses**; administração local (itens 2.1 a 2.6) orçada com **7 meses** |
| Regime de execução, edital, contrato | Não constam; **não verificável** |

**Como a aba PLANILHA ORÇAMENTÁRIA calcula (colunas, linhas 15 a 306):**
- A = item · B = fonte · C = código · D = descrição · E = unidade · F = quantidade (digitada).
- **L = custo sem BDI**, via `PROCV(A; basenova; 7; FALSO)`. O nome `basenova` aponta para `PL_Base_062025!$B$6:$K$298` (aba **oculta**).
- **G = preço unitário com BDI** = `TRUNC(L × M$7 ou M$3; 2)`. **H = total** = `TRUNC(F × G; 2)`.
- Consequência: **a correção de preço deve ser feita na base (PL_Base_062025)**, senão a fórmula sobrescreve a aba visível. A base tem BDI zero, então o BDI é aplicado uma única vez.
- A quantidade da aba visível pode divergir da base. Exemplos: 1.1 (45 contra 40), 1.4 (218,02 contra 120) e **12.3.6 (2 na visível, 1 na base)**.

**Abas (todas conferidas):**
- Visíveis: RESUMO, PLANILHA ORÇAMENTÁRIA, CPUs_062025 (composições analíticas), CRONOGRAMA, COTAÇÕES INICIAL (38 imagens: prints de loja e propostas), Compos. Própias INCIAL (versão antiga das composições próprias), Compos. BDI AQUISIÇÃO, Compos. BDI, Compos. Enc. Sociais.
- **Ocultas:** `Orçamento - SINAPI` (versão antiga, total R$ 1.489.434,21; aplicava BDI de aquisição a todos os itens de cotação), `PL_Base_062025`, `CURVA ABC` (datada de 23/02/2026, com preços diferentes dos atuais), `M. CAL. ESTRUTURAL`, `ESCLARECIMENTO DAS COMPOSIÇÕES` (justificativa de não apresentar as composições oficiais).

---

## 4. Escopo mecânico adotado (80 itens, R$ 778.719,20, cerca de 33% da obra)

| Grupo | Itens |
|---|---|
| Comissionamento | 1.13, 1.16 |
| Içamento | 6.1, 6.2 |
| Rede PVC "água fria" | 8.2.1 a 8.2.26 |
| Rede aço galvanizado | 8.3.1 a 8.3.9 |
| Equipamentos e válvulas | 10.1 a 10.17 |
| PRFV (UASB, FBAS, tanque de contato, decantador) | 12.1.1 a 12.1.7, 12.2.1 a 12.2.5, 12.3.1 a 12.3.6, 12.4.1, 12.4.2 |
| Incêndio | 13.1 a 13.4 |

**Itens de fronteira, ainda SEM decisão do usuário (fora da análise até decidir):**
- 8.1.1 a 8.1.11, esgoto PVC (R$ 16.242,87).
- 6.4 escada marinheiro e 6.5 guarda-corpo (R$ 85.049,55). A 6.4 não tem custo oficial (escada com preço zero). A 6.5 usa o código SINAPI 99837, **desativado em 10/2025**.
- 7.5 pintura de tubo + 1.7 remoção de tubulações (R$ 10.384,50).
- 1.8 esgotamento com bomba (R$ 4.514,40).
- Grupo 11 (elevatória existente): é todo civil, sem item mecânico.

---

## 5. Conferência de preços contra o SINAPI-PA 06/2025 (desonerado)

Foram cruzados os 149 itens SINAPI da planilha com a tabela da data-base.

| Resultado | Itens |
|---|---|
| Preço **igual à tabela, ao centavo** | 117 (R$ 664.790,93 c/ BDI) |
| Preço diferente | 2 (itens 2.3 e 2.5, fora do escopo mecânico) |
| **Tabela não traz custo** para o código | 30 |

- **Escopo mecânico com preço conferido: 36 itens, R$ 78.535,94 c/ BDI:** 8.2.x (24 itens, exceto 8.2.19 e 8.2.24), 8.3.1, 8.3.4 a 8.3.7, 8.3.9, 10.12, 10.13, 10.15, 10.16, 10.17 e 13.2.
- **50 linhas SINAPI de mão de obra e insumos** dentro das composições próprias do escopo mecânico foram conferidas: **nenhuma diverge** da tabela.
- **Sem custo oficial no escopo mecânico (R$ 57.013,76 c/ BDI): 6.1 e 6.2 (guindaste, R$ 47.892,00), 6.4 (escada, R$ 8.946,00) e 11.5 (escada, R$ 175,76).** Os códigos 102850 e 102851 foram criados em 11/2021 como "composição sem custo" e nunca tiveram custo divulgado. A composição da planilha zera depreciação, juros e manutenção; o R$ 98,78/h é só materiais na operação (R$ 69,85) mais operador (R$ 28,93).
- **8.2.24 (bucha DN 32×25):** a planilha usa composição própria a R$ 101,40 (sem BDI), com insumo de bucha DN 110 da ORSE. A descrição é a da composição SINAPI **103953**, que custa **R$ 7,62** na tabela de 06/2025.
- **8.3.2:** o orçado fica em R$ 145/m, enquanto os SINAPI equivalentes de 4" custam R$ 194 a R$ 209/m (valor irrelevante, 1 vara).
- **Encargos:** SINAPI-PA 06/2025 desonerado: horista **95,00%** e mensalista **53,45%**. A aba "Compos. Enc. Sociais" mostra 89,42% e 49,63%, "fonte SINAPI-Pará". Os preços da planilha seguem a tabela; a aba é que está inconsistente. *Hipótese:* os 95,00% incluem o INSS de 5% da transição de 2025.
- **Itens fora do escopo, para o fiscal responsável:** 2.3 e 2.5 estão R$ 1.178,16/mês acima da tabela (cerca de R$ 21 mil c/ BDI em 7 meses); 26 composições (elétrica, lógica e SPDA) sem custo oficial (R$ 23.596,79), das quais 4 códigos foram **criados em 07/2025**, depois da data-base (106024, 106025, 106027, 106031).
- **Referência de inflação (refeita na sessão 2, seção 16):** nos 36 itens SINAPI do escopo mecânico, o SINAPI-PA 09/2026 vai de **−19,8% a +22,1%** por item em relação a 06/2025; no conjunto, **+6,46%**. Válvulas de bronze ≈ +14%, conexões galvanizadas ≈ +11,5%, PVC de 60 a 110 mm +4% a +6%; tubos e joelhos de 20 e 25 mm e a placa 13.2 **caíram**. Para comparação, o IBGE dá 6,81% em 12 meses até 09/2026.

---

## 6. BDI (conferência de equipamento × serviço)

**Fórmula (TCU, Acórdão 2622/2013):** BDI = [(1+AC+S+R+G) × (1+DF) × (1+L) / (1−I)] − 1. As abas "Compos. BDI" (C24) e "Compos. BDI AQUISIÇÃO" (C20) usam essa fórmula corretamente.

| | AC | SG | R | DF | L | I (PIS + COFINS + ISS + CPRB) | BDI |
|---|---|---|---|---|---|---|---|
| **Serviço** | 3,4% | 0,4% | 0,97% | 0,59% | 5% | 13,15% (0,65 + 3 + 5 + **4,5**) | **27,41%** |
| **Aquisição** | **0** | 0,4% | **0** | 0,59% | 5% | 8,65% (0,65 + 3 + **5** + 0) | **16,08%** |

**Faixas de referência do TCU (Acórdão 2622/2013), conferidas em transcrições; confirmar no texto oficial antes de citar no parecer:**
- Redes de água e esgoto e correlatas (inclui ETE): 1º quartil 20,76% · médio 24,18% · 3º quartil **26,44%**.
- Mero fornecimento de materiais e equipamentos: 11,10% · 14,02% · **16,80%**. Administração central nessa faixa: 1,50% · 3,45% · 4,49%.
- Acima do 3º quartil exige justificativa técnica. O BDI diferenciado vale para **mero fornecimento de materiais e equipamentos relevantes e de natureza específica**, não para insumos consumidos na execução (Súmula TCU 253 consolida a regra).

**Achados:**
1. **Serviço 27,41% está acima do 3º quartil (26,44%)** por causa do CPRB de 4,5%. Em 2025 a Lei 14.973/2024 prevê CPRB de 3,6% (80%) mais 5% de INSS sobre a folha; em 2026, 2,7% e 10%. Com CPRB de 3,6%, o BDI fica em **26,11%** (dentro da faixa); com 2,7%, em 24,83%. **Regime e alíquota a confirmar no edital e no contrato.** Efeito estimado nos itens mecânicos que ficam em serviço (depois da reclassificação): **cerca de −R$ 3,6 mil**.
2. **Aquisição 16,08% está dentro da faixa** (11,10 a 16,80), mas a composição zera AC e Risco e embute ISS de 5%. Sem o ISS, o BDI seria **10,06%**. A incidência de ISS sobre fornecimento de mercadoria (normalmente ICMS) é questão tributária: **a confirmar**.
3. **Classificação por item (critério: aquisição = equipamento ou material comprado pronto; serviço = instalação, montagem ou execução em campo):**

| Itens | Aplicado | Correto | Status | Δ BDI c/ BDI |
|---|---|---|---|---|
| 1.13, 1.16, 6.1, 6.2, 8.2.x, 8.3.1, 8.3.4 a 8.3.9, 13.1, 13.3 | Serviço | Serviço | OK | — |
| 8.3.2, 10.1 a 10.8, 10.14 | Aquisição | Aquisição | OK (mão de obra incluída ≤ 4%; difusor 14%, cerca de R$ 400) | — |
| 10.9 a 10.13, 10.15 a 10.17 (registros e retenções) | Serviço | critério misto | OK com ressalva (equivalentes ao 10.14, que está em aquisição) | −1.670,23 se migrassem (fora do total abaixo) |
| **12.4.1** decantador | Serviço | **Aquisição** | NÃO OK | **−17.932,38** |
| 12.1.1 separador, 12.1.2 defletor, 12.3.1 kit chincana | Serviço | **Aquisição** | NÃO OK | −2.301,98 / −2.151,88 / −734,88 |
| Fretes 12.1.7, 12.2.5, 12.3.6, 12.4.2 | Serviço | **Aquisição** (seguem o item) | NÃO OK | −169,95 / −169,95 / −169,95 (qtd 1) / −1.246,30 |
| 12.1.3 a 12.1.6, 12.2.1 a 12.2.4, 12.3.2 a 12.3.5 (revestimento, gelcoat, acessos, montagem) | Serviço | Serviço | OK (execução em campo) | — |
| 13.2 (placa, só material), 13.4 (extintor) | Serviço | Aquisição | NÃO OK | −7,29 / −71,40 |
| **Total dos itens firmes** | | | | **−24.955,96** |

- Se todo o grupo 12 voltasse para aquisição (como na versão oculta antiga), seria −R$ 43.876,26. **Não recomendado**: montagem, revestimento e gelcoat são serviço.
- Para sustentar o BDI reduzido, a proposta da Biomais precisa vir **desmembrada em fornecimento e montagem**.

---

## 7. Pesquisa de mercado (consulta em 15/10/2026; preços de varejo ou anúncio)

| Item | Orçado (insumo, sem BDI) | Mercado encontrado | Leitura |
|---|---|---|---|
| 10.1 Calha Parshall 6" PRFV | R$ 5.883,02 (print Bakof, **com caixas de entrada e saída**) | Calha só: R$ 2.200 (Sanecom, Mercado Livre) a R$ 3.200 (ECR) | OK se o projeto pedir as caixas; senão, até ≈ R$ 3,1 mil c/ BDI acima |
| 10.3 Soprador | R$ 10.567,90 (print Policomp JQT-7500, 8,6 kW) | Compressor radial duplo estágio 11,53 cv (8,6 kW) novo: R$ 13.600 (OLX/compmaq). Asten CRC-2 820 36 TD HE: 12,6 kW (16,9 cv), vazão máx 10,33 m³/min (≈ 620 m³/h), pressão máx 4.700 mmCA a 60 Hz | Especificação em 3 versões; NÃO VERIFICÁVEL |
| 10.4 Difusor 250 mm | R$ 161,20 | R$ 119,90 (270 mm, Era Ambiental) a R$ 189,00 (250 mm, Altamar) | OK |
| 10.7 Motobomba Brava E30 3 cv | R$ 5.679,24 | R$ 4.201,00 a R$ 6.590,00 (várias lojas); recalque 3", sólidos 25 mm, até 43,6 m³/h | OK |
| 10.8 Pall ring | R$ 1.180,00/m³ ("2"") | R$ 1.180,00/m³ para anel PP de **3"** (biodigestornaweb) | OK com ressalva (2" × 3") |
| 13.4 Extintor ABC 6 kg | R$ 199,99 | R$ 191,50 (GOINFRA 02/2026); R$ 226,94 (composição ORSE-1511) | OK; trocar a cotação pela ORSE |
| 10.2, 10.6, 10.14 (dosadora EMEC FCE, manômetro, válvula de alívio) | R$ 1.367,90 / R$ 168,23 / R$ 941,05 | Sem preço público confiável | NÃO VERIFICÁVEL; pedir 3 propostas |
| Grupo 12 (PRFV, R$ 493 mil) | Proposta única Biomais | Produto sob encomenda, sem preço público | NÃO VERIFICÁVEL; pedir mais propostas |

**Cotação da Biomais:** datada de 24/07/2025 (depois da data-base), apenas a página 4 está na planilha, sem CNPJ, validade ou especificação. Total da proposta R$ 385.757,18; a soma do grupo 12 na planilha (sem BDI) dá R$ 387.257,18. **A diferença de R$ 1.500,00 é exatamente o frete duplicado no 12.3.6.**

---

## 8. Achados por bloco (verificação item a item)

**Bloco A, comissionamento**
- **1.13** (linha 28, R$ 25.370,35): composição EMBASA 41.05.01 (tabela da **Bahia**, pedir tabela e justificativa). Inclui 40 h de caminhão jato/vácuo (R$ 239,18/h), 20 h de guindaste de 12 t e mão de obra: conferir se o serviço existe no projeto e se repete o 6.1/6.2. Texto duplicado em D28. **NÃO VERIFICÁVEL.**
- **1.16** (linha 31, R$ 8.043,13): comissiona 3 extintores e placas (grupo 13 inteiro = R$ 1.223,19). Cobra 40 h de engenheiro júnior (R$ 118,33/h), que já está pago no 2.1, mais 20 h de auxiliar e 40 h de encanador. **NÃO OK:** excluir ou reduzir a inspeção com relatório.

**Bloco B, içamento**
- **6.1 e 6.2** (linhas 69 e 70, R$ 47.892,00): sem custo oficial; 240 CHP + 480 CHI de guindaste de 75 t sobre esteiras; pagamento espalhado por 6 meses no cronograma, mas as peças do grupo 12 concentram nos meses 2 e 3. Exigir **plano de içamento com peso das peças**. Referências com custo publicado em 09/2026 (não é a data-base): guindaste hidráulico de 30 t (SINAPI 89272, R$ 230,04/h produtiva) e guindauto de 14,3 t (106251, R$ 373,13/h). **NÃO OK.** *(Sessão 2: na data-base 06/2025 o 89272 custa R$ 220,46/h e o 106251 ainda não existe; ver seção 15.1.)*

**Bloco C, rede PVC (8.2.1 a 8.2.26): preço OK nos itens SINAPI**
- Tubos: 8.2.1 (DN 20, 1 m), 8.2.2 (DN 25, 34 m), 8.2.3 (DN 60, 67 m), 8.2.4 (DN 75, 53 m), 8.2.5 (DN 85, 1 m), 8.2.6 (DN 110, 39 m). **Não há tubo DN 50**, apesar de 140 tês 75×50 e 140 buchas 50×25. Itens de 1 m (8.2.1 e 8.2.5) parecem resíduos.
- Cadeia dos difusores: 8.2.13, 8.2.14, 8.2.20 e 8.2.25 têm 140 unidades cada, igual ao 10.4 (coerente). *Hipótese:* 140 tês em 53 m de DN 75 dão cerca de 2,6 saídas por metro: conferir o espaçamento no isométrico.
- Linha DN 110: joelho ×11, curva ×4, tê ×3, luva ×2, união ×8 (8.2.19), adaptador com flanges livres ×14 (8.2.23). Os **14 flanges fecham com 2 × (3 registros de gaveta + 4 retenções)**. Mas as válvulas de bronze 10.15 a 10.17 são **roscáveis**: *hipótese* de incompatibilidade com flange livre; confirmar o tipo de conexão.
- 8.2.19: união DN 110 a R$ 608,93 c/ BDI (4× a luva); marca "TIGRE" na descrição (art. 41 da Lei 14.133, a confirmar); por que 8?
- Distribuição: tê 60 ×7 contra **21 registros DN 60** (10.11 + 10.13); joelho 60 ×34; joelho 75 ×24; tê 75 ×22.
- *Hipótese:* temperatura do ar na saída do soprador contra o limite do PVC soldável (cerca de 60 °C).
- **8.2.24:** NÃO OK (ver seção 5); não há tubo de 32 mm em nenhum item.

**Bloco D, aço galvanizado (8.3.1 a 8.3.9)**
- **8.3.1** tubo DN 80 (3") ×34 m, mas **todas as conexões e válvulas são 2½"** (cotovelos, luvas, niples, uniões, tê, filtro, registro, retenção). Se o tubo for 2½" (SINAPI 94463, R$ 118,45/m contra R$ 155,65/m do DN 80), diferença de cerca de R$ 1,3 mil sem BDI (≈ R$ 1,6 mil c/ BDI). **NÃO OK (incoerência).**
- 8.3.2: vara de 6 m ("DN 110", mas é 4"), nenhuma conexão de 4"; onde entra?
- 8.3.3 (bucha 1¼×½ ×2) e 8.3.8 (tê 2½×1¼ ×4): coerentes com 2 manômetros + 2 válvulas de alívio. 8.3.7 (20 niples) com 8.3.9 (10 uniões): 2 por união.

**Bloco E, equipamentos (10.1 a 10.17)**
- 10.1 calha: ver seção 7. 10.2 dosadora: qual produto químico e vazão?
- **10.3 soprador:** item "CRC 2820" (Asten), composição "16/18 cv", print de 8,6 kW. O print e o CRC-2 820 36 TD HE têm vazão máxima parecida (≈ 620 m³/h) e pressão máxima parecida (40 a 47 kPa); o que muda é a potência. O **ponto de operação do projeto** decide. 2 unidades: uma de reserva?
- **Dimensionamento indicativo (hipótese):** 140 difusores × 3 a 4 m³/h = 420 a 560 m³/h, compatível com um soprador de 620 m³/h.
- **10.5 filtro:** item "7AS5 194 2½"", mas o insumo cotado é filtro de 2" para até 5 m³/min, e o soprador chega a cerca de 10 m³/min. **NÃO OK.**
- 10.6 manômetro: conferir a faixa (soprador chega a cerca de 0,45 bar).
- 10.7 motobomba ×2: qual a função e o ponto (vazão e altura)? A elevatória do grupo 11 não tem bomba.
- 10.8 pall ring ×15 m³: 2" contra 3"; volume dos leitos do projeto.
- 10.9 e 10.10: registro de gaveta (SEDOP, 02/2025); flange ou rosca?
- **10.11 e 10.13:** mesmo código SINAPI 94493 (8 + 13 = 21). O 10.11 aparece como "COMPOSIÇÃO 8" na planilha, mas a CPU usa o SINAPI 94493. Confirmar quantos no projeto.
- 10.12 (registro DN 20 ×2): onde entram, se só há 1 m de tubo DN 20?
- **10.14 válvula de alívio "2BX4 140" 1¼":** *hipótese:* se "140" for psi (≈ 9,7 bar), não protege um soprador de ≈ 0,45 bar; confirmar a pressão de abertura.
- 10.15 (retenção 2½" ×2, uma por soprador); 10.16 e 10.17 (retenções 4": 2 horizontais + 2 verticais para 2 bombas; os 14 flanges só fecham com as 4).

**Bloco F, PRFV (12.1.1 a 12.4.2)**
- Perguntar quais unidades são novas e quais existentes ("revestimento e reforço interno" e "substituição do acesso" sugerem reforma).
- "Montagem do sistema (matéria-prima e mão de obra)" pode repetir o revestimento. Pedir o escopo detalhado de cada linha à Biomais.
- Revestimento por unidade: UASB R$ 16.804,69 (12.1.3), FBAS R$ 14.788,13 (12.2.1), tanque de contato R$ 8.066,25 (12.3.2): conferir a base de cálculo (m² de laminado).
- Fretes: 12.1.7 qtd 1, 12.2.5 qtd 1, **12.3.6 qtd 2 (proposta: 1)**, 12.4.2 qtd 2 (proposta: 2). A base (PL_Base) também tem 1 para o 12.3.6.
- Decantador 4,00 m × 4,10 m ×2: peso e fundação (grupo 5) compatíveis.
- Exigir **no mínimo mais duas propostas**.

**Bloco G, incêndio (13.1 a 13.4)**
- 13.1 e 13.3 (ORSE, sem a tabela); 13.2 (SINAPI 37556, só insumo, sem instalação, com BDI de serviço); 13.4 (extintor, 3 unidades, igual aos 3 suportes): quantidade a conferir com a norma e o CBM-PA. 13.4 NÃO OK só por BDI.

---

## 9. Curva ABC corrigida (valor c/ BDI, coluna H)

**Critério:** classe A até 80% do valor acumulado (inclui o item que cruza 80%), B até 95%, C o restante.
**Regra de agrupamento (análise, não medição):** soma as linhas da planilha que são o **mesmo objeto de custo**: (1) frete exclusivo de um único bem (decantador + frete); (2) mesmo equipamento dividido em hora produtiva e improdutiva (guindaste); (3) mesmo código em duas linhas (registro DN 60). **Não agrupa** acessórios que são bens físicos diferentes nem fretes de conjunto (UASB, FBAS e tanque de contato).
**Legenda:** S = BDI de serviço (27,41%); A = BDI de aquisição (16,08%); **S → A** = deveria usar aquisição. "Linha" = número da linha na aba PLANILHA ORÇAMENTÁRIA. Δ BDI = efeito de aplicar o BDI correto (12.3.6 usa quantidade 1).

### Resumo por classe

| Classe | Linhas | Valor (R$) | % | Δ BDI (R$) |
|---|---|---|---|---|
| **A** | 19 | 631.986,26 | 81,2% | −23.632,54 |
| **B** | 20 | 109.648,24 | 14,1% | −904,83 |
| **C** | 38 | 37.084,70 | 4,8% | −418,59 |
| **Total** | 77 | 778.719,20 | 100% | **−24.955,96** |

### Classe A (até 80% do valor acumulado)

| # | Item | Linha | Descrição | Qtd | R$ c/ BDI | % acum. | BDI | Δ BDI (R$) | Verificar (bloco) e status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 12.4.1 + 12.4.2 | 255 e 256 | Decantador secundário 4,00 × 4,10 m + frete | 2 + 2 | 215.671,40 | 27,7 | **S → A** | −19.178,68 | F: proposta única; comparar preço posto-obra; peso e fundação; BDI → aquisição (equipamento −R$ 17.932,38; frete −R$ 1.246,30) |
| 2 | 6.1 + 6.2 | 69 e 70 | Guindaste 75 t (horas produtivas + improdutivas) | 240 h + 480 h | 47.892,00 | 33,8 | S | — | B: NÃO OK; sem custo oficial no SINAPI; exigir plano de içamento |
| 3 | 12.1.3 | 236 | Revestimento e reforço interno (UASB) | 2 | 33.609,38 | 38,2 | S | — | F: unidade nova ou existente? base em m² |
| 4 | 10.4 | 208 | Difusor 250 mm | 140 | 30.354,80 | 42,1 | A | — | E: preço OK; 140 fecha com a rede |
| 5 | 12.1.6 | 239 | Montagem do sistema (UASB) | 2 | 29.576,26 | 45,9 | S | — | F: pode repetir o revestimento |
| 6 | 12.2.1 | 242 | Revestimento e reforço interno (FBAS) | 2 | 29.576,26 | 49,7 | S | — | F: base de cálculo vs 12.1.3 |
| 7 | 12.1.1 | 234 | Separador trifásico | 2 | 25.886,62 | 53,0 | **S → A** | −2.301,98 | F: escopo da proposta; BDI → aquisição |
| 8 | 1.13 | 28 | Comissionamento da ETE (EMBASA) | 1 | 25.370,35 | 56,2 | S | — | A: NÃO VERIFICÁVEL; EMBASA/BA; sobreposição com guindaste |
| 9 | 10.3 | 207 | Soprador radial duplo estágio | 2 | 24.987,56 | 59,4 | A | — | E: NÃO VERIFICÁVEL; especificação em 3 versões |
| 10 | 12.1.2 | 235 | Defletor em PRFV | 2 | 24.198,74 | 62,6 | **S → A** | −2.151,88 | F: escopo da proposta; BDI → aquisição |
| 11 | 12.2.4 | 245 | Montagem do sistema (FBAS) | 2 | 24.198,74 | 65,7 | S | — | F: pode repetir o revestimento |
| 12 | 10.8 | 212 | Pall ring 2" | 15 m³ | 21.270,15 | 68,4 | A | — | E: OK com ressalva; 2" × 3"; conferir volume |
| 13 | 12.1.5 | 238 | Substituição do acesso lateral e superior (UASB) | 2 | 17.476,88 | 70,6 | S | — | F: reforma de unidade existente? |
| 14 | 12.1.4 | 237 | Pintura com gelcoat (UASB) | 2 | 16.132,50 | 72,7 | S | — | F: escopo da proposta |
| 15 | 12.3.2 | 249 | Revestimento e reforço interno (tanque de contato) | 2 | 16.132,50 | 74,8 | S | — | F: base de cálculo |
| 16 | 12.3.5 | 252 | Montagem do sistema (tanque de contato) | 2 | 13.443,74 | 76,5 | S | — | F: pode repetir o revestimento |
| 17 | 8.2.14 | 108 | Tê de redução 75 × 50 | 140 | 13.400,80 | 78,2 | S | — | C: 140 = difusores; sem tubo DN 50; ≈ 2,6 saídas/m |
| 18 | 10.7 | 211 | Motobomba submersível Brava E30 | 2 | 13.396,96 | 79,9 | A | — | E: preço OK; função e ponto de operação |
| 19 | 12.2.2 | 243 | Pintura com gelcoat (FBAS) | 2 | 9.410,62 | 81,2 | S | — | F: escopo da proposta |

### Classe B (80% a 95%)

| # | Item | Linha | Descrição | Qtd | R$ c/ BDI | % acum. | BDI | Δ BDI (R$) | Verificar (bloco) e status |
|---|---|---|---|---|---|---|---|---|---|
| 20 | 12.2.3 | 244 | Substituição do acesso superior (FBAS) | 2 | 8.738,44 | 82,3 | S | — | F: escopo da proposta |
| 21 | 12.3.4 | 251 | Substituição do acesso superior (tanque de contato) | 2 | 8.738,44 | 83,4 | S | — | F: escopo da proposta |
| 22 | 12.3.1 | 248 | Kit chincana | 2 | 8.263,86 | 84,5 | **S → A** | −734,88 | F: fornecimento sem montagem; BDI → aquisição |
| 23 | 1.16 | 31 | Comissionamento do combate a incêndio | 1 | 8.043,13 | 85,5 | S | — | A: NÃO OK; excluir ou reduzir |
| 24 | 10.10 | 214 | Registro de gaveta 4" | 3 | 7.719,81 | 86,5 | S | — | E: SEDOP, NÃO VERIFICÁVEL; flange ou rosca? |
| 25 | 8.2.6 | 100 | Tubo PVC DN 110 | 39 m | 6.998,55 | 87,4 | S | — | C: preço OK; temperatura do ar × PVC |
| 26 | 10.1 | 205 | Calha Parshall 6" | 1 | 6.902,11 | 88,3 | A | — | E: OK com ressalva; cotação inclui caixas |
| 27 | 8.3.1 | 122 | Tubo aço galvanizado DN 80 | 34 m | 6.742,54 | 89,1 | S | — | D: NÃO OK; conexões são 2½" |
| 28 | 8.2.23 | 117 | Adaptador com flanges DN 110 × 4" | 14 | 6.191,78 | 89,9 | S | — | C: 14 = 2×(3+4) coerente; tipo de conexão |
| 29 | 8.2.19 | 113 | União PVC DN 110 (Tigre) | 8 | 4.871,44 | 90,6 | S | — | C: por que 8? marca Tigre |
| 30 | 12.3.3 | 250 | Pintura com gelcoat (tanque de contato) | 2 | 4.705,30 | 91,2 | S | — | F: escopo da proposta |
| 31 | 10.5 | 209 | Filtro de entrada | 2 | 4.132,98 | 91,7 | A | — | E: NÃO OK; filtro 2" × soprador |
| 32 | 8.2.11 | 105 | Joelho 90° DN 110 | 11 | 4.084,19 | 92,2 | S | — | C: conferir no isométrico |
| 33 | 12.3.6 | 253 | Frete do conjunto tanque de contato | 2 | 3.822,30 | 92,7 | **S → A** | −169,95 | F: NÃO OK; qtd 2 × proposta 1 (−R$ 1.911,15, à parte); BDI → aquisição |
| 34 | 8.2.4 | 98 | Tubo PVC DN 75 | 53 m | 3.818,65 | 93,2 | S | — | C: comprimento × planta |
| 35 | 8.2.10 | 104 | Joelho 90° DN 75 | 24 | 3.658,08 | 93,7 | S | — | C: conferir no isométrico |
| 36 | 10.2 | 206 | Bomba dosadora EMEC FCE | 2 | 3.299,14 | 94,1 | A | — | E: NÃO VERIFICÁVEL; pedir 3 propostas |
| 37 | 10.16 | 220 | Retenção horizontal 4" | 2 | 3.144,44 | 94,5 | S | — | E: preço OK; 4 retenções p/ 2 bombas |
| 38 | 8.2.3 | 97 | Tubo PVC DN 60 | 67 m | 2.957,38 | 94,9 | S | — | C: 7 tês × 21 registros DN 60 |
| 39 | 10.11 + 10.13 | 215 e 217 | Registro de esfera DN 60 (mesmo código SINAPI 94493) | 8 + 13 | 2.815,68 | 95,2 | S | — | E: NÃO OK; duplicidade; são 21 no projeto? (−R$ 1.072,64 se 8 sobrarem) |

### Classe C (95% a 100%)

| # | Item | Linha | Descrição | Qtd | R$ c/ BDI | % acum. | BDI | Δ BDI (R$) | Verificar (bloco) e status |
|---|---|---|---|---|---|---|---|---|---|
| 40 | 8.2.16 | 110 | Tê PVC DN 75 | 22 | 2.742,08 | 95,6 | S | — | C: conferir no isométrico |
| 41 | 8.3.9 | 130 | União galvanizada 2½" | 10 | 2.719,50 | 95,9 | S | — | D: coerente com 20 niples |
| 42 | 8.2.25 | 119 | Bucha de redução 50 × 25 | 140 | 2.402,40 | 96,2 | S | — | C: = difusores |
| 43 | 8.2.13 | 107 | Luva com bucha de latão 25 × ¾" | 140 | 2.377,20 | 96,6 | S | — | C: = difusores |
| 44 | 10.14 | 218 | Válvula de alívio 1¼" | 2 | 2.248,88 | 96,8 | A | — | E: NÃO VERIFICÁVEL; pressão de abertura |
| 45 | 10.17 | 221 | Retenção vertical 4" | 2 | 2.188,26 | 97,1 | S | — | E: confirmar 2 + 2 |
| 46 | 8.2.9 | 103 | Joelho 90° DN 60 | 34 | 2.034,22 | 97,4 | S | — | C: conferir no isométrico |
| 47 | 8.3.7 | 128 | Niple galvanizado 2½" | 20 | 1.933,40 | 97,6 | S | — | D: 2 por união |
| 48 | 12.1.7 | 240 | Frete do conjunto UASB | 1 | 1.911,15 | 97,9 | **S → A** | −169,95 | F: quantidade confere; BDI → aquisição |
| 49 | 12.2.5 | 246 | Frete do conjunto FBAS | 1 | 1.911,15 | 98,1 | **S → A** | −169,95 | F: quantidade confere; BDI → aquisição |
| 50 | 10.15 | 219 | Retenção horizontal 2½" | 2 | 1.483,34 | 98,3 | S | — | E: OK; uma por soprador |
| 51 | 10.9 | 213 | Registro de gaveta 2½" | 2 | 1.373,52 | 98,5 | S | — | E: SEDOP, NÃO VERIFICÁVEL |
| 52 | 8.2.26 | 120 | Curva 90° DN 110 | 4 | 1.340,40 | 98,7 | S | — | C: conferir no isométrico |
| 53 | 8.2.20 | 114 | Adaptador curto com rosca 25 × ¾" | 140 | 1.232,00 | 98,8 | S | — | C: = difusores |
| 54 | 8.3.2 | 123 | Vara de tubo galvanizado "DN 110" | 1 | 1.011,43 | 99,0 | A | — | D: onde entra? sem conexão de 4" |
| 55 | 8.2.17 | 111 | Tê PVC DN 110 | 3 | 986,01 | 99,1 | S | — | C: conferir no isométrico |
| 56 | 8.3.5 | 126 | Cotovelo 90° galvanizado 2½" | 6 | 948,42 | 99,2 | S | — | D: conferir no isométrico |
| 57 | 8.3.8 | 129 | Tê de redução 2½ × 1¼" | 4 | 947,92 | 99,3 | S | — | D: OK; 2 alívios + 2 manômetros |
| 58 | 13.4 | 261 | Extintor ABC 6 kg | 3 | 802,89 | 99,4 | **S → A** | −71,40 | G: NÃO OK só por BDI |
| 59 | 8.3.4 | 125 | Cotovelo 45° galvanizado 2½" | 4 | 686,04 | 99,5 | S | — | D: conferir no isométrico |
| 60 | 8.2.2 | 96 | Tubo PVC DN 25 | 34 m | 584,80 | 99,6 | S | — | C: conferir no isométrico |
| 61 | 8.2.15 | 109 | Tê PVC DN 60 | 7 | 503,86 | 99,7 | S | — | C: conferir no isométrico |
| 62 | 8.3.6 | 127 | Luva galvanizada 2½" | 4 | 441,64 | 99,7 | S | — | D: conferir no isométrico |
| 63 | 10.6 | 210 | Manômetro 4" | 2 | 390,56 | 99,8 | A | — | E: NÃO VERIFICÁVEL; faixa de pressão |
| 64 | 8.2.12 | 106 | Luva PVC DN 110 | 2 | 305,60 | 99,8 | S | — | C: conferir no isométrico |
| 65 | 8.2.21 | 115 | Adaptador 75 × 2½" | 6 | 261,90 | 99,8 | S | — | C: conferir no isométrico |
| 66 | 8.2.24 | 118 | Bucha de redução 32 × 25 | 2 | 258,38 | 99,9 | S | — | C: NÃO OK; trocar por SINAPI 103953 (R$ 7,62) |
| 67 | 13.3 | 260 | Suporte para extintores | 3 | 230,97 | 99,9 | S | — | G: ORSE, NÃO VERIFICÁVEL |
| 68 | 8.2.22 | 116 | Luva PVC DN 85 | 2 | 172,94 | 99,9 | S | — | C: resíduo? |
| 69 | 8.2.8 | 102 | Joelho 90° DN 25 | 13 | 148,98 | 99,9 | S | — | C: conferir no isométrico |
| 70 | 13.1 | 258 | Placa de rota de fuga | 6 | 107,58 | 99,9 | S | — | G: ORSE, NÃO VERIFICÁVEL |
| 71 | 8.2.5 | 99 | Tubo PVC DN 85 | 1 m | 99,35 | 100,0 | S | — | C: resíduo? |
| 72 | 8.3.3 | 124 | Bucha galvanizada 1¼ × ½" | 2 | 93,78 | 100,0 | S | — | D: OK; 2 manômetros |
| 73 | 13.2 | 259 | Placa de segurança contra incêndio | 3 | 81,75 | 100,0 | **S → A** | −7,29 | G: OK com ressalva; só material; BDI → aquisição |
| 74 | 10.12 | 216 | Registro de esfera DN 20 | 2 | 58,16 | 100,0 | S | — | E: onde entra? |
| 75 | 8.2.18 | 112 | União PVC DN 25 | 2 | 39,64 | 100,0 | S | — | C: conferir no isométrico |
| 76 | 8.2.1 | 95 | Tubo PVC DN 20 | 1 m | 14,99 | 100,0 | S | — | C: resíduo? |
| 77 | 8.2.7 | 101 | Joelho 90° DN 20 | 1 | 9,61 | 100,0 | S | — | C: resíduo? |


**Fora do Δ BDI da tabela:** CPRB de 3,6% (≈ −R$ 3,6 mil, depende do regime); registros e retenções 10.9 a 10.17 (−R$ 1.670,23 se mudar o critério); correção da quantidade do 12.3.6 (−R$ 1.911,15, à parte).

---

## 10. Impactos em R$ já quantificados (com BDI)

| Ajuste | Impacto | Natureza |
|---|---|---|
| Reclassificar BDI do PRFV (fornecimento + fretes) e de 13.2/13.4 para aquisição | **−24.955,96** | Firme, se o critério do TCU for aceito |
| 12.3.6: frete com quantidade 1 (a proposta traz 1) | −1.911,15 | Firme (soma-se ao Δ BDI do mesmo item sem dupla contagem) |
| 8.2.24: trocar pela composição SINAPI 103953 | −238,98 | Firme |
| 1.16: excluir ou reduzir o comissionamento de incêndio | até −8.043,13 | Recomendação (depende de decisão) |
| 10.11 / 10.13: se 8 registros DN 60 forem duplicados | até −1.072,64 | Hipótese |
| 8.3.1: se o tubo for DN 65 em vez de DN 80 | ≈ −1,6 mil | Hipótese |
| 10.1: calha sem caixas de entrada e saída | até ≈ −3,1 mil | Hipótese |
| CPRB de 3,6% no BDI de serviço | ≈ −3,6 mil | A confirmar (regime) |
| 10.16 e 10.17: se 2 das 4 retenções forem excedentes | até −2.188,26 | Hipótese pouco provável (os 14 flanges fecham com 4) |
| 10.9 e 10.10: registros de gaveta SEDOP, se forem latão/bronze roscáveis (SINAPI 94499 e 94501) | −6.592,35 (−833,10 e −5.759,25) | Hipótese forte (seção 15.2); depende da descrição completa e da SEDOP |
| 6.1 e 6.2: guindaste com custo horário SINAPI completo, nas mesmas 720 h | **+84.573,60 (30 t) a +168.909,60 (60 t)** | Sentido contrário (abaixo do custo na data-base); depende do plano de içamento (seção 15.1) |
| **Não estimáveis hoje:** 6.1 e 6.2 (R$ 47.892,00 em discussão), soprador 10.3, filtro 10.5, PRFV (R$ 493 mil, sem preço público) | — | Dependem de plano de içamento, memorial e propostas |
| **Fora do escopo mecânico:** itens 2.3 e 2.5 | ≈ R$ 21 mil acima da tabela | Informar o fiscal responsável |

---

## 11. Pendências (de onde retomar) — atualizada na sessão 2

**Feito na sessão 2 (detalhes na seção 15):** referência de custo na data-base para o guindaste (6.1/6.2), para os registros SEDOP (10.9/10.10), para o incêndio (13.1, 13.3, 13.4) e para os equipamentos do comissionamento (1.13); Etapa 6 (lacunas de escopo) levantada, toda "a confirmar".

**Documentos a obter:**
0. **Reanexar a planilha `ORÇAMENTO_ETE__BARROS_062025_VENTO_SUL.xlsx`.** Sem ela não dá para ler a descrição completa dos itens 10.9, 10.10, 13.1 e 13.3, nem a CPU do 1.13 (taxa horária do guindaste de 12 t), nem conferir as lacunas da seção 15.5 contra os grupos civis e elétricos.
1. **Tabelas SEDOP 02/2025, ORSE 06/2025 e EMBASA 06/2025.** Fecham 10.9, 10.10, 13.1, 13.3 e 1.13. Pedir também a justificativa de usar a EMBASA (Bahia) e a ORSE (Sergipe). Para 10.9/10.10, o que decide é o **material e a ligação** (latão roscável × ferro fundido flangeado), seção 15.2.
2. **Proposta completa da Biomais** (CNPJ, validade, especificação, desenhos) e **mais duas propostas** do PRFV. Pedir a proposta desmembrada em fornecimento e montagem.
3. **Projeto e memorial de processo:** vazão e pressão do ar, ponto de operação das motobombas, isométrico da rede de ar (DN 50? espaçamento dos difusores, 21 registros DN 60), volume do pall ring, peças e fundação do PRFV; e os pontos da seção 15.5 (biogás, lodo, dosagem, suportes, instrumentação).
4. **Plano de içamento** com peso das peças, raio, capacidade do guindaste e horas (decide 6.1 e 6.2; seção 15.1 dá as faixas).
5. **Edital e contrato:** regime de execução, origem dos recursos (Decreto 7.983/2013?), regime de CPRB e alíquota, índice de reajuste.
6. **Propostas formais** para 10.2 (dosadora), 10.3 (soprador, no modelo especificado), 10.5 (filtro compatível), 10.6 (manômetro) e 10.14 (válvula de alívio).

**Decisões do usuário em aberto:**
- Quais itens de fronteira entram no escopo (8.1, 6.4/6.5, 7.5 + 1.7, 1.8).
- Confirmar a aplicabilidade das normas (NBR 12209, 12208, 5580, 12693; NR-10, 12, 33, 35; Lei 14.133 art. 23 e 41; Decreto 7.983/2013) antes de afirmar conformidade (Etapa 7).
- Formato do parecer final (.xlsx ou Word).

**Hipóteses ainda a confirmar:**
H1 temperatura do ar × limite do PVC · H2 tubo DN 80 × conexões 2½" · H3 pressão de abertura da válvula de alívio ("140") · H4 válvulas roscáveis × adaptadores com flange · H5 140 saídas em 53 m de DN 75 · H6 INSS de 5% já dentro dos encargos SINAPI de 2025 · H7 ISS na composição de aquisição · H8 filtro pequeno para o soprador · H9 pall ring 2" × 3" · H10 equipamento "soprador" 8,6 kW × 12,6 kW · **H11** registros SEDOP 10.9/10.10 são latão roscável (então acima do SINAPI) ou ferro fundido flangeado (então ligados a H4) · **H12** as 720 h de guindaste não correspondem a uma necessidade real de içamento.

**Próximos passos naturais:**
- Com a planilha reanexada: ler a descrição completa de 10.9, 10.10, 13.1, 13.3 e a CPU do 1.13; conferir a seção 15.5 contra os demais grupos.
- Com as tabelas SEDOP/ORSE/EMBASA: fechar o preço dos itens restantes de tabela.
- Com o projeto: fechar quantitativos (rede, difusores, registros, retenções), diâmetros e especificação dos equipamentos.
- Com mais propostas: fechar o grupo 12 (maior valor do escopo).
- Etapa 7 (conformidade), depois da decisão sobre as normas.
- Gerar o **parecer final** (tabela por item, resumo executivo, pendências, documentos faltantes) em .xlsx ou Word.

---

## 12. Registro de correções feitas na conversa (não repetir os erros)

1. **Soprador:** a hipótese inicial de que "CRC 2820" era código de anúncio usado estava **errada**. CRC é a nomenclatura da Asten; o modelo CRC-2 820 36 TD HE tem 12,6 kW. O print anexado é de 8,6 kW, com vazão e pressão máximas parecidas. A divergência é de especificação e potência, e o status correto é **NÃO VERIFICÁVEL** até o projeto definir o ponto de operação. O preço do print (R$ 10.567,90) está no piso do mercado para 8,6 kW (R$ 10,6 a R$ 13,6 mil).
2. **BDI do decantador:** o impacto de mudar para aquisição é **R$ 17.932,38** (não R$ 40 mil). Somando os 4 fornecimentos PRFV: R$ 23.121,12.
3. **Curva ABC:** a primeira versão separava decantador e frete, guindaste CHP e CHI, e registros DN 60 de mesmo código. A versão desta seção agrupa o mesmo objeto de custo. Total e Δ BDI não mudaram.
4. **Itens 8.2 que eu chamava de "preço não verificável":** passaram a **OK** depois que a tabela SINAPI 06/2025 foi recebida.
5. **Grupo 12:** tem **20 linhas** (12.1.1 a 12.1.7, 12.2.1 a 12.2.5, 12.3.1 a 12.3.6, 12.4.1 e 12.4.2).
6. **Inflação 06/2025 → 09/2026 (sessão 2):** a faixa "+0,5% a +14%" da sessão 1 estava incompleta. Item a item vai de −19,8% (tubo DN 20) a +22,1% (bucha 50 × 25, item 8.2.25); vários itens de PVC de pequeno diâmetro caíram depois da revisão de composições de 09/2026.

---

## 13. Notas técnicas para refazer as extrações

**Planilha (openpyxl):**
- Aba `PLANILHA ORÇAMENTÁRIA`: colunas e fórmulas da seção 3. Para ver as fórmulas, abrir sem `data_only`; para os valores, com `data_only=True`.
- Aba `CPUs_062025`: cada composição começa numa linha com o número do item na coluna A e "Código" na B; as linhas seguintes têm "Composição", "Comp. Aux." ou "Insumo" na coluna A. Na leitura por índice (0-based): código = 1, banco = 2, descrição = 3, **quantidade = 7**, **valor unitário = 8**, total = 9.
- As imagens das cotações ficam em `xl/media/imageN.png` dentro do .xlsx (descompactar o .xlsx). A proposta da Biomais (página 4, base do grupo 12) está em `image36.png`; a calha Parshall (10.1) em `image5.png`; o soprador (10.3) em `image7.png`.

**SINAPI (Referência xlsx):**
- Abas: `ISD`/`ICD` (insumos sem/com desoneração), `CSD`/`CCD` (composições sem/com desoneração), `Analítico`.
- Dados a partir da linha 11. Cada UF ocupa 2 colunas (Custo e %AS) nas composições. **PA = índice 30 (0-based) em CCD/CSD** e **índice 18 em ICD/ISD**.
- Em CCD/CSD, o código da composição está **dentro de uma fórmula HYPERLINK** (ler com `data_only=False` e extrair com a expressão `,(\d+)\)\s*$`). Em ICD/ISD o código é número direto.
- Encargos PA: linhas 6 (horista) e 7 (mensalista) da aba CCD.
- `SINAPI_Manutenções_*.xlsx`: histórico por código (Referência, Tipo, Código, Descrição, Manutenção), a partir da linha 6. Serve para saber quando um código foi criado, alterado ou desativado.
- Preço "0" na tabela significa composição **sem custo divulgado**.

---

## 14. Fontes consultadas (acesso em 15/10/2026)

- **TCU, Acórdão 2622/2013-Plenário** (faixas de BDI): pesquisa.apps.tcu.gov.br; transcrição em editais.uff.br (Base BDI – Acórdão-2622-2013.pdf); buscadorsinapi.com.br/bdi-referencia. *Conferir no texto oficial antes de citar.*
- **Lei 14.973/2024** (reoneração da folha): gov.br/compras (orientação sobre a reoneração gradual); FIEMG, Informação Estratégica nº 49.
- **IBGE/SINAPI:** índice nacional de 6,81% em 12 meses até 09/2026 (ftp.ibge.gov.br, caderno sinapi_202609).
- **SINAPI/CAIXA:** caixa.gov.br/sinapi (pacote "SINAPI-2025-06-formato-xlsx.zip").
- **Mercado:** lojaeraambiental.com.br (difusor 270 mm); altamar.com.br (disco difusor 250 mm); meritocomercial.com.br, comerciallanel.com.br, acasasaopaulo.com.br, ricardobombas.com.br, leomarbombas.com.br (Brava E30); asten.com.br (catálogo de compressores radiais); olx.com.br (compressor radial duplo estágio 11,53 cv); mercadolivre.com.br e ecr.ind.br (calha Parshall 6"); biodigestornaweb.com.br (anel pall 3"); orcamentor.com (GOINFRA 02/2026 e ORSE-1511).

---

## 15. Sessão 2 (15/10/2026): conferência com o SINAPI-PA 06/2025

**Arquivos recebidos na sessão 2:** este HANDOFF e os quatro arquivos SINAPI 06/2025. **A planilha do orçamento não veio.** Todo valor "orçado" abaixo vem das seções 5 a 10; o custo unitário sem BDI foi obtido como (total c/ BDI ÷ quantidade ÷ fator de BDI), o que é aritmética, não leitura da planilha.
**Controle:** encargos PA desonerados 95,00% e 53,45% e o código 103953 a R$ 7,62 batem com a sessão 1 (é a mesma tabela).
**Fonte de todos os preços desta seção:** SINAPI-PA 06/2025, desonerado (abas CCD e ICD do arquivo `SINAPI_Referência_2025_06.xlsx`, emissão 11/07/2025) e histórico em `SINAPI_Manutenções_2025_06.xlsx`.

### 15.1 Guindaste (6.1 e 6.2): há código com custo na data-base

| Código | Equipamento (SINAPI-PA 06/2025) | CHP (R$/h) | CHI (R$/h) | Histórico |
|---|---|---|---|---|
| 102850 / 102851 | Sobre esteiras, lança treliçada 40 m, 75 t (**o usado na planilha**) | 0 (sem custo) | 0 (sem custo) | criados 11/2021 "sem custo" |
| 93287 / 93288 | Hidráulico autopropelido, lança telescópica 40 m, **60 t**, 260 kW | **353,26** | **177,88** | com custo desde 03/2016 |
| 89272 / 89273 | Hidráulico autopropelido, lança telescópica 28,80 m, **30 t**, 97 kW | **220,46** | **106,38** | com custo desde 11/2014 |
| 105984 / 105985 | Guindauto 8,5 t (30,4 t·m), caminhão trucado | 337,30 | 97,85 | criado 05/2025 com custo |
| 106251 | Guindauto 14,3 t | — | — | **não existe na tabela de 06/2025** |

**Fato:** no 75 t sobre esteiras só têm custo os "materiais na operação" (102849, R$ 69,85/h) e o operador (88296, R$ 28,93/h). Somam R$ 98,78/h, exatamente a CHP da planilha; a CHI da planilha (R$ 28,93) é só o operador. No 60 t, a CHP é depreciação 99,64 + juros 35,12 + manutenção 160,17 + materiais 15,21 + impostos e seguros 14,19 + operador 28,93; a CHI é depreciação + juros + impostos e seguros + operador.

**Mesmas horas da planilha (240 CHP + 480 CHI), BDI de serviço e TRUNC como na planilha:**

| Base | CHP c/ BDI | CHI c/ BDI | Total c/ BDI | Diferença contra o orçado |
|---|---|---|---|---|
| Orçado (75 t sem depreciação, juros e manutenção) | 125,85 | 36,85 | 47.892,00 | — |
| 30 t (89272/89273) | 280,88 | 135,53 | 132.465,60 | +84.573,60 |
| 60 t (93287/93288) | 450,08 | 226,63 | 216.801,60 | +168.909,60 |

**Leitura (pergunta 3 × pergunta 4):**
- **Preço por hora: NÃO OK, abaixo do custo na data-base.** É prejuízo real, não efeito de inflação: a CHP orçada é 28% da CHP do 60 t e 45% da do 30 t, e o código escolhido não tem custo oficial.
- **Quantidade: NÃO VERIFICÁVEL e suspeita (H12).** 720 h, das quais 480 improdutivas, para montar 8 unidades de PRFV (2 UASB, 2 FBAS, 2 tanques de contato, 2 decantadores, conforme as quantidades da seção 9) não tem plano que sustente. O orçado (R$ 37.593,60 sem BDI) paga cerca de **106 h produtivas do 60 t** ou **170 h do 30 t**, sem nenhuma hora improdutiva.
- **Conclusão:** os dois erros puxam em sentidos opostos e o efeito líquido só sai com o **plano de içamento** (peso, raio, capacidade, horas). Recomendação: reorçar 6.1/6.2 com código **com custo** compatível com a capacidade do plano (30 t, 60 t ou guindauto) e as horas do plano; não usar 102850/102851. Conferir junto a sobreposição com as 20 h de guindaste de 12 t dentro do 1.13.

### 15.2 Registros de gaveta SEDOP (10.9 e 10.10)

| Item | Orçado sem BDI (derivado) | SINAPI-PA 06/2025, mesmo diâmetro | Razão | Δ c/ BDI se trocar pelo SINAPI |
|---|---|---|---|---|
| 10.9 registro de gaveta 2½" ×2 | ≈ R$ 539,02/un | 94499 gaveta bruto latão roscável 2½" F+I: R$ 212,08 (insumo 6011: R$ 188,45) | 2,54× | −833,10 |
| 10.10 registro de gaveta 4" ×3 | ≈ R$ 2.019,68/un | 94501 gaveta bruto latão roscável 4" F+I: R$ 512,93 (insumo 6027: R$ 475,38) | 3,94× | −5.759,25 |

- **Comparação interna (fato):** o registro de gaveta de 4" orçado custa mais que a **retenção** de bronze de 4" do mesmo orçamento (10.16 = SINAPI 99626, R$ 1.233,99), quando no SINAPI a gaveta de 4" (R$ 512,93) custa menos da metade da retenção.
- **Registro de ferro fundido flangeado** (SINAPI 103527 a 103536, DN 50 a 500) existe, mas está **sem custo** desde a criação (12/2021); não serve de referência.
- **Leitura (H11):** se a SEDOP for registro de latão ou bronze roscável (mesmo padrão das retenções 10.15 a 10.17), o item está **acima** e o ajuste é de **−R$ 6.592,35 c/ BDI**. Se for ferro fundido flangeado, o preço pode ser coerente e ajuda a explicar os 14 adaptadores com flange (H4); aí as retenções roscáveis é que ficam fora do padrão. **Status: NÃO VERIFICÁVEL, com indício de preço acima.** Falta a descrição completa do item (planilha) e a SEDOP 02/2025.

### 15.3 Incêndio (13.1, 13.3, 13.4)

| Item | Orçado sem BDI (derivado) | Referência SINAPI-PA 06/2025 | Leitura | Status |
|---|---|---|---|---|
| 13.4 extintor ABC 6 kg ×3 | ≈ R$ 210,05/un | Não há ABC no SINAPI. PQS **BC** 6 kg: insumo 10892 R$ 242,50; F+I 101909 R$ 267,42 | Não está acima; o ABC orçado sai abaixo do BC do SINAPI e dentro do mercado da seção 7 (R$ 191,50 a R$ 226,94) | Preço OK; **NÃO OK só pelo BDI** (sem mudança) |
| 13.1 placa rota de fuga ×6 (ORSE) | ≈ R$ 14,07/un | Insumos fotoluminescentes: 37557 14×14 cm R$ 11,06; 37539 13×26 cm R$ 18,50; 37556 20×20 cm R$ 21,39 (só material) | Dentro da faixa do insumo SINAPI | **OK com ressalva** (dimensão e tabela ORSE a confirmar) |
| 13.3 suporte de extintor ×3 (ORSE) | ≈ R$ 60,43/un | SINAPI não tem o item | — | NÃO VERIFICÁVEL (sem mudança) |

### 15.4 Comissionamento 1.13 (EMBASA): referências para os equipamentos

- Caminhão jato/vácuo, 40 h a R$ 239,18/h (seção 8): o SINAPI só tem caminhão de **sucção** 12.000 L (92106, CHP R$ 373,15; CHI 92107 R$ 95,24). O orçado não está acima dessa referência, mas o equipamento não é o mesmo (jato + vácuo combinados).
- Guindaste de 12 t, 20 h: o SINAPI-PA 06/2025 não tem 12 t. As referências mais próximas são o guindauto 8,5 t (105984, R$ 337,30/h) e o guindaste 30 t (89272, R$ 220,46/h). A taxa usada no 1.13 não está no HANDOFF; falta a CPU (planilha).
- **Status: continua NÃO VERIFICÁVEL.** A questão principal segue sendo se o serviço existe no projeto e se repete o 6.1/6.2.

### 15.5 Etapa 6: lacunas de escopo (todas "a confirmar")

Lista do que um sistema UASB + FBAS aerado + decantador + tanque de contato normalmente precisa e que **não aparece entre os 80 itens mecânicos** da seção 4. Pode estar em outro grupo (elétrico, civil), na unidade existente ou fora do objeto: nada aqui é afirmação de falta.

| # | Possível lacuna | Por que importa | Onde conferir |
|---|---|---|---|
| L1 | Biogás do UASB: coleta, selo hídrico, queimador | Segurança e odor; reator anaeróbio gera gás inflamável | Projeto; unidade existente? |
| L2 | Lodo: descarte/recirculação do decantador ao UASB, tubulação de lodo, destino (leito de secagem ou caçamba) | Sem descarte o decantador perde eficiência; as 2 motobombas 10.7 podem ser essa função | Memorial de processo; grupo 8.1 (fronteira) |
| L3 | Partida: inoculação do UASB (lodo, transporte) e período de partida assistida | O 1.13 pode cobrir; conferir na CPU | CPU 1.13 |
| L4 | Quadros de comando e partida de sopradores e motobombas (alternância, reserva, proteção) | Equipamento sem comando não opera | Grupo elétrico |
| L5 | Base, amortecedores e junta flexível na descarga dos sopradores; silenciador; abrigo ventilado | Vibração e ruído; transmissão de esforço à rede de PVC | Projeto; grupos civis |
| L6 | Suportes e abraçadeiras das redes de ar (PVC e galvanizada) | Nenhum item de suporte no grupo 8 | Grupo 8; CPUs |
| L7 | Descidas de ar e fixação da grade de difusores no fundo do reator | Os 140 difusores precisam de suporte e nivelamento | Proposta Biomais; projeto |
| L8 | Dosagem: tanque de solução, mangueira, ponto de injeção, bacia de contenção | 10.2 tem só as dosadoras; produto químico não definido | Memorial; grupo 12.3 |
| L9 | Instrumentação: medidor de nível na calha Parshall, vazão de ar, OD | Sem isso não se controla a aeração nem a vazão tratada | Projeto |
| L10 | Barras-guia e corrente para as motobombas submersíveis; válvulas da elevatória | O grupo 11 é todo civil, sem bomba | Projeto do grupo 11 |
| L11 | Testes: estanqueidade dos tanques PRFV, teste de pressão das redes | Condição de recebimento | CPU 1.13; proposta Biomais |
| L12 | Segurança em espaço confinado e em altura (ventilação, detector de gás, vigia, andaime) para o revestimento interno dos tanques | Custo de execução e exigência legal (NR-33, NR-35: aplicabilidade a confirmar, Etapa 7) | Composições do grupo 12; administração local |
| L13 | Manual de operação, treinamento e "as built" | Recebimento da obra | CPU 1.13; edital |

### 15.6 Status que mudaram na sessão 2

| Item | Antes | Agora | Motivo |
|---|---|---|---|
| 6.1 + 6.2 | NÃO OK (sem custo oficial) | **NÃO OK**, agora com faixa: custo SINAPI completo nas mesmas horas = R$ 132,5 mil (30 t) a R$ 216,8 mil (60 t) | 15.1 |
| 10.9 | NÃO VERIFICÁVEL | NÃO VERIFICÁVEL, **indício de acima** (2,54× SINAPI 94499) | 15.2 |
| 10.10 | NÃO VERIFICÁVEL | NÃO VERIFICÁVEL, **indício de acima** (3,94× SINAPI 94501) | 15.2 |
| 13.1 | NÃO VERIFICÁVEL | OK com ressalva | 15.3 |
| 13.4 | NÃO OK só por BDI | sem mudança; preço confirmado abaixo da referência BC | 15.3 |

---

## 16. Sessão 2: comparação com o SINAPI-PA 09/2026 (pergunta 3: "está muito abaixo hoje?")

**Arquivos:** `SINAPI_Referência_2026_09.xlsx` (emissão 09/10/2026), `SINAPI_Manutenções_2026_09.xlsx` e os demais de 09/2026, recebidos na sessão 2. Mesmo método: PA, desonerado, BDI e TRUNC da planilha.
**Encargos PA desonerados 09/2026:** horista **103,26%** e mensalista **59,98%** (em 06/2025: 95,00% e 53,45%). *Hipótese:* a alta acompanha a reoneração gradual da folha prevista na Lei 14.973/2024 (INSS de 5% em 2025 para 10% em 2026).
**Como os códigos foram identificados:** a planilha não estava disponível; o código SINAPI de cada item foi obtido casando o preço unitário c/ BDI (seção 9) com TRUNC(custo 06/2025 × 1,2741) e conferindo a descrição. Os 36 itens casaram com **um único código** de descrição compatível. Confirmar na planilha quando ela for reanexada.

### 16.1 Itens SINAPI do escopo mecânico (36 linhas, com o 10.11 junto do 10.13)

| Item | Código | Descrição | Qtd | Custo 06/2025 | Custo 09/2026 | Variação | Total c/ BDI 06/2025 | Total c/ BDI 09/2026 | Diferença |
|---|---|---|---|---|---|---|---|---|---|
| 8.2.1 | 89401 | Tubo PVC DN 20 | 1 | 11,77 | 9,44 | −19,80% | 14,99 | 12,02 | −2,97 |
| 8.2.2 | 89402 | Tubo PVC DN 25 | 34 | 13,50 | 11,93 | −11,63% | 584,80 | 516,80 | −68,00 |
| 8.2.3 | 89450 | Tubo PVC DN 60 | 67 | 34,65 | 36,15 | +4,33% | 2.957,38 | 3.085,35 | +127,97 |
| 8.2.4 | 89451 | Tubo PVC DN 75 | 53 | 56,55 | 59,02 | +4,37% | 3.818,65 | 3.985,07 | +166,42 |
| 8.2.5 | 89452 | Tubo PVC DN 85 | 1 | 77,98 | 81,44 | +4,44% | 99,35 | 103,76 | +4,41 |
| 8.2.6 | 94655 | Tubo PVC DN 110 | 39 | 140,85 | 148,67 | +5,55% | 6.998,55 | 7.387,38 | +388,83 |
| 8.2.7 | 89404 | Joelho DN 20 | 1 | 7,55 | 6,69 | −11,39% | 9,61 | 8,52 | −1,09 |
| 8.2.8 | 89408 | Joelho DN 25 | 13 | 9,00 | 9,29 | +3,22% | 148,98 | 153,79 | +4,81 |
| 8.2.9 | 89505 | Joelho DN 60 | 34 | 46,96 | 48,75 | +3,81% | 2.034,22 | 2.111,74 | +77,52 |
| 8.2.10 | 89513 | Joelho DN 75 | 24 | 119,63 | 124,66 | +4,20% | 3.658,08 | 3.811,68 | +153,60 |
| 8.2.11 | 94686 | Joelho DN 110 | 11 | 291,42 | 307,03 | +5,36% | 4.084,19 | 4.302,98 | +218,79 |
| 8.2.12 | 94671 | Luva DN 110 | 2 | 119,93 | 126,96 | +5,86% | 305,60 | 323,50 | +17,90 |
| 8.2.13 | 89427 | Luva c/ bucha latão 25 × ¾" | 140 | 13,33 | 13,51 | +1,35% | 2.377,20 | 2.409,40 | +32,20 |
| 8.2.14 | 94698 | Tê de redução 75 × 50 | 140 | 75,13 | 79,77 | +6,18% | 13.400,80 | 14.228,20 | +827,40 |
| 8.2.15 | 94696 | Tê DN 60 | 7 | 56,50 | 60,06 | +6,30% | 503,86 | 535,64 | +31,78 |
| 8.2.16 | 94697 | Tê DN 75 | 22 | 97,83 | 103,78 | +6,08% | 2.742,08 | 2.908,84 | +166,76 |
| 8.2.17 | 94701 | Tê DN 110 | 3 | 257,97 | 272,69 | +5,71% | 986,01 | 1.042,29 | +56,28 |
| 8.2.18 | 89428 | União DN 25 | 2 | 15,56 | 16,22 | +4,24% | 39,64 | 41,32 | +1,68 |
| 8.2.20 | 89383 | Adaptador 25 × ¾" | 140 | 6,91 | 7,55 | +9,26% | 1.232,00 | 1.345,40 | +113,40 |
| 8.2.21 | 89613 | Adaptador 75 × 2½" | 6 | 34,26 | 35,63 | +4,00% | 261,90 | 272,34 | +10,44 |
| 8.2.22 | 89614 | Luva DN 85 | 2 | 67,87 | 70,73 | +4,21% | 172,94 | 180,22 | +7,28 |
| 8.2.23 | 94715 | Adaptador c/ flanges 110 × 4" | 14 | 347,13 | 364,52 | +5,01% | 6.191,78 | 6.502,02 | +310,24 |
| 8.2.25 | 103999 | Bucha de redução 50 × 25 | 140 | 13,47 | 16,45 | +22,12% | 2.402,40 | 2.933,00 | +530,60 |
| 8.2.26 | 94687 | Curva 90° DN 110 | 4 | 263,01 | 277,28 | +5,43% | 1.340,40 | 1.413,12 | +72,72 |
| 8.3.1 | 94464 | Tubo galvanizado DN 80 | 34 | 155,65 | 156,42 | +0,49% | 6.742,54 | 6.775,86 | +33,32 |
| 8.3.4 | 94474 | Cotovelo 45° galv. 2½" | 4 | 134,62 | 150,14 | +11,53% | 686,04 | 765,16 | +79,12 |
| 8.3.5 | 94473 | Cotovelo 90° galv. 2½" | 6 | 124,07 | 138,32 | +11,49% | 948,42 | 1.057,38 | +108,96 |
| 8.3.6 | 94467 | Luva galv. 2½" | 4 | 86,66 | 96,65 | +11,53% | 441,64 | 492,56 | +50,92 |
| 8.3.7 | 94468 | Niple galv. 2½" | 20 | 75,88 | 84,58 | +11,47% | 1.933,40 | 2.155,20 | +221,80 |
| 8.3.9 | 92890 | União galv. 2½" | 10 | 213,45 | 239,04 | +11,99% | 2.719,50 | 3.045,60 | +326,10 |
| 10.11+10.13 | 94493 | Registro de esfera DN 60 | 21 | 105,24 | 110,23 | +4,74% | 2.815,68 | 2.949,24 | +133,56 |
| 10.12 | 103047 | Registro de esfera DN 20 | 2 | 22,83 | 24,01 | +5,17% | 58,16 | 61,18 | +3,02 |
| 10.15 | 99624 | Retenção horizontal 2½" | 2 | 582,12 | 663,23 | +13,93% | 1.483,34 | 1.690,04 | +206,70 |
| 10.16 | 99626 | Retenção horizontal 4" | 2 | 1.233,99 | 1.406,33 | +13,97% | 3.144,44 | 3.583,60 | +439,16 |
| 10.17 | 99634 | Retenção vertical 4" | 2 | 858,75 | 978,25 | +13,92% | 2.188,26 | 2.492,76 | +304,50 |
| 13.2 | 37556 | Placa fotolum. 20 × 20 (insumo) | 3 | 21,39 | 17,35 | −18,89% | 81,75 | 66,30 | −15,45 |
| **Total** | | | | | | **+6,46%** | **79.608,58** | **84.749,26** | **+5.140,68** |

(O total de 06/2025 inclui as 8 unidades do 10.11, R$ 1.072,64; sem elas dá os R$ 78.535,94 da seção 5.)

**Leitura:**
- **Nenhum item SINAPI do escopo mecânico ficou "muito abaixo hoje" por outro motivo que não a inflação.** A maior defasagem em R$ está no tê 75 × 50 (8.2.14, +R$ 827,40), na bucha 50 × 25 (8.2.25, +R$ 530,60) e nas retenções de bronze (10.15 a 10.17, +R$ 950,36 somadas). É matéria de **reajuste contratual**, não de prejuízo (critério da seção 2).
- Itens que **caíram** de preço: 8.2.1, 8.2.2 e 8.2.7 (composições revisadas em 09/2026, descrição e coeficientes) e 13.2 (queda do preço do insumo 37556). Não muda nada na data-base.

### 16.2 Códigos alterados ou desativados depois da data-base (Manutenções 09/2026)

| Data | Código | Item | Manutenção |
|---|---|---|---|
| 10/2025 | 99837 | 6.5 guarda-corpo (fronteira) | **Desativação**; o código não aparece mais em 09/2026 |
| 10/2025 | 106251 | (referência) guindauto 14,3 t | Criação com custo (R$ 373,13/h em 09/2026) |
| 01/2026 | 92890 | 8.3.9 união galvanizada 2½" | Alteração de descrição e coeficientes |
| 01/2026 | 101909 | (referência do 13.4) extintor PQS BC 6 kg | Alteração de descrição e coeficientes |
| 09/2026 | 89383, 89401, 89402, 89404, 89408, 89427, 89428, 89450, 89451, 89452, 89505, 89513, 89613, 89614, 103953, 103999 | 8.2.1 a 8.2.5, 8.2.7 a 8.2.10, 8.2.13, 8.2.18, 8.2.20 a 8.2.22, 8.2.25 e a referência do 8.2.24 | Alteração de descrição e coeficientes |

Nenhum código usado nos itens do escopo mecânico foi desativado. A revisão de 09/2026 não afeta a análise na data-base, mas qualquer **aditivo** com preço novo deve usar a composição revisada.

### 16.3 Itens sem preço SINAPI direto, vistos em 09/2026

| Item | 06/2025 | 09/2026 | Leitura |
|---|---|---|---|
| 6.1/6.2 guindaste 75 t sobre esteiras (102850/102851) | sem custo | **continua sem custo** | Materiais na operação foram de R$ 69,85 para R$ 79,64 (+14,0%); operador de R$ 28,93 para R$ 34,19 (+18,2%) |
| Referência 30 t (89272/89273), mesmas 720 h, c/ BDI | 132.465,60 | 138.616,80 | O orçado (R$ 47.892,00) cobre 35% hoje e 36% na data-base: a defasagem é **anterior** à inflação |
| Referência 60 t (93287/93288), mesmas 720 h, c/ BDI | 216.801,60 | 221.745,60 | Idem (22% hoje) |
| 10.9 registro gaveta 2½" (ref. 94499) | 212,08 | 347,68 (+63,9%) | O insumo 6011 subiu de R$ 188,45 para R$ 321,59 sem mudança na composição. **Mesmo hoje** o orçado (≈ R$ 539,02) fica 1,55× acima |
| 10.10 registro gaveta 4" (ref. 94501) | 512,93 | 852,66 (+66,2%) | O insumo 6027 subiu de R$ 475,38 para R$ 811,24. **Mesmo hoje** o orçado (≈ R$ 2.019,68) fica 2,37× acima |
| 13.4 extintor (ref. BC 6 kg, 101909) | 267,42 | 260,84 (−2,5%) | Sem defasagem |
| 8.2.24 bucha 32 × 25 (ref. 103953) | 7,62 | 8,49 (+11,4%) | O orçado (R$ 101,40) segue ≈ 12× a referência |
| 1.13 caminhão de sucção (ref. 92106) | 373,15 | 412,29 (+10,5%) | O orçado (R$ 239,18/h) segue abaixo |

**Efeito na seção 15.2 (H11):** se 10.9/10.10 forem de latão roscável, o ajuste a preço de 09/2026 seria −R$ 487,58 e −R$ 4.460,70 (−R$ 4.948,28). O ajuste correto continua sendo o da **data-base** (−R$ 6.592,35); o número de 09/2026 só mostra que o excesso não é explicado pela inflação.

### 16.4 Resposta à pergunta 3 no escopo mecânico

- **Abaixo do custo já na data-base (prejuízo real, não se resolve com reajuste):** só o guindaste 6.1/6.2, e o tamanho do prejuízo depende das horas do plano de içamento (seção 15.1). Itens fora do SINAPI (PRFV, equipamentos cotados) continuam NÃO VERIFICÁVEIS.
- **Abaixo hoje só por inflação:** os itens SINAPI, +6,46% no conjunto (+R$ 5.140,68 c/ BDI). Resolve-se com o índice de reajuste do contrato (a confirmar).
- **Acima mesmo hoje:** 8.2.24 (bucha) e, se forem de latão, os registros 10.9/10.10.

---

## 17. Sessão 2 (16/10/2026): planilha do projetista e memorial (ESP R00)

### 17.1 Documentos recebidos
- **Planilha do projetista:** `ORÇAMENTO ETE. BARROS BARRETO maio-2026 - entregue.xls` (Sanigy; data do orçamento 23/02/2026; SINAPI 11/2025 desonerado, ORSE 05/2025, SEDOP 10/2025, SICRO3 07/2025; total R$ 1.892.034,82). Tem as mesmas abas ocultas da planilha analisada (orçamento antigo de R$ 1.489.434,21 e curva ABC de 23/02/2026): mesma origem.
- **Memorial:** `1. ESP ETE HOSPITAL UNIVERSITÁRIO JOÃO DE BARROS BARRETO R00.pdf` (Sanigy, julho/2025, 25 p.). Contratante do projeto: BM Serviço de Apoio Administrativo Ltda (CNPJ 23.941.500/0001-23). RT: Addyson Macedo Silva, CREA 1519212780/PA, ART PA20251354299. Normas citadas: NBR 12208/2020, NBR 12209/2011, CONAMA 357/2005 e 430/2011. **Só traz especificações:** as seções de cálculo do sumário não existem no arquivo (referências quebradas), então não há vazões nem demanda de ar.

### 17.2 Comparação com a planilha do projetista (escopo mecânico)
- Mesmos itens, códigos e fontes; os 36 códigos SINAPI deduzidos conferem. Grupo 12 idêntico ao centavo.
- Total mecânico: analisada R$ 778.719,20 × projetista R$ 786.370,57 (−1,0%). Causas: 1.13 −13.016,16 (mesmo código EMBASA, sem explicação); mão de obra de instalação somada às cotações +5.882,04; 1.16 −1.152,55 (só mão de obra: 06/2025 × valores iguais aos de 09/2026); data-base SINAPI +777,52; outros −139,57.
- Única quantidade divergente: 10.12 (2 na analisada, 1 no projetista). Pelo memorial, a analisada está certa (2 tanques de contato).
- Os erros já apontados (BDI do PRFV, frete 12.3.6 ×2, 8.3.1, guindaste, soprador, filtro, 8.2.24, registros SEDOP) **estão na planilha do projetista**.
- A planilha do projetista mistura data-bases de mão de obra entre composições e tem a composição 8 (10.11) com insumo "escavadeira hidráulica" num registro de PVC.
- **Total geral:** analisada R$ 2.343.873,57 × projetista R$ 1.892.034,82 (+R$ 451.838,75, +23,9%), concentrado fora do escopo mecânico. Precisa da planilha analisada para localizar.

### 17.3 O que o memorial muda

| Item | Memorial diz | Efeito |
|---|---|---|
| 10.3 soprador | Compressor **existente** na ETE: CRC 2 820 36 TD HE, 10,33 m³/min, 16,9 cv, "pressão de operação 0,6 a 0,8 kgf/cm²". O Anexo II mostra **outro** modelo (CRC-2 520 46 TD HE, 3,45 kW, 4,58 m³/min, 3.400 mmCA) | Por que comprar 2? (até −R$ 24.987,56). O modelo do Anexo II não vence a lâmina de 3,90 m do FAS; a pressão do texto não bate com nenhum modelo; o cotado (JQT-7500, 40 kPa ≈ 4.080 mmCA) deixa pouca folga. **NÃO OK (incoerência projeto × orçamento)** |
| 10.2 dosadora | EMEC FCE **existente**; hipoclorito de sódio; 1,5 L/h | Por que comprar 2? (até −R$ 3.299,14) |
| 10.4 difusor | 140 un, disco bolhas finas, Vagalhões, 9 m³/h, PP/EPDM, **rosca macho ¾" BSP**, fixação em estrutura PRFV no fundo | Quantidade confirmada. Com rosca macho no difusor, a peça necessária é a luva com bucha de latão (8.2.13); o adaptador curto (8.2.20) tende a sobrar: −R$ 1.232,00 (hipótese forte). 140 × 9 = 1.260 m³/h é capacidade do difusor, não demanda (2 compressores CRC 2 820 somam 1.240 m³/h só na vazão máxima) |
| Rede de ar | Interna PVC DN 75; **externa aço galvanizado 2½"** | 8.3.1 (tubo 3") **NÃO OK confirmado**: trocar por 2½" (SINAPI 94463): −R$ 1.611,60 |
| 10.7 motobomba | Brava E30 3 cv **a adquirir**, EEE de esgoto bruto, 32,7 m³/h máx, Hm ≥ 14 mca, alternância | Função esclarecida: **OK** |
| 10.16/10.17 retenções | EEE: **válvulas de retenção em ferro fundido** | Orçamento usa bronze roscável: **NÃO OK (especificação)**. Os 14 adaptadores com flange (8.2.23) são coerentes com válvulas flangeadas de ferro fundido |
| 10.8 pall ring | 2", 14,70 m³ | Orçado 15 m³ e 2": **OK** (H9 resolvida) |
| 10.11/10.13 | Dreno DN 60 com registro esfera em cada tanque | 8 drenos (2 UASB, 2 FAS, 2 DS, 2 TC) = 10.11 (8). Duplicidade enfraquece; confirmar os 13 do 10.13. **OK com ressalva** |
| 10.12, 8.2.1, 8.2.7 | Tanque de contato: tubulação de verificação DN 20 com registro esfera | Explica os itens "resíduo"; 2 registros para 2 TC: **OK** |
| 10.1 calha | Instalada em canal de concreto, com régua limnimétrica | A cotação com caixas de entrada e saída em PRFV pode duplicar o canal (até ≈ −R$ 3,1 mil); régua não encontrada no orçamento |
| 12.1.1/12.1.2 | Separador, coletor de biogás, **defletor**, caixa distribuidora (8 saídas), anteparo de escuma, calha coletora e caixa dos amostradores de lodo, todos em PRFV | Defletor é peça distinta: risco de duplicidade do #10 cai. O 12.1.1 (projetista) inclui anteparo e calha. **Faltam no orçamento:** coletor de biogás (se não estiver no separador), caixa distribuidora, caixa dos amostradores |
| 12.1.5 acesso | UASB com **acesso superior de 0,80 m** (sem acesso lateral) | O orçamento cobra lateral + superior: lateral sem previsão no projeto (até −R$ 8.738,44 nos 2 UASB, hipótese) |
| Grupo 12 | Todos os tanques especificados como **fabricação nova** (filamento contínuo, parede 20 mm, liner epóxi, gelcoat UV). UASB Ø5,00 × 4,50 m; FAS Ø4,00 × 3,90 m; DS Ø4,00 × 3,85 m; TC Ø3,00 × 2,50 m | O orçamento trata UASB, FAS e TC como **reforma** (revestimento, gelcoat, acessos, montagem) e só o decantador como fornecimento. Contradição de escopo no grupo de R$ 493 mil. Áreas aproximadas (costado + fundo + topo): revestimento sai ≈ R$ 120/m² (UASB), R$ 157/m² (FAS), R$ 168/m² (TC), sem BDI |
| Filtro de biogás | Ø1,00 × 0,60 m em PRFV, 50 kg de carvão ativado, tubulação PVC DN 75 | **Não orçado** (lacuna L1 confirmada) |
| Preliminar | Grade inox 304 ou PRFV (2 cm, limpeza manual); caixa de areia com 2 canais e comportas de bypass em PRFV | Grade e comportas **não encontradas** na planilha do projetista |
| Automação | Quadro de comando com seletoras, alternância, alarmes; boia de nível; recomenda interligar ao gerador | Só há quadros de distribuição; quadro de comando e boia **não encontrados** |
| Decantador | Lodo recirculado para a EEE; calha coletora e fundo cônico em PRFV | Lacuna L2 parcialmente resolvida |

### 17.4 Manual de operação e manutenção (MO R00, Sanigy, julho/2025, 17 p.)
Mesmo RT, ART e contratante do memorial (17.1). Acrescenta:

| Assunto | Manual diz | Efeito |
|---|---|---|
| Vazão | 615 m³/dia (≈ 25,6 m³/h; 7,1 L/s) | Primeiro dado de vazão do projeto. TDH aproximado: 2 UASB ≈ 6,9 h; 2 FAS ≈ 3,8 h (cálculo meu, volumes do memorial) |
| Elevatória | Bombas 1+1, boias de nível, quadro elétrico de comando das bombas, troca anual do cabo de aço | Confirma 10.7 (2 bombas). Quadro de comando, boias e cabo de içamento não encontrados no orçamento |
| UASB, amostradores | 4 registros de amostragem (0,50; 1,00; 1,50; 2,00 m), dreno de fundo, dreno intermediário a 1,20 m e registro de escuma, por reator | 7 registros por UASB × 2 = 14, mais 6 drenos (2 FAS, 2 DS, 2 TC) = 20, além dos registros do tanque de lodo. Os 21 registros DN 60 (10.11 + 10.13) ficam plausíveis: a hipótese de duplicidade praticamente cai |
| **Tanque de lodo** | Recebe o lodo de excesso do UASB; sobrenadante volta à elevatória por registros em várias alturas | **Unidade não especificada no memorial e não orçada.** Lacuna nova (L15) |
| UASB | "Após a instalação do reator, teste de estanqueidade" | Reforça que o projeto prevê reator **novo** (contra a reforma orçada). Teste deve estar no comissionamento |
| Biogás | Gás "comumente queimado"; unidade de tratamento de gases com troca anual do recheio | Coerente com o filtro de biogás (carvão) do memorial, que não está orçado |
| FAS | Soprador em "casa de máquinas"; verificar "óleo e correias"; OD ≥ 2 mg/L semanal; pall ring com 100 m²/m³ | Compressor radial monobloco não tem correia: texto genérico. Casa de máquinas não verificada no orçamento (L5). **Pall ring de 14,70 m³ em 2 FAS de Ø4,00 m dá leito de ≈ 0,58 m por módulo**, baixo para filtro aerado submerso: conferir no cálculo (hipótese) |
| Decantador | Lodo por gravidade para a elevatória e daí ao UASB | Precisa de tubulação de retorno (confirmar no 8.1) |
| Desinfecção | Dosadora ≈ 12,5 L/dia (≈ 0,52 L/h); reservatório de produto de 50 L; bombona de 50 L a cada 2 dias. Cita hipoclorito de sódio e, num trecho, de cálcio | Vazão dentro da FCE (1,5 L/h). Reservatório de 50 L não orçado (L8) |
| Subprodutos sólidos | "Não contemplados no escopo do projeto" | Destinação por limpa-fossa; não é obra |

### 17.5 Memorial descritivo e de cálculo (MD R00, Sanigy, julho/2025, 69 p.)
É o documento com os cálculos que faltavam no ESP. Mesmo RT, ART e contratante. **Ele prevalece sobre o ESP onde os dois divergem.**

**Fatos principais:**
- **"Trata-se de uma ETE existente"; o projeto é de adequação, com aproveitamento das paredes dos tanques e adequação das partes internas.** Resolve a contradição da 17.3: o orçamento de **reforma** (revestimento, reforço interno, internos) está coerente com o projeto. O texto de "fabricação" do ESP é genérico.
- Vazão 615 m³/d (média), 1.107 m³/d (máxima, 46,1 m³/h). Base: projeto Sanevias de 2011 e dados do contratante (12.300 hab. equivalentes × 50 L/d). DBO 900 mg/L, DQO 1.800 mg/L.
- **UASB:** 2 módulos Ø5,00 × 4,50 m; separador trifásico Ø3,00 m; coletor de gases Ø1,20 m; **8 distribuidores por módulo**; biogás 126 m³/d. A taxa de aplicação superficial calculada (1,25 m³/m²·h) passa do limite que o próprio memorial atribui à NBR 12209 (1,20); o memorial reconhece e justifica.
- **FAS:** 2 módulos Ø4,00 × 3,90 m. **Pall ring: 30% do volume útil de 49,01 m³ = 14,70 m³ — o volume útil é de um módulo**, então o total para 2 módulos seria 29,40 m³.
- **Demanda de ar:** 7.865 Nm³/d = **5,46 Nm³/min (≈ 328 m³/h)**. Potência calculada 5,29 kW com descarga a 1,5 atm (≈ 5,2 m.c.a.). Compressor adotado: **CRC-2 820 36 TD HE (Asten), 10,33 m³/min, 16,9 cv, pressão máxima 4,70 m.c.a.**, com filtro de entrada e válvula de alívio. Quantidade não informada.
- **Difusores:** Vagalhões P-250 EPDM, 9 m³/h, **70 por módulo, 140 no total**. O cálculo não liga o número à demanda: 328 m³/h ÷ 9 m³/h = 37 difusores.
- **Decantador:** Ø4,00 m, lâmina 3,85 m (cilindro 1,55 + cone 2,30). O texto diz "1 módulo", mas a conta usa 2 (só fecha com 2): coerente com os 2 do orçamento.
- **Tanque de contato:** calculado como **um** tanque Ø3,00 × 2,50 m com a vazão total (TDH 82,75 min).
- **Elevatória:** recalque PVC DN 110, 29 m, Hman 13,0 m; perda de carga com 1 registro de gaveta e 2 retenções por bomba. Bomba Brava E30 3 cv adotada embora o cálculo dê 6,02 cv; o memorial diz que, nos picos, a bomba reserva entra junto.
- **Desinfecção:** hipoclorito 12%, cloro residual 5 mg/L, ≈ 1,04 L/h, bombona de 50 L a cada 2 dias.
- **Filtro de biogás:** Ø1,00 × 0,60 m, 50 kg de carvão. O cálculo de H₂S usa densidade de gás em kg/L (1.000× maior) e chega a troca do carvão a cada 7 dias; o manual fala em troca anual.

**Efeito nos itens:**

| Item | Antes | Agora | Impacto (c/ BDI) |
|---|---|---|---|
| Grupo 12 (escopo) | Contradição tanque novo × reforma | **Resolvida:** reforma de tanques existentes, como orçado | — |
| 10.8 pall ring (15 m³) | OK | **Provável insuficiência:** 14,70 m³ é por módulo; total 29,40 m³ | até **+R$ 20.419,34** (14,4 m³ a R$ 1.418,01): abaixo, risco para a contratada |
| 12.3.x tanque de contato (×2) | OK | **A confirmar:** o cálculo prevê **1** tanque; o 10.12 da planilha do projetista também tem 1 | até **−R$ 25.641,92** (metade de 12.3.1 a 12.3.5), além do frete do 12.3.6 |
| 10.4 + acessórios (140) | OK com ressalva | **Quantidade sem justificativa no cálculo** (37 pela demanda de ar); pode haver critério de distribuição em planta não escrito | cada 100 pontos a menos ≈ −R$ 35.548,00 (difusor + tê + bucha + luva + adaptador) |
| 10.3 soprador (×2) | NÃO OK | Modelo de projeto é o CRC-2 820; o ESP diz que já existe. A conta de potência supõe 5,2 m.c.a., acima do máximo do modelo (4,70); com 3,90 m de água sobre os difusores, falta a vazão na curva a ≈ 4,3–4,5 m.c.a. O JQT-7500 cotado (máx. ≈ 4,08 m.c.a.) provavelmente não atende | — |
| 10.5 filtro (5 m³/min) | NÃO OK | Abaixo da demanda (5,46 Nm³/min) e da vazão máxima do compressor (10,33) | — |
| 10.10, 10.16, 10.17 | — | 2 bombas × (1 gaveta + 2 retenções) = 2 gavetas e 4 retenções; o orçamento tem 3 gavetas e 4 retenções | 1 gaveta a confirmar |
| L14 caixa distribuidora | Lacuna | 8 distribuidores por UASB no cálculo; segue sem item no orçamento | — |
| L15 tanque de lodo | Lacuna | O cálculo dá volume de lodo para desaguamento (193,7 kg SS/d) mas não dimensiona tanque de lodo | — |

---

## 18. Sessão 2 (até 20/10/2026): apontamentos do fiscal e administração local

### 18.1 Apontamentos feitos pelo usuário (planilha analisada, coluna I)
| Item | Apontamento | Impacto c/ BDI |
|---|---|---|
| 1.16 | Excluir engenheiro civil da composição (já remunerado na administração local) | −6.030,57 (item passa a R$ 2.012,56) |
| 10.3 | Item cotado diverge do descrito (print JQT-7500 × CRC 2820; ESP diz que o CRC 2820 já existe) | não quantificado |
| 12.1.1 | BDI trocado → aquisição (montagem no 12.1.6) | −2.301,98 |
| 12.1.2 | BDI trocado → aquisição (montagem no 12.1.6) | −2.151,88 |
| 12.3.6 | Frete dobrado (proposta Biomais prevê 1) + BDI trocado | −2.081,10 |
| 12.4.1 | BDI trocado → aquisição (ressalva: proposta diz "fornecimento e instalação") | −17.932,38 |
| 12.4.2 | BDI trocado → aquisição | −1.246,30 |
Base legal conferida no texto oficial: Decreto 7.983/2013, art. 9º §§ 1º e 2º (Planalto); Acórdão 2622/2013-TCU-Plenário, itens 9.1, 9.2.1, 9.2.2 e 9.3.2.2 (texto recebido do usuário). O acórdão traz faixas de referência ("mero fornecimento": 11,10/14,02/16,80%; redes de água e esgoto: 20,76/24,18/26,44%) e mostra que no fornecimento administração central e risco existem, mas menores.

### 18.2 Administração local (itens 2.1 a 2.6, planilha analisada `ORÇAMENTO ETE. BARROS 062025 VENTO SUL.xlsx`, reanexada em 16/10)
Grupo 2 = R$ 550.127,97 (projetista: R$ 257.594,19). 7 meses em todos os itens; cronograma de 6 meses (1/6 por mês). Adm. local = 23,35% do custo direto (TCU 3º quartil 10,89%; projetista declara 14,74%).
| Item | Profissional | Fonte | R$/mês sem BDI | SINAPI-PA 06/2025 | Problema |
|---|---|---|---|---|---|
| 2.1 | Eng. civil pleno | SINAPI 93567 | 21.449,62 | 21.449,62 | OK |
| 2.2 | Eletrotécnico | COMP-01 | 9.662,43 | 101401: 5.586,93 | composição própria com código SINAPI existente; salário 4.350 sem fonte; encargos 53,45% sobre base com complementares |
| 2.3 | Almoxarife | "SINAPI" 93563 | 5.149,80 | 3.971,64 | + alimentação 988,66 + transporte 189,50 (o SINAPI 93563 não inclui) |
| 2.4 | Encarregado geral | COMP-02 | 10.210,71 | 93572: 4.106,99 | idem 2.2; salário 5.000 sem fonte; transporte na base dos encargos sem linha |
| 2.5 | Aux. técnico eng. | "SINAPI" 101390 | 5.969,80 | 4.791,64 | idem 2.3 |
| 2.6 | Téc. edificações | COMP-03 (planilha diz COMP-04) | 9.240,18 | 100534: 3.781,36 | idem 2.2 |
Impacto c/ BDI: preços SINAPI em 7 meses −160.486,41; SINAPI e 6 meses −216.149,49. O usuário optou por manter salários acima do SINAPI (retenção de pessoal): exige relatório técnico do art. 8º, parágrafo único, do Decreto 7.983/2013, com fontes de mercado; os erros de método (base dos encargos, rótulo SINAPI, inconsistências) precisam ser corrigidos de qualquer forma.

### 18.3 Próximo passo combinado
O usuário enviará (1) a planilha com os apontamentos para a contratada e (2) a planilha devolvida pela contratada. Conferir, item a item, se cada apontamento foi atendido, se a correção foi feita na base oculta `PL_Base_062025` (a aba visível calcula por PROCV), se não surgiram erros novos e se o resultado continua coerente com a planilha do projetista e com o memorial (MD/ESP/MO).
