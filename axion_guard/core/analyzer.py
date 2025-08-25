"""
Security Analyzer - Motor principal de análise de segurança
"""

from typing import List, Dict, Any, Optional
from .base import BaseModule, AnalysisRequest, SecurityResult, ModuleRegistry
import logging
from datetime import datetime


class SecurityAnalyzer:
    """
    Analisador principal que coordena todos os módulos de segurança
    """
    
    def __init__(self):
        self.registry = ModuleRegistry()
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
    
    def _setup_logging(self):
        """Configura o sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def register_module(self, module: BaseModule) -> None:
        """
        Registra um novo módulo de análise
        
        Args:
            module: Módulo a ser registrado
        """
        self.registry.register(module)
        self.logger.info(f"Módulo {module.name} registrado com sucesso")
    
    def analyze_text(self, text: str, context: Optional[Dict[str, Any]] = None) -> List[SecurityResult]:
        """
        Analisa um texto usando todos os módulos habilitados
        
        Args:
            text: Texto a ser analisado
            context: Contexto adicional para a análise
            
        Returns:
            Lista de resultados de segurança de todos os módulos
        """
        request = AnalysisRequest(text=text, context=context)
        results = []
        
        enabled_modules = self.registry.get_enabled_modules()
        
        if not enabled_modules:
            self.logger.warning("Nenhum módulo habilitado para análise")
            return results
        
        self.logger.info(f"Iniciando análise com {len(enabled_modules)} módulos")
        
        for module in enabled_modules:
            try:
                self.logger.debug(f"Executando análise com módulo: {module.name}")
                result = module.analyze(request)
                results.append(result)
                self.logger.debug(f"Módulo {module.name} completou análise: {result.risk_level}")
            except Exception as e:
                self.logger.error(f"Erro no módulo {module.name}: {str(e)}")
                # Criar resultado de erro
                error_result = SecurityResult(
                    module_name=module.name,
                    risk_level="unknown",
                    confidence=0.0,
                    description=f"Erro durante análise: {str(e)}",
                    details={"error": str(e)},
                    timestamp=datetime.now(),
                    analysis_id=""
                )
                results.append(error_result)
        
        return results
    
    def get_overall_risk_assessment(self, results: List[SecurityResult]) -> Dict[str, Any]:
        """
        Calcula uma avaliação geral de risco baseada nos resultados
        
        Args:
            results: Lista de resultados de análise
            
        Returns:
            Dicionário com avaliação geral de risco
        """
        if not results:
            return {
                "overall_risk": "unknown",
                "confidence": 0.0,
                "summary": "Nenhuma análise realizada"
            }
        
        # Mapear níveis de risco para valores numéricos
        risk_values = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4,
            "unknown": 0
        }
        
        # Calcular risco médio ponderado pela confiança
        total_weighted_risk = 0
        total_confidence = 0
        
        for result in results:
            if result.risk_level in risk_values:
                weighted_risk = risk_values[result.risk_level] * result.confidence
                total_weighted_risk += weighted_risk
                total_confidence += result.confidence
        
        if total_confidence == 0:
            overall_risk = "unknown"
            avg_confidence = 0.0
        else:
            avg_risk_value = total_weighted_risk / total_confidence
            avg_confidence = total_confidence / len(results)
            
            # Converter de volta para categoria de risco
            if avg_risk_value >= 3.5:
                overall_risk = "critical"
            elif avg_risk_value >= 2.5:
                overall_risk = "high"
            elif avg_risk_value >= 1.5:
                overall_risk = "medium"
            else:
                overall_risk = "low"
        
        # Contar resultados por categoria
        risk_counts = {}
        for result in results:
            risk_counts[result.risk_level] = risk_counts.get(result.risk_level, 0) + 1
        
        return {
            "overall_risk": overall_risk,
            "confidence": avg_confidence,
            "risk_distribution": risk_counts,
            "total_modules": len(results),
            "summary": f"Análise de {len(results)} módulos - Risco geral: {overall_risk}"
        }
    
    def get_module_status(self) -> List[Dict[str, Any]]:
        """
        Retorna o status de todos os módulos registrados
        
        Returns:
            Lista com informações de status dos módulos
        """
        modules_status = []
        
        for module in self.registry.get_all_modules():
            status = {
                "name": module.name,
                "version": module.version,
                "enabled": module.is_enabled(),
                "info": module.get_module_info()
            }
            modules_status.append(status)
        
        return modules_status
    
    def enable_module(self, module_name: str) -> bool:
        """
        Habilita um módulo específico
        
        Args:
            module_name: Nome do módulo
            
        Returns:
            True se o módulo foi habilitado, False caso contrário
        """
        module = self.registry.get_module(module_name)
        if module:
            module.enable()
            self.logger.info(f"Módulo {module_name} habilitado")
            return True
        return False
    
    def disable_module(self, module_name: str) -> bool:
        """
        Desabilita um módulo específico
        
        Args:
            module_name: Nome do módulo
            
        Returns:
            True se o módulo foi desabilitado, False caso contrário
        """
        module = self.registry.get_module(module_name)
        if module:
            module.disable()
            self.logger.info(f"Módulo {module_name} desabilitado")
            return True
        return False

