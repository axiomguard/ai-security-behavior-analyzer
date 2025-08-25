#!/usr/bin/env python3
"""
Script para executar a API do Axion Guard
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from axion_guard.api.app import create_app


def main():
    """Função principal para executar a API"""
    
    print("🛡️ Iniciando Axion Guard API...")
    print("=" * 40)
    
    # Criar aplicação
    app = create_app()
    
    print("✅ API configurada com sucesso!")
    print("🌐 Endpoints disponíveis:")
    print("  • GET  /           - Informações da API")
    print("  • POST /analyze    - Analisar texto")
    print("  • GET  /status     - Status do sistema")
    print("  • GET  /modules    - Listar módulos")
    print("  • GET  /history    - Histórico de análises")
    print("  • GET  /health     - Health check")
    print()
    print("🚀 Servidor rodando em: http://0.0.0.0:5000")
    print("📋 Para testar: curl http://localhost:5000/")
    print()
    
    # Executar servidor
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n🛑 Servidor interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao executar servidor: {e}")


if __name__ == '__main__':
    main()

