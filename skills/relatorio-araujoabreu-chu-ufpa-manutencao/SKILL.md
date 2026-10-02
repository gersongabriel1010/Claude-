---
name: relatorio-araujoabreu-chu-ufpa-manutencao
description: Gera o Relatório de Avaliação de Serviços (IMR) mensal do contrato de manutenção do CHU-UFPA/EBSERH (rede de ar comprimido, refrigeração etc.), a partir do PDF de folha de ponto/frequência dos funcionários e de dados fornecidos manualmente (chamados corretivos, manutenções preventivas, OF/OS, mão de obra). Use esta skill sempre que o usuário mencionar "relatório de fiscalização", "folha de ponto", "frequência dos funcionários", "indicador de disponibilidade/DSC", "glosa", "IMR", "OF/OS do contrato", ou pedir para apurar faltas de funcionários e calcular o valor devido no mês — mesmo que ele não peça explicitamente por "usar a skill". Também use para checar/atualizar o calendário de dias úteis (feriados de Belém-PA) usado no cálculo.
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

### Passo 1 — Extrair a folha de ponto do PDF
```bash
python3 scripts/extract_ponto.py <caminho_do_pdf_de_ponto> --out ponto_extraido.json
```
Isso lê o PDF por coordenadas de texto (robusto a colunas que aparecem/somem entre funcionários,
como a coluna "Saldo") e gera um JSON com um registro por colaborador por dia: horários, horas
normais e o texto de Motivo/Observação.

**Sempre confira o `stderr`** — ele informa quantos funcionários foram extraídos. Se o número
não bater com o esperado (ex: a lista de funcionários enviada pelo usuário), avise o usuário
antes de prosseguir; pode ser que a página não tenha sido reconhecida (avisa no JSON com
`"aviso": "cabeçalho de tabela não localizado nesta página"`).

### Passo 2 — Calcular dias úteis, faltas e o indicador 3 (DSC)
```bash
python3 scripts/calc_indicador3.py ponto_extraido.json --mes 7 --ano 2026 \
    --feriados references/feriados_belem.json \
    --horas-dia 8.8 --qtd-funcionarios 27 \
    [--employee-list lista_funcionarios.json] \
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

Se o usuário fornecer uma lista de funcionários esperados (imagem, Excel ou texto — extraia os
nomes você mesmo se vier como imagem/Excel), passe em `--employee-list` como um JSON de lista de
nomes (`["FULANO DA SILVA", ...]`) pra conferência automática de quem está/não está no ponto.

**O total de faltas calculado aqui é uma SUGESTÃO.** Sempre mostre pro usuário a lista de faltas
por funcionário (o campo `funcionarios[].faltas`) e o total sugerido antes de seguir pro relatório
final — ele decide manualmente o número que efetivamente entra na fórmula (pode reduzir por causa
de alguma compensação, erro de ponto, etc.). Não pule essa revisão.

**Atenção a anomalias**: se aparecer um dia com `horas_normais: "00:00"` e `motivo: ""` (vazio)
apesar de ter horário de entrada/saída registrado, isso é estranho — sinalize pro usuário como
possível erro no sistema de ponto, não uma falta real óbvia.

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
- Não decida sozinho o número final de faltas que entra no indicador 3 — é sempre revisão manual
  do usuário (ver Passo 2).
- Não invente números de NCC/NMC/ME/MP, valores de OF/OS ou números SEI — pergunte, eles vêm de
  fora do ponto.
- Não aplique um "ponto facultativo" federal (Carnaval, Corpus Christi etc.) como dia não-útil por
  padrão — só se o usuário confirmar que a EBSERH/CHU-UFPA observa esse ponto facultativo (use
  `--incluir-pontos-facultativos` nesse caso).

## Arquivos desta skill
- `scripts/extract_ponto.py` — extrai a folha de ponto do PDF (por coordenadas de texto)
- `scripts/calc_indicador3.py` — dias úteis, faltas/meias faltas, indicador DSC
- `scripts/calc_relatorio.py` — consolida os 3 indicadores, VDT, valor final
- `scripts/gerar_docx.js` — gera o `.docx` final no layout do modelo SEI
- `references/feriados_belem.json` — calendário de feriados (atualizar todo ano)
- `references/composicao_mao_obra.json` — tabela de custo por posto de trabalho (atualizar por Termo Aditivo)
- `assets/dados_mes.exemplo.json` — modelo do JSON de entrada manual do Passo 3
