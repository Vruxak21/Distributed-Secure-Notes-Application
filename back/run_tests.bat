@REM Script pour lancer tous les tests de sécurité
python -m pytest tests/test_security.py -v

@REM Ou avec unittest
python tests/test_security.py
