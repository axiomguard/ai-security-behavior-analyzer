"""
Axion Guard API - Flask Application
===================================

API REST para a plataforma de segurança Axion Guard
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import logging
import traceback

from ..core.guard import AxionGuard


def create_app(config=None):
    """
    Factory function para criar a aplicação Flask
    
    Args:
        config: Dicionário de configuração opcional
        
    Returns:
        Flask app configurada
    """
    app = Flask(__name__)
    
    # Configuração CORS para permitir acesso de qualquer origem
    CORS(app, origins="*")
    
    # Configuração de logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Instância global do Axion Guard
    guard = AxionGuard(config)
    
    @app.route('/', methods=['GET'])
    def home():
        """Endpoint raiz - informações da API"""
        return jsonify({
            "name": "Axion Guard API",
            "version": "1.0.0",
            "description": "API de segurança e governança para sistemas de IA",
            "status": "operational",
            "timestamp": datetime.now().isoformat(),
            "endpoints": {
                "GET /": "Informações da API",
                "POST /analyze": "Analisar texto",
                "GET /status": "Status do sistema",
                "GET /modules": "Listar módulos",
                "POST /modules/{name}/configure": "Configurar módulo",
                "POST /modules/{name}/enable": "Habilitar módulo",
                "POST /modules/{name}/disable": "Desabilitar módulo",
                "GET /history": "Histórico de análises",
                "GET /analysis/{id}": "Obter análise específica",
                "GET /health": "Health check"
            }
        })
    
    @app.route('/analyze', methods=['POST'])
    def analyze_text():
        """
        Endpoint principal para análise de texto
        
        Body JSON:
        {
            "text": "Texto a ser analisado",
            "context": {"key": "value"} // opcional
        }
        """
        try:
            data = request.get_json()
            
            if not data or 'text' not in data:
                return jsonify({
                    "error": "Campo 'text' é obrigatório",
                    "status": "error"
                }), 400
            
            text = data['text']
            context = data.get('context', {})
            
            if not text.strip():
                return jsonify({
                    "error": "Texto não pode estar vazio",
                    "status": "error"
                }), 400
            
            # Executar análise
            result = guard.analyze(text, context)
            
            # Adicionar metadados da API
            result['api_version'] = '1.0.0'
            result['status'] = 'success'
            
            logger.info(f"Análise realizada - Risco: {result['overall_assessment']['overall_risk']}")
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Erro na análise: {str(e)}")
            logger.error(traceback.format_exc())
            
            return jsonify({
                "error": "Erro interno do servidor",
                "message": str(e),
                "status": "error",
                "timestamp": datetime.now().isoformat()
            }), 500
    
    @app.route('/status', methods=['GET'])
    def system_status():
        """Endpoint para status do sistema"""
        try:
            status = guard.get_system_status()
            status['api_version'] = '1.0.0'
            status['status'] = 'success'
            
            return jsonify(status)
            
        except Exception as e:
            logger.error(f"Erro ao obter status: {str(e)}")
            
            return jsonify({
                "error": "Erro ao obter status do sistema",
                "message": str(e),
                "status": "error"
            }), 500
    
    @app.route('/modules', methods=['GET'])
    def list_modules():
        """Lista todos os módulos disponíveis"""
        try:
            modules = guard.analyzer.get_module_status()
            
            return jsonify({
                "modules": modules,
                "total_modules": len(modules),
                "status": "success",
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Erro ao listar módulos: {str(e)}")
            
            return jsonify({
                "error": "Erro ao listar módulos",
                "message": str(e),
                "status": "error"
            }), 500
    
    @app.route('/modules/<module_name>/configure', methods=['POST'])
    def configure_module(module_name):
        """Configura um módulo específico"""
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({
                    "error": "Configuração é obrigatória",
                    "status": "error"
                }), 400
            
            success = guard.configure_module(module_name, data)
            
            if success:
                return jsonify({
                    "message": f"Módulo {module_name} configurado com sucesso",
                    "status": "success"
                })
            else:
                return jsonify({
                    "error": f"Módulo {module_name} não encontrado",
                    "status": "error"
                }), 404
                
        except Exception as e:
            logger.error(f"Erro ao configurar módulo {module_name}: {str(e)}")
            
            return jsonify({
                "error": "Erro ao configurar módulo",
                "message": str(e),
                "status": "error"
            }), 500
    
    @app.route('/modules/<module_name>/enable', methods=['POST'])
    def enable_module(module_name):
        """Habilita um módulo específico"""
        try:
            success = guard.analyzer.enable_module(module_name)
            
            if success:
                return jsonify({
                    "message": f"Módulo {module_name} habilitado com sucesso",
                    "status": "success"
                })
            else:
                return jsonify({
                    "error": f"Módulo {module_name} não encontrado",
                    "status": "error"
                }), 404
                
        except Exception as e:
            logger.error(f"Erro ao habilitar módulo {module_name}: {str(e)}")
            
            return jsonify({
                "error": "Erro ao habilitar módulo",
                "message": str(e),
                "status": "error"
            }), 500
    
    @app.route('/modules/<module_name>/disable', methods=['POST'])
    def disable_module(module_name):
        """Desabilita um módulo específico"""
        try:
            success = guard.analyzer.disable_module(module_name)
            
            if success:
                return jsonify({
                    "message": f"Módulo {module_name} desabilitado com sucesso",
                    "status": "success"
                })
            else:
                return jsonify({
                    "error": f"Módulo {module_name} não encontrado",
                    "status": "error"
                }), 404
                
        except Exception as e:
            logger.error(f"Erro ao desabilitar módulo {module_name}: {str(e)}")
            
            return jsonify({
                "error": "Erro ao desabilitar módulo",
                "message": str(e),
                "status": "error"
            }), 500
    
    @app.route('/history', methods=['GET'])
    def analysis_history():
        """Retorna histórico de análises"""
        try:
            limit = request.args.get('limit', 10, type=int)
            limit = min(limit, 100)  # Máximo de 100 análises
            
            history = guard.get_analysis_history(limit)
            
            return jsonify({
                "history": history,
                "total_returned": len(history),
                "limit": limit,
                "status": "success",
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Erro ao obter histórico: {str(e)}")
            
            return jsonify({
                "error": "Erro ao obter histórico",
                "message": str(e),
                "status": "error"
            }), 500
    
    @app.route('/analysis/<analysis_id>', methods=['GET'])
    def get_analysis(analysis_id):
        """Obtém uma análise específica por ID"""
        try:
            analysis = guard.export_analysis(analysis_id)
            
            if analysis:
                import json
                return jsonify({
                    "analysis": json.loads(analysis),
                    "status": "success"
                })
            else:
                return jsonify({
                    "error": f"Análise {analysis_id} não encontrada",
                    "status": "error"
                }), 404
                
        except Exception as e:
            logger.error(f"Erro ao obter análise {analysis_id}: {str(e)}")
            
            return jsonify({
                "error": "Erro ao obter análise",
                "message": str(e),
                "status": "error"
            }), 500
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        try:
            status = guard.get_system_status()
            
            return jsonify({
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "modules_active": len([m for m in status['modules'] if m['enabled']]),
                "system_health": status['system_health']
            })
            
        except Exception as e:
            logger.error(f"Erro no health check: {str(e)}")
            
            return jsonify({
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }), 500
    
    @app.errorhandler(404)
    def not_found(error):
        """Handler para 404"""
        return jsonify({
            "error": "Endpoint não encontrado",
            "status": "error",
            "timestamp": datetime.now().isoformat()
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handler para 405"""
        return jsonify({
            "error": "Método não permitido",
            "status": "error",
            "timestamp": datetime.now().isoformat()
        }), 405
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

