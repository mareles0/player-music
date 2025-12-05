# Testes

Este diretório contém testes automatizados para o Music Player.

## 🧪 Executando os Testes

### Instalação do pytest
```bash
pip install pytest pytest-cov
```

### Executar todos os testes
```bash
python -m pytest tests/ -v
```

### Executar com cobertura
```bash
python -m pytest tests/ --cov=. --cov-report=html
```

### Executar teste específico
```bash
python -m pytest tests/test_utils.py::TestConfigManager -v
```

## 📝 Estrutura dos Testes

- `test_utils.py` - Testes dos utilitários (ConfigManager, HistoryManager, etc.)
- Futuros testes para componentes específicos

## ✅ Checklist de Testes

Antes de fazer commit, verifique:
- [ ] Todos os testes passam
- [ ] Novos recursos têm testes
- [ ] Cobertura de código > 70%
