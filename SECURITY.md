# 🔒 Política de Segurança

## 🐛 Reportando Vulnerabilidades

Se você descobrir uma vulnerabilidade de segurança no Music Player, por favor **NÃO** abra uma Issue pública.

### Como Reportar:
1. **Email**: Entre em contato diretamente via email (se disponível no perfil do desenvolvedor)
2. **GitHub Security Advisory**: Use a aba "Security" → "Report a vulnerability"
3. **Issue Privada**: Se necessário, abra uma Issue com detalhes mínimos

### O que Incluir:
- Descrição da vulnerabilidade
- Passos para reproduzir
- Versão afetada
- Impacto potencial
- Sugestão de correção (se houver)

## ✅ Versões Suportadas

| Versão | Suportada          |
| ------ | ------------------ |
| 1.x.x  | :white_check_mark: |
| < 1.0  | :x:                |

## 🛡️ Boas Práticas de Segurança

### Para Usuários:
- ✅ Baixe apenas da página oficial de Releases
- ✅ Verifique o hash SHA256 do executável (quando disponível)
- ❌ Não execute versões de fontes não confiáveis
- ✅ Mantenha o Windows Defender ativado

### Para Desenvolvedores:
- ✅ Sempre valide entrada de usuário
- ✅ Use try-catch em operações de arquivo
- ✅ Não armazene dados sensíveis em texto puro
- ✅ Mantenha dependências atualizadas

## 📋 Checklist de Segurança

- [x] Validação de caminhos de arquivo
- [x] Tratamento de exceções
- [x] Sem execução de código arbitrário
- [x] Dependências com versões fixas
- [ ] Assinatura digital do executável (planejado)
- [ ] Testes de segurança automatizados (planejado)

## 🔐 Privacidade

### Dados Coletados:
- **NENHUM** - O aplicativo não coleta telemetria
- **Local** - Todas as configurações são salvas localmente em `~/.music_player/`
- **Offline** - Funciona completamente offline

### Permissões:
- **Leitura de arquivos** - Apenas para carregar músicas
- **Escrita local** - Apenas em `~/.music_player/` para configurações
- **Rede** - **NÃO UTILIZA**

## 📞 Contato

Para questões de segurança urgentes, entre em contato:
- GitHub Security Advisory (recomendado)
- Email do mantenedor (se disponível)

---

**Obrigado por ajudar a manter o Music Player seguro! 🔒**
