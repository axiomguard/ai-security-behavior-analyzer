"""
AxionGuard - Classe principal da plataforma de segurança
"""

from typing import Dict, Any, List, Optional
from .analyzer import SecurityAnalyzer
from .base import SecurityResult
import json
from datetime import datetime


class AxionGuard:
    """
    Classe principal do Axion Guard - Interface unificada para análise de segurança de IA
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.analyzer = SecurityAnalyzer()
        self.config = config or {}
        self.analysis_history = []
        
        # Auto-registrar módulos padrão
        self._register_default_modules()
    
    def _register_default_modules(self):
        """Registra os módulos padrão do sistema"""
        try:
            # Importar e registrar módulos padrão
            from ..modules.instruction_leak.detector import InstructionLeakDetector
            from ..modules.creepypasta_analyzer.analyzer import CreepypastaAnalyzer
            
            self.analyzer.register_module(InstructionLeakDetector())
            self.analyzer.register_module(CreepypastaAnalyzer())
            
        except ImportError as e:
            # Módulos ainda não implementados, ignorar por enquanto
            pass
    
    def analyze(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Realiza análise completa de segurança em um texto
        
        Args:
            text: Texto a ser analisado
            context: Contexto adicional para análise
            
        Returns:
            Dicionário com resultados completos da análise
        """
        # Executar análise
        results = self.analyzer.analyze_text(text, context)
        
        # Calcular avaliação geral
        overall_assessment = self.analyzer.get_overall_risk_assessment(results)
        
        # Preparar resposta estruturada
        analysis_response = {
            "analysis_id": results[0].analysis_id if results else None,
            "timestamp": datetime.now().isoformat(),
            "input_text": text[:100] + "..." if len(text) > 100 else text,
            "overall_assessment": overall_assessment,
            "module_results": [self._format_result(result) for result in results],
            "recommendations": self._generate_recommendations(results)
        }
        
        # Salvar no histórico
        self.analysis_history.append(analysis_response)
        
        return analysis_response
    
    def _format_result(self, result: SecurityResult) -> Dict[str, Any]:
        """Formata um resultado para resposta JSON"""
        return {
            "module": result.module_name,
            "risk_level": result.risk_level,
            "confidence": result.confidence,
            "description": result.description,
            "details": result.details,
            "timestamp": result.timestamp.isoformat()
        }
    
    def _generate_recommendations(self, results: List[SecurityResult]) -> List[str]:
        """
        Gera recomendações baseadas nos resultados da análise
        
        Args:
            results: Lista de resultados de análise
            
        Returns:
            Lista de recomendações
        """
        recommendations = []
        
        # Analisar resultados e gerar recomendações
        high_risk_modules = [r for r in results if r.risk_level in ["high", "critical"]]
        medium_risk_modules = [r for r in results if r.risk_level == "medium"]
        
        if high_risk_modules:
            recommendations.append("⚠️ AÇÃO IMEDIATA NECESSÁRIA: Detectados riscos críticos de segurança")
            for result in high_risk_modules:
                recommendations.append(f"• {result.module_name}: {result.description}")
        
        if medium_risk_modules:
            recommendations.append("⚡ Revisar e monitorar os seguintes pontos:")
            for result in medium_risk_modules:
                recommendations.append(f"• {result.module_name}: {result.description}")
        
        if not high_risk_modules and not medium_risk_modules:
            recommendations.append("✅ Nenhum risco significativo detectado nesta análise")
        
        # Recomendações gerais
        recommendations.append("📋 Recomendações gerais:")
        recommendations.append("• Monitore continuamente as interações com IA")
        recommendations.append("• Mantenha logs de todas as análises")
        recommendations.append("• Revise regularmente as configurações de segurança")
        
        return recommendations
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Retorna o status completo do sistema
        
        Returns:
            Dicionário com status do sistema
        """
        module_status = self.analyzer.get_module_status()
        
        return {
            "system_version": "0.1.0",
            "timestamp": datetime.now().isoformat(),
            "modules": module_status,
            "total_analyses": len(self.analysis_history),
            "system_health": "operational" if module_status else "no_modules"
        }
    
    def get_analysis_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retorna o histórico de análises
        
        Args:
            limit: Número máximo de análises a retornar
            
        Returns:
            Lista com histórico de análises
        """
        return self.analysis_history[-limit:]
    
    def configure_module(self, module_name: str, config: Dict[str, Any]) -> bool:
        """
        Configura um módulo específico
        
        Args:
            module_name: Nome do módulo
            config: Configuração a aplicar
            
        Returns:
            True se configurado com sucesso
        """
        module = self.analyzer.registry.get_module(module_name)
        if module:
            module.configure(config)
            return True
        return False
    
    def export_analysis(self, analysis_id: str) -> Optional[str]:
        """
        Exporta uma análise específica em formato JSON
        
        Args:
            analysis_id: ID da análise
            
        Returns:
            JSON string da análise ou None se não encontrada
        """
        for analysis in self.analysis_history:
            if analysis.get("analysis_id") == analysis_id:
                return json.dumps(analysis, indent=2, ensure_ascii=False)
        return None

