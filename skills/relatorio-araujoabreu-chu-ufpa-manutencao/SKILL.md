---
name: relatorio-araujoabreu-chu-ufpa-manutencao
description: Gera o Relatório de Avaliação de Serviços (IMR) mensal do contrato de manutenção do CHU-UFPA/EBSERH (rede de ar comprimido, refrigeração etc.), a partir do PDF de folha de ponto/frequência dos funcionários e de dados fornecidos manualmente (chamados corretivos, manutenções preventivas, OF/OS, mão de obra). Use esta skill sempre que o usuário mencionar "relatório de fiscalização", "folha de ponto", "frequência dos funcionários", "indicador de disponibilidade/DSC", "glosa", "IMR", "OF/OS do contrato", ou pedir para apurar faltas de funcionários, fazer a "análise da frequência"/"relatório de faltas" do mês, ou calcular o valor devido no mês — mesmo que ele não peça explicitamente por "usar a skill". Também use para checar/atualizar o calendário de dias úteis (feriados de Belém-PA) usado no cálculo.
---

# Fiscalização mensal — contrato de manutenção CHU-UFPA

Gera o relatório mensal de avaliação de serviços (RC, PMP e DSC) exigido pelo IMR do contrato,
a partir da folha de ponto em PDF + dados que o fiscal informa manualmente (chamados corretivos,
preventivas, OF/OS). O resultado final é um `.docx` no layout do modelo SEI do CHU-UFPA.

**Por que isso importa:** o indicador 3 (DSC) e as faltas de funcionários são a parte mais
trabalhosa e sujeita a erro manual do relatório — cruzar dezenas de páginas de ponto, aplicar
a regra de "falta conta independente do motivo", achar dias com menos de 6h de jornada, e ainda
descontar corretamente sábado/domingo/feriado. Esta skill automatiza essa parte e deixa os outros
dois indicadores (que dependem de números que só o fiscal tem) prontos pra preencher.

## Fluxo completo (siga nesta ordem)

Dependências Python: `pip install pdfplumber openpyxl` (se faltarem no ambiente).

### Passo 1 — Extrair a folha de ponto do PDF
```bash
python3 scripts/extract_ponto.py <caminho_do_pdf_de_ponto> --out ponto_extraido.json
```
Isso lê o PDF por coordenadas de texto (robusto a colunas que aparecem/somem entre funcionários,
como a coluna "Saldo") e gera um JSON com um registro por colaborador por dia: horários, horas
normais e o texto de Motivo/Observação.

**Sempre confira o `stderr`** — ele informa quantos funcionários foram extraídos. Se alguma
página não foi reconhecida, o JSON avisa com `"aviso": "cabeçalho de tabela não localizado nesta
página"` — avise o usuário antes de prosseguir. É normal o ponto ter mais gente que a relação
(outros contratos, coberturas): quem fica fora da relação é tratado no Passo 2.

**A Relação de Funcionários do mês é obrigatória** (planilha .xlsx/.csv da contratada, com
colunas NOME FUNCIONÁRIO, FUNÇÃO, DATA ADMISSÃO, DEMISSÃO, OBSERVAÇÃO). Se o usuário não mandou,
peça antes do Passo 2. Se vier como imagem/texto, monte você mesmo um .csv com essas colunas.

### Passo 2 — Calcular dias úteis, faltas e o indicador 3 (DSC)
```bash
python3 scripts/calc_indicador3.py ponto_extraido.json --mes 7 --ano 2026 \
    --feriados references/feriados_belem.json \
    --horas-dia 8.8 --qtd-funcionarios 27 \
    --relacao <relacao_funcionarios.xlsx> \
    --out indicador3.json
```
Regras de negócio já embutidas (confirmadas com o usuário, não pergunte de novo):
- Dia útil = seg-sex, excluindo feriados nacionais/estaduais/municipais de Belém-PA
  (`references/feriados_belem.json` — **antes de usar num ano novo, confira/atualize esse
  arquivo**, ele foi compilado até 2026).
- **Falta cheia (1,0)**: `horas_normais == 00:00` num dia útil, **qualquer que seja o motivo**
  (atestado médico, licença, liberação do cliente etc. contam igual — só o motivo e a data
  ficam registrados, não isentam a falta).
- **Meia falta (0,5)**: `horas_normais < 06:00` num dia útil (ex: foi à consulta de manhã, só
  trabalhou a tarde).
- Sábado, domingo e feriado **nunca contam**, mesmo que o motivo do ponto diga outra coisa.

- **Só quem está na relação conta.** Com `--relacao`, o script casa cada nome da relação com o
  ponto (tolera nomes do meio abreviados, ex: "EUTHYMIOS M D S PAPASPIROPOULO" = "EUTHYMIOS MAX
  DA SILVA PAPASPIROPAULOS"; não casa nomes ambíguos). Quem está no ponto e fora da relação vai
  pra `fora_da_relacao` e **não entra** no total nem nas tabelas — só é informado.
- Observação da relação: "Aditivo" = posto do Termo Aditivo; "Aditivo (Fulano)" = o ponto do
  posto está registrado sob o nome "Fulano" (usa as faltas do Fulano); "Cobrir faltas" = função
  de cobertura.
- Dias antes da admissão não contam; dias depois do desligamento contam e saem marcados como
  "sem motivo (pós-desligamento)".

### Passo 2b — Entregar a análise de frequência (as duas tabelas)
```bash
python3 scripts/gerar_tabelas_frequencia.py indicador3.json
```
Imprime duas tabelas em texto separado por TAB. **Esta é a saída da análise de frequência:**
responda no chat com cada tabela num bloco de código (```` ``` ````) copiado **exatamente** como
o script imprimiu (sem converter pra tabela Markdown, sem trocar TAB por espaço), e diga pro
usuário colar na célula A1 do Excel. **Não gere arquivo** (.xlsx/.docx) pra isso, a não ser que
ele peça.

1. **ANÁLISE DA FREQUÊNCIA** — todos da relação, ordem alfabética: Nome | Função | Observação |
   SUBSTITUTO (SUBSTITUTO fica vazio; o fiscal preenche).
2. **RELATÓRIO DE FALTAS MÊS <MÊS>** — quem teve falta, quem não consta no ponto (Faltas em
   branco + "verificar"), quem cobre faltas, postos do Termo Aditivo e desligados; ordem
   decrescente de faltas: Funcionário | Função | Faltas (0,00) | Detalhe. No fim, uma linha
   SUBTOTAL por função e a linha TOTAL.

Férias contam como falta (regra do contrato — confirmado com o usuário). Depois das tabelas,
liste em poucas linhas: o total de faltas, o DSC sugerido (do `indicador3.json`), quem está na
relação e não consta no ponto, e quem está no ponto fora da relação (com as faltas que teria —
só informativo). Isso sai do `stderr` do script.

**O total de faltas é uma SUGESTÃO.** O usuário decide o número que efetivamente entra na fórmula
do DSC (pode reduzir por compensação, erro de ponto etc.). Não siga pro relatório final sem essa
confirmação.

**Atenção a anomalias**: "sem motivo, com marcação de ponto (verificar)" no Detalhe = dia com
horas normais 00:00, sem motivo, mas com horário registrado — sinalize como possível erro no
sistema de ponto. "sem registro de ponto e sem motivo" = nenhuma marcação no dia (ausência
injustificada no sistema).

Os Passos 3 a 5 só rodam se o usuário pedir o relatório completo (IMR/.docx); quando o pedido é
só "análise da frequência", pare aqui.

### Passo 3 — Reunir os dados que só o fiscal sabe
Pergunte ao usuário (ou use o que ele já mandou na conversa) pra preencher um JSON no formato de
`assets/dados_mes.exemplo.json`:
- `indicador1`: NCC (chamados corretivos totais) e NMC (realizados)
- `indicador2`: MP (preventivas planejadas) e ME (executadas)
- `indicador3.total_faltas_final_revisado`: o número que o usuário decidiu no Passo 2
- `mao_de_obra.valor_mensal_base`: valor vigente (confira `references/composicao_mao_obra.json`;
  atualize esse arquivo quando houver Termo Aditivo)
- `mao_de_obra.descontos_vaga_nao_substituida` (opcional): lista de
  `{"cargo": "...", "valor_mensal_do_cargo": ..., "dias_sem_substituto": ...}` — só quando um
  funcionário foi desligado/afastado sem substituto no mês
- `of_os`: lista de `{"numero": "OF 168", "valor": 28558.25}`
- `identificacao`: mês, ano, número do contrato, contratada, número do relatório SEI, processo
  SEI, anexos SEI

### Passo 4 — Consolidar os 3 indicadores e calcular o valor final
```bash
python3 scripts/calc_relatorio.py dados_mes.json --out relatorio_final.json
```
Aplica as faixas de ajuste/glosa de cada indicador, soma o VDT (Percentual Total de Desconto
Mensal = soma dos percentuais de desconto dos 3 indicadores, aplicado sobre o valor fixo da mão
de obra), aplica desconto por vaga não substituída separadamente, e calcula o valor total do mês.
Leia os `alertas` no JSON de saída (ex: DSC abaixo de 90% implica risco de rescisão contratual —
mostre isso com destaque pro usuário, nunca esconda).

### Passo 5 — Gerar o relatório final em .docx
```bash
node scripts/gerar_docx.js relatorio_final.json /mnt/user-data/outputs/relatorio_fiscalizacao_MM_AAAA.docx indicador3.json
```
O terceiro argumento (`indicador3.json`) é opcional — se passado, anexa ao final do documento
uma tabela auditável com todas as faltas consideradas (funcionário, data, tipo, motivo), útil
pra defender o número usado se questionado depois.

Depois de gerar, **sempre verifique visualmente antes de entregar** (mesmo processo do skill de
docx): converta pra PDF e olhe as páginas renderizadas.
```bash
python3 /mnt/skills/public/docx/scripts/office/soffice.py --headless --convert-to pdf relatorio_fiscalizacao_MM_AAAA.docx
pdftoppm -jpeg -r 100 relatorio_fiscalizacao_MM_AAAA.pdf page
```
Leia as imagens geradas antes de apresentar o arquivo ao usuário.

## Coisas que você NÃO deve fazer sozinho
- Não inclua nas tabelas nem no total quem não está na Relação de Funcionários do mês.
- Não decida sozinho o número final de faltas que entra no indicador 3 — é sempre revisão manual
  do usuário (ver Passo 2).
- Não invente números de NCC/NMC/ME/MP, valores de OF/OS ou números SEI — pergunte, eles vêm de
  fora do ponto.
- Não aplique um "ponto facultativo" federal (Carnaval, Corpus Christi etc.) como dia não-útil por
  padrão — só se o usuário confirmar que a EBSERH/CHU-UFPA observa esse ponto facultativo (use
  `--incluir-pontos-facultativos` nesse caso).

## Arquivos desta skill
- `scripts/extract_ponto.py` — extrai a folha de ponto do PDF (por coordenadas de texto)
- `scripts/relacao.py` — lê a Relação de Funcionários e casa os nomes com o ponto
- `scripts/calc_indicador3.py` — dias úteis, faltas/meias faltas, indicador DSC (só quem está na relação)
- `scripts/gerar_tabelas_frequencia.py` — as duas tabelas da análise de frequência (TAB, pra colar no Excel)
- `scripts/calc_relatorio.py` — consolida os 3 indicadores, VDT, valor final
- `scripts/gerar_docx.js` — gera o `.docx` final no layout do modelo SEI
- `references/feriados_belem.json` — calendário de feriados (atualizar todo ano)
- `references/composicao_mao_obra.json` — tabela de custo por posto de trabalho (atualizar por Termo Aditivo)
- `assets/dados_mes.exemplo.json` — modelo do JSON de entrada manual do Passo 3
