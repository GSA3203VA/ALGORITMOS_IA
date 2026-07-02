# Diretrizes para o Claude Code neste Repositório

1. **Restrição de Escopo:** 
Este é um repositório multi-projeto (Cursos e Tese). Nunca tente ler arquivos fora da pasta do subprojeto em que fomos inicializados.
2. **Proibição de Leitura de Dados:** 
Nunca use a ferramenta `FileRead` em arquivos dentro de pastas chamadas `dados_bruto` ou com extensões `csv` e `.dat`. 
3. **Uso de Amostras:** 
Se precisar entender a estrutura dos dados para corrigir ou criar scripts em `src`, leia única e exclusivamente os arquivos contidos na pasta `dados_amostra/` ou verifique os metadados na pasta `docs/`.
4. **Estilo de Código:** 
Dê preferência a scripts Python estruturados e limpos utilizando boas práticas de Machine Learning e manipulação de dados com Pandas.