// Gera o Relatório de Avaliação de Serviços (.docx) no layout do modelo SEI/CHU-UFPA,
// a partir do JSON produzido por calc_relatorio.py (e, opcionalmente, do indicador3.json
// de calc_indicador3.py, pra anexar a lista de faltas consideradas).
//
// Uso: node gerar_docx.js <relatorio_final.json> <saida.docx> [indicador3.json]

const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  HeadingLevel, AlignmentType, WidthType, ShadingType, BorderStyle, VerticalAlign,
} = require("docx");

const [, , dadosPath, outPath, indicador3Path] = process.argv;
if (!dadosPath || !outPath) {
  console.error("Uso: node gerar_docx.js <relatorio_final.json> <saida.docx> [indicador3.json]");
  process.exit(1);
}
const d = JSON.parse(fs.readFileSync(dadosPath, "utf-8"));
const ind3detalhe = indicador3Path ? JSON.parse(fs.readFileSync(indicador3Path, "utf-8")) : null;

const MESES = ["", "JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO",
  "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"];

const id = d.identificacao || {};
const mesNome = MESES[id.mes] || "";
const fmtBRL = (v) => v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

// ---------- helpers de estilo ----------
const TABLE_WIDTH = 9350; // dxa (~6.5in)

function p(text, opts = {}) {
  return new Paragraph({
    alignment: opts.align || AlignmentType.JUSTIFIED,
    spacing: { after: 120 },
    children: [new TextRun({ text, bold: !!opts.bold, italics: !!opts.italics, size: opts.size || 22 })],
  });
}

function heading(text, level = HeadingLevel.HEADING_1) {
  return new Paragraph({ heading: level, spacing: { before: 200, after: 120 }, children: [new TextRun({ text, bold: true })] });
}

function cell(text, opts = {}) {
  return new TableCell({
    width: { size: opts.width || 2000, type: WidthType.DXA },
    shading: opts.shaded ? { type: ShadingType.CLEAR, fill: "D9E2C8" } : undefined,
    verticalAlign: VerticalAlign.CENTER,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({
      alignment: opts.align || AlignmentType.LEFT,
      children: [new TextRun({ text, bold: !!opts.bold, size: 20 })],
    })],
  });
}

function tabelaIndicador(titulo, campos) {
  // campos: array de [label, valor] — cada um vira uma linha de 2 colunas (25% / 75%)
  const larguraLabel = Math.round(TABLE_WIDTH * 0.28);
  const larguraValor = TABLE_WIDTH - larguraLabel;
  const rows = [
    new TableRow({
      children: [cell(titulo, { width: TABLE_WIDTH, shaded: true, bold: true, align: AlignmentType.CENTER })],
    }),
  ];
  // a primeira linha precisa ocupar as duas colunas — recriamos com colSpan
  rows[0] = new TableRow({
    children: [new TableCell({
      width: { size: TABLE_WIDTH, type: WidthType.DXA },
      columnSpan: 2,
      shading: { type: ShadingType.CLEAR, fill: "D9E2C8" },
      children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: titulo, bold: true, size: 20 })] })],
    })],
  });
  for (const [label, valor] of campos) {
    rows.push(new TableRow({
      children: [
        cell(label, { width: larguraLabel, bold: true }),
        cell(valor, { width: larguraValor }),
      ],
    }));
  }
  return new Table({ width: { size: TABLE_WIDTH, type: WidthType.DXA }, columnWidths: [larguraLabel, larguraValor], rows });
}

// ---------- Indicadores (texto fixo do IMR / Termo de Referência) ----------
const rc = d.indicador1_rc, pmp = d.indicador2_pmp, dsc = d.indicador3_dsc;

const tabelaInd1 = tabelaIndicador("INDICADOR 01 - EFETIVIDADE DE ATENDIMENTO — RENDIMENTO CORRETIVO (RC)", [
  ["FINALIDADE", "Garantir, quantitativamente, o pagamento proporcional ao rendimento corretivo da contratada."],
  ["META A CUMPRIR", "95% com tolerância de 2%"],
  ["INSTRUMENTO DE MEDIÇÃO", "Ordens de Serviço"],
  ["MECANISMO DE CÁLCULO", "RC = (NMC / NCC) x 100"],
  ["FAIXAS DE AJUSTE (GLOSA)", "93% ≤ RC — sem redução | 85% ≤ RC < 93% — redução de 2% | RC < 85% — redução de 5%"],
]);

const tabelaInd2 = tabelaIndicador("INDICADOR 02 – PERFORMANCE DE MANUTENÇÃO PROGRAMADA (PMP)", [
  ["FINALIDADE", "Garantir a execução, pela CONTRATADA, dos serviços previstos no PMOC."],
  ["META A CUMPRIR", "95% com tolerância de 2%"],
  ["INSTRUMENTO DE MEDIÇÃO", "Check lists de manutenção preventiva executada e atestada pela fiscalização"],
  ["MECANISMO DE CÁLCULO", "PMP = (ME / MP) x 100"],
  ["FAIXAS DE AJUSTE (GLOSA)", "93% ≤ PMP — sem redução | 85% ≤ PMP < 93% — redução de 2% | PMP < 85% — redução de 5%"],
]);

const tabelaInd3 = tabelaIndicador("INDICADOR 03 – DISPONIBILIDADE DOS SERVIÇOS CONTRATADOS (DSC)", [
  ["FINALIDADE", "Garantir a prestação contínua dos serviços contratados."],
  ["META A CUMPRIR", "Produtividade de referência = 100% das horas trabalhadas conforme a jornada prevista no mês"],
  ["INSTRUMENTO DE MEDIÇÃO", "Folhas de ponto"],
  ["MECANISMO DE CÁLCULO", "DSC (%) = HT / HPR x 100"],
  ["FAIXAS DE AJUSTE", "≥98% sem desconto | <98% desconto de 5% | <95% desconto de 10% | <90% desconto de 20% + rescisão contratual"],
]);

// ---------- Resultados (3.1, 3.2, 3.3) ----------
const atendeuTexto = (atendeu) => atendeu
  ? "a empresa contratada atendeu a meta do indicador."
  : "a empresa contratada NÃO atendeu a meta do indicador.";

const resultado31 = [
  p("3.1. Para a avaliação do Indicador 1 - Efetividade de atendimento (Rendimento Corretivo)."),
  p(`RC = (NMC / NCC) x 100 = (${rc.nmc} / ${rc.ncc}) x 100 = ${rc.resultado_percentual}%`, { bold: true }),
  p(`Com o resultado obtido, ${atendeuTexto(rc.atendeu_meta)}${rc.sancao ? " Sanção prevista: " + rc.sancao + "." : ""}`),
];

const resultado32 = [
  p("3.2. Para a avaliação do Indicador 2 - Performance de Manutenção Programada."),
  p(`PMP = (ME / MP) x 100 = (${pmp.me} / ${pmp.mp}) x 100 = ${pmp.resultado_percentual}%`, { bold: true }),
  p(`Com o resultado obtido, ${atendeuTexto(pmp.atendeu_meta)}${pmp.sancao ? " Sanção prevista: " + pmp.sancao + "." : ""}`),
];

const resultado33 = [
  p("3.3. Para a avaliação do Indicador 3 - Disponibilidade dos Serviços Contratados."),
  p(`Foram consideradas as folhas de ponto dos funcionários. Parâmetros: ${dsc.horas_trabalho_dia}h/dia x `
    + `${dsc.quantidade_funcionarios} funcionários x ${dsc.dias_uteis_no_mes} dias úteis = HPR de ${dsc.HPR}h. `
    + `Faltas/ausências consideradas: ${dsc.total_faltas_considerado} dia(s). `
    + `HT = HPR − (faltas x horas/dia) = ${dsc.HT}h.`),
  p(`DSC (%) = HT / HPR x 100 = ${dsc.HT} / ${dsc.HPR} x 100 = ${dsc.resultado_percentual}%`, { bold: true }),
  p(`Com o resultado obtido, ${atendeuTexto(dsc.atendeu_meta)}`),
];

// ---------- Seção 4: valores ----------
const linhasOfOs = (d.of_os || []).map(item => new TableRow({
  children: [cell(item.numero, { width: Math.round(TABLE_WIDTH * 0.6) }), cell(fmtBRL(item.valor), { width: Math.round(TABLE_WIDTH * 0.4), align: AlignmentType.RIGHT })],
}));
const tabelaOfOs = new Table({
  width: { size: TABLE_WIDTH, type: WidthType.DXA },
  columnWidths: [Math.round(TABLE_WIDTH * 0.6), Math.round(TABLE_WIDTH * 0.4)],
  rows: [
    new TableRow({ children: [cell("Nº OF/OS", { bold: true, shaded: true, width: Math.round(TABLE_WIDTH * 0.6) }), cell("Valor (R$)", { bold: true, shaded: true, align: AlignmentType.RIGHT, width: Math.round(TABLE_WIDTH * 0.4) })] }),
    ...linhasOfOs,
    new TableRow({ children: [cell("Total Geral (OF + OS)", { bold: true, width: Math.round(TABLE_WIDTH * 0.6) }), cell(fmtBRL(d.total_of_os), { bold: true, align: AlignmentType.RIGHT, width: Math.round(TABLE_WIDTH * 0.4) })] }),
  ],
});

const descontosVagaTexto = (d.mao_de_obra.descontos_vaga_nao_substituida || []).length
  ? d.mao_de_obra.descontos_vaga_nao_substituida.map(dv =>
      `${dv.cargo || "Cargo não informado"}: ${dv.dias_sem_substituto} dia(s) sem substituto — desconto de ${fmtBRL(dv.valor_descontado)}.`
    ).join(" ")
  : null;

const secao4 = [
  heading("4. VALOR CORRESPONDENTE AO CUSTO DOS SERVIÇOS", HeadingLevel.HEADING_1),
  p("4.1. Valor referente à mão de obra"),
  p(`Valor mensal base da mão de obra (Tabela de Composição de Valores do Contrato): ${fmtBRL(d.mao_de_obra.valor_base)}.`),
  p(`VDT (Percentual Total de Desconto Mensal) apurado: ${d.vdt_percentual_total_desconto}%`
    + (d.vdt_percentual_total_desconto > 0 ? ` — valor após VDT: ${fmtBRL(d.mao_de_obra.apos_vdt)}.` : " — não se aplica desconto.")),
  ...(descontosVagaTexto ? [p(`Desconto adicional por vaga não substituída (proporcional, apurado separadamente do VDT): ${descontosVagaTexto} Total: ${fmtBRL(d.mao_de_obra.total_desconto_vaga)}.`)] : []),
  p(`Valor final da mão de obra no mês: ${fmtBRL(d.mao_de_obra.valor_final)}.`, { bold: true }),
  p("4.2. Valor referente ao fornecimento de materiais (OF) e serviços (OS)"),
  tabelaOfOs,
  p("4.3. Valor total"),
  p(`Valor total = Valor da mão de obra + Valor de OF/OS = ${fmtBRL(d.mao_de_obra.valor_final)} + ${fmtBRL(d.total_of_os)} = ${fmtBRL(d.valor_total_do_mes)}`, { bold: true }),
];

// ---------- Seção 6 ----------
const secao6 = [
  heading("6. INDICAÇÃO DOS VALORES DEVIDOS", HeadingLevel.HEADING_1),
  p(d.vdt_percentual_total_desconto > 0
    ? `Considerando as avaliações dos indicadores, aplica-se o VDT de ${d.vdt_percentual_total_desconto}% sobre a parcela fixa da mão de obra. O valor total devido no mês corresponde ao montante de ${fmtBRL(d.valor_total_do_mes)}.`
    : `Considerando as avaliações dos indicadores, o Percentual Total de Desconto Mensal (VDT) não se aplica. O valor total devido no mês corresponde ao montante de ${fmtBRL(d.valor_total_do_mes)}.`),
];

// ---------- Anexo: lista de faltas consideradas (se indicador3.json foi passado) ----------
let anexoFaltas = [];
if (ind3detalhe) {
  const linhas = [];
  for (const f of ind3detalhe.funcionarios) {
    if (f.total_faltas > 0) {
      for (const falta of f.faltas) {
        linhas.push(new TableRow({
          children: [
            cell(f.colaborador, { width: 2800 }),
            cell(falta.data, { width: 1200 }),
            cell(falta.tipo, { width: 1600 }),
            cell(falta.motivo, { width: 3750 }),
          ],
        }));
      }
    }
  }
  anexoFaltas = [
    new Paragraph({ children: [], pageBreakBefore: true }),
    heading("ANEXO — LISTA DE FALTAS/AUSÊNCIAS CONSIDERADAS NO INDICADOR 3", HeadingLevel.HEADING_1),
    p("Lista gerada automaticamente a partir da folha de ponto para fins de conferência. O total de faltas "
      + "efetivamente utilizado no cálculo do indicador foi revisado manualmente pelo fiscal do contrato."),
    new Table({
      width: { size: TABLE_WIDTH, type: WidthType.DXA },
      columnWidths: [2800, 1200, 1600, 3750],
      rows: [
        new TableRow({ children: [
          cell("Colaborador", { bold: true, shaded: true, width: 2800 }),
          cell("Data", { bold: true, shaded: true, width: 1200 }),
          cell("Tipo", { bold: true, shaded: true, width: 1600 }),
          cell("Motivo (registrado no ponto)", { bold: true, shaded: true, width: 3750 }),
        ] }),
        ...linhas,
      ],
    }),
  ];
}

// ---------- Documento ----------
const doc = new Document({
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 } } }, // A4
    children: [
      p("COMPLEXO HOSPITALAR UNIVERSITÁRIO DA UNIVERSIDADE FEDERAL DO PARÁ", { align: AlignmentType.CENTER, bold: true }),
      p("Rua dos Mundurucus, nº 4487 - Bairro Guamá", { align: AlignmentType.CENTER }),
      p("Belém-PA, CEP 66073-000", { align: AlignmentType.CENTER }),
      p("- http://chu-ufpa.hubrasil.gov.br", { align: AlignmentType.CENTER }),
      p(`Relatório - SEI nº ${id.numero_relatorio_sei || "[preencher número SEI]"}`, { bold: true }),
      p("Belém, data da assinatura eletrônica", { align: AlignmentType.RIGHT }),
      p(`Assunto: RELATÓRIO DE AVALIAÇÃO DE SERVIÇOS REFERENTE AO MÊS DE ${mesNome}_${id.ano} - CONTRATO N° ${id.contrato || "[preencher]"}.`, { bold: true }),

      heading("1. INTRODUÇÃO", HeadingLevel.HEADING_1),
      p(`1.1. Trata-se do Relatório de Avaliação dos serviços prestados pela empresa ${id.contratada || "[preencher]"}, `
        + "nas dependências do CHU-UFPA, visando aferir a qualidade dos serviços executados, bem como determinar os "
        + "respectivos efeitos remuneratórios, em conformidade com o Termo de Referência da contratação."),

      heading("2. INSTRUMENTO DE MEDIÇÃO DE RESULTADOS - IMR", HeadingLevel.HEADING_1),
      p("2.1. Os pagamentos serão realizados mensalmente em conformidade com os serviços efetivamente prestados, "
        + "mediante aferição quantitativa e avaliação qualitativa das execuções. Serão avaliados os seguintes indicadores:"),
      p("2.1.1. Indicador 1 – Efetividade de atendimento (rendimento corretivo);"),
      p("2.1.2. Indicador 2 – Performance de Manutenção Programada;"),
      p("2.1.3. Indicador 3 - Disponibilidade dos Serviços Contratados;"),

      tabelaInd1, p(""), tabelaInd2, p(""), tabelaInd3, p(""),

      heading("3. RESULTADOS", HeadingLevel.HEADING_1),
      ...resultado31, ...resultado32, ...resultado33,

      ...secao4,

      heading("5. RECOMENDAÇÃO", HeadingLevel.HEADING_1),
      p("5.1. É importante registrar que qualquer situação que exceda a rotina, tais como trabalho em dias de "
        + "folga, compensação de faltas, substituição de colaborador, mudança de horário de trabalho e outras "
        + "situações relevantes, deve ser registrada previamente junto à fiscalização do contrato."),

      ...secao6,

      p(""), p("Atenciosamente,"),
      p(`Referência: Processo nº ${id.processo_sei || "[preencher]"}`),

      ...anexoFaltas,
    ],
  }],
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(outPath, buffer);
  console.error(`OK -> ${outPath}`);
});
