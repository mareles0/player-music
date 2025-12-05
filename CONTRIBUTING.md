# 🤝 Contribuindo para o Music Player

Obrigado por considerar contribuir com o projeto! Este guia ajudará você a começar.

## 📋 Diretrizes Gerais

### Como Contribuir

1. **Fork o repositório**
2. **Clone seu fork**
   ```bash
   git clone https://github.com/seu-usuario/player-music.git
   cd player-music
   ```

3. **Crie uma branch para sua feature**
   ```bash
   git checkout -b feature/minha-feature
   ```

4. **Faça suas alterações**
   - Mantenha o código limpo e documentado
   - Siga o estilo existente
   - Adicione docstrings em português

5. **Teste suas alterações**
   ```bash
   python main.py
   ```

6. **Commit suas mudanças**
   ```bash
   git add .
   git commit -m "feat: adiciona nova funcionalidade"
   ```

7. **Push para o GitHub**
   ```bash
   git push origin feature/minha-feature
   ```

8. **Abra um Pull Request**

## 🎯 Áreas para Contribuição

### 🐛 Reportar Bugs
- Use a aba **Issues** no GitHub
- Descreva o bug detalhadamente
- Inclua passos para reproduzir
- Mencione sua versão do Windows e Python

### ✨ Sugerir Funcionalidades
- Abra uma Issue com a tag `enhancement`
- Explique o caso de uso
- Descreva a solução proposta

### 📝 Melhorar Documentação
- README, comentários no código
- Exemplos de uso
- Tutoriais

### 🔧 Áreas Prioritárias
- [ ] Equalizer de áudio
- [ ] Visualizador de ondas
- [ ] Importação de playlists M3U
- [ ] Suporte a mais formatos (AIFF, APE)
- [ ] Lyrics integrados
- [ ] Testes automatizados

## 📐 Padrões de Código

### Python
- Use **4 espaços** para indentação
- Siga **PEP 8**
- Docstrings em **português**
- Type hints onde apropriado

### Commits
Use o padrão **Conventional Commits**:
- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Documentação
- `style:` - Formatação
- `refactor:` - Refatoração
- `test:` - Testes
- `chore:` - Manutenção

**Exemplos:**
```
feat: adiciona busca por artista
fix: corrige erro ao pausar música
docs: atualiza README com novos atalhos
```

## 🧪 Testes

Antes de enviar seu PR, teste:
- ✅ O player inicia sem erros
- ✅ Todas as funcionalidades funcionam
- ✅ Não há erros no console
- ✅ O código está documentado

## 🔍 Revisão de Código

Seu PR será revisado considerando:
- **Funcionalidade** - Resolve o problema?
- **Qualidade** - Código limpo e legível?
- **Documentação** - Bem documentado?
- **Compatibilidade** - Não quebra código existente?

## ❓ Dúvidas?

- Abra uma Issue com a tag `question`
- Entre em contato via email (se disponível no perfil)

## 📜 Código de Conduta

- Seja respeitoso e profissional
- Aceite feedback construtivo
- Foco em melhorar o projeto
- Sem discriminação ou assédio

---

**Obrigado por contribuir! 🎵**
