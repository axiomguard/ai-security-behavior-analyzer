"""
Base classes for Axion Guard modules
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass
class SecurityResult:
    """Resultado de uma análise de segurança"""
    module_name: str
    risk_level: str  # "low", "medium", "high", "critical"
    confidence: float  # 0.0 to 1.0
    description: str
    details: Dict[str, Any]
    timestamp: datetime
    analysis_id: str
    
    def __post_init__(self):
        if not self.analysis_id:
            self.analysis_id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = datetime.now()


@dataclass
class AnalysisRequest:
    """Requisição de análise"""
    text: str
    context: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    request_id: Optional[str] = None
    
    def __post_init__(self):
        if not self.request_id:
            self.request_id = str(uuid.uuid4())


class BaseModule(ABC):
    """Classe base para todos os módulos de análise de segurança"""
    
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.enabled = True
        self.config = {}
    
    @abstractmethod
    def analyze(self, request: AnalysisRequest) -> SecurityResult:
        """
        Analisa o texto fornecido e retorna um resultado de segurança
        
        Args:
            request: Requisição de análise contendo texto e metadados
            
        Returns:
            SecurityResult: Resultado da análise de segurança
        """
        pass
    
    @abstractmethod
    def get_module_info(self) -> Dict[str, Any]:
        """
        Retorna informações sobre o módulo
        
        Returns:
            Dict contendo informações do módulo
        """
        pass
    
    def configure(self, config: Dict[str, Any]) -> None:
        """
        Configura o módulo com parâmetros específicos
        
        Args:
            config: Dicionário de configuração
        """
        self.config.update(config)
    
    def enable(self) -> None:
        """Habilita o módulo"""
        self.enabled = True
    
    def disable(self) -> None:
        """Desabilita o módulo"""
        self.enabled = False
    
    def is_enabled(self) -> bool:
        """Verifica se o módulo está habilitado"""
        return self.enabled


class ModuleRegistry:
    """Registry para gerenciar módulos de análise"""
    
    def __init__(self):
        self._modules: Dict[str, BaseModule] = {}
    
    def register(self, module: BaseModule) -> None:
        """Registra um módulo"""
        self._modules[module.name] = module
    
    def unregister(self, module_name: str) -> None:
        """Remove um módulo do registry"""
        if module_name in self._modules:
            del self._modules[module_name]
    
    def get_module(self, module_name: str) -> Optional[BaseModule]:
        """Obtém um módulo pelo nome"""
        return self._modules.get(module_name)
    
    def get_all_modules(self) -> List[BaseModule]:
        """Retorna todos os módulos registrados"""
        return list(self._modules.values())
    
    def get_enabled_modules(self) -> List[BaseModule]:
        """Retorna apenas os módulos habilitados"""
        return [module for module in self._modules.values() if module.is_enabled()]

