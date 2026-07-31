# Controle de Gases Medicinais — Manual de Uso

Sistema desktop para controle de entrada e saída de materiais de gases
medicinais (fluxômetros, manômetros, reguladores de cilindro e
equipamentos correlatos), com estoque calculado automaticamente e
histórico auditável.

## 1. Como gerar o executável (.exe) no Windows

Por limitação deste ambiente de desenvolvimento (rodando em Linux, sem
acesso à internet externa para baixar o Python do Windows), o arquivo
`.exe` final precisa ser gerado **uma única vez**, rodando um script
pronto em um computador Windows do hospital. O PyInstaller sempre gera o
executável para o mesmo sistema operacional em que é executado — por isso
não é possível "cross-compilar" um `.exe` de dentro de um Linux sem
Windows real. É um processo rápido e não exige conhecimento técnico:

1. Instale o [Python 3.11 ou superior](https://www.python.org/downloads/)
   em qualquer computador Windows (marque a opção **"Add Python to
   PATH"** durante a instalação). Isso só precisa ser feito uma vez, no
   computador onde o `.exe` será gerado — os demais computadores do
   hospital **não** precisam ter Python instalado, só usam o `.exe`
   pronto.
2. Copie a pasta `gases_medicinais` (código-fonte) para esse computador.
3. Dê duplo clique no arquivo `build_windows.bat` dentro da pasta.
4. Aguarde a mensagem "Pronto!". O executável estará em
   `dist\ControleGasesMedicinais.exe`.
5. Copie esse `.exe` para os demais computadores que forem usar o
   programa (ele é um arquivo único, não precisa de instalador).

Junto com este pacote também é entregue um executável de demonstração já
testado em Linux (`dist/ControleGasesMedicinais_demo_linux`), usado
apenas para comprovar que o processo de empacotamento funciona
corretamente — para uso real no hospital, gere o `.exe` do Windows
seguindo os passos acima.

## 2. Primeira configuração: pasta compartilhada do banco de dados

Todo o sistema é um único arquivo de banco de dados
(`gases_medicinais.db`). Para que **todos os computadores** do setor
enxerguem os mesmos dados, esse arquivo precisa ficar em uma pasta de
rede acessível por todos (ex.: um HD de rede, ou uma pasta compartilhada
do servidor do hospital, mapeada como uma unidade de rede tipo `Z:\`).

**No primeiro computador (quem vai criar o banco):**
1. Abra o programa.
2. Vá até a aba **Configurações**.
3. Clique em **"Criar novo banco em uma pasta..."**.
4. Selecione a pasta de rede compartilhada (ex.: `Z:\Gases Medicinais`).
5. O programa cria o arquivo `gases_medicinais.db` dentro dela.

**Nos demais computadores:**
1. Abra o programa.
2. Vá até a aba **Configurações**.
3. Clique em **"Usar banco existente (arquivo .db)..."**.
4. Navegue até a mesma pasta de rede e selecione o arquivo
   `gases_medicinais.db` que já foi criado no passo anterior.

Use o botão **"Testar Conexão"** a qualquer momento para confirmar que o
computador está enxergando o banco de dados corretamente.

> **Importante:** se a pasta de rede ficar indisponível (computador
> desligado, cabo de rede solto, etc.), o programa avisa com uma mensagem
> amigável em vez de travar ou corromper dados. Basta reconectar a rede e
> tentar novamente, ou ajustar o caminho em Configurações.

## 3. Abas do sistema

### Estoque Atual
Mostra a quantidade atual de cada item, calculada automaticamente a
partir de todo o histórico de entradas e saídas. Itens com quantidade
abaixo do estoque mínimo definido aparecem destacados em vermelho.

### Nova Movimentação
Tela para registrar uma entrada ou saída de material:
- Escolha o tipo (Entrada ou Saída).
- Selecione o item e a quantidade.
- Informe quem solicitou/retirou o material.
- Informe o setor (destino, no caso de saída; origem/fornecedor, no caso
  de entrada).
- Número de série/patrimônio é opcional.
- Informe o responsável pelo registro (quem está digitando).
- Data e hora são preenchidas automaticamente.
- Ao clicar em "Registrar Movimentação", o estoque é atualizado na hora.

### Cadastro de Itens
Cadastre os equipamentos controlados (nome, categoria, unidade de
medida e estoque mínimo desejado). Itens podem ser editados ou
desativados (itens desativados saem das listas de nova movimentação, mas
o histórico deles é mantido para auditoria).

### Histórico
Lista todas as movimentações já registradas, com filtros por item, tipo
(entrada/saída), período (data inicial e final) e solicitante. Os
botões **Exportar CSV** e **Exportar Excel** salvam os registros
filtrados em arquivo, para fins de auditoria.

### Configurações
Permite ver e alterar o caminho do arquivo de banco de dados, conforme
explicado na seção 2 acima.

## 4. Perguntas frequentes

**Dois computadores podem usar ao mesmo tempo?**
Sim, desde que o uso não seja constante e simultâneo o tempo todo. Se
duas pessoas tentarem gravar no exato mesmo instante, o programa espera
alguns segundos automaticamente; se ainda assim não conseguir, mostra um
aviso pedindo para tentar novamente em instantes — sem corromper os
dados.

**Perdi a conexão com a pasta de rede no meio do uso, e agora?**
O programa mostra uma mensagem explicando que não conseguiu acessar o
banco de dados. Verifique a conexão de rede e tente novamente, ou use a
aba Configurações para apontar para outro local, se necessário.

**Como faço backup dos dados?**
Basta copiar o arquivo `gases_medicinais.db` da pasta configurada — ele
contém todo o histórico. Recomenda-se que a própria pasta de rede já
tenha uma rotina de backup do hospital.
