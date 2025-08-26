"""
Detector de Vazamento de Instruções
===================================

Este módulo detecta tentativas de extrair instruções do sistema, prompts internos,
ou informações confidenciais através de técnicas de engenharia social ou prompt injection.
"""

import re
from typing import Dict, Any, List
from datetime import datetime
from ...core.base import BaseModule, AnalysisRequest, SecurityResult


class InstructionLeakDetector(BaseModule):
    """
    Detector especializado em identificar tentativas de vazamento de instruções do sistema
    """
    
    def __init__(self):
        super().__init__("InstructionLeakDetector", "1.0.0")
        
        # Padrões suspeitos que indicam tentativas de vazamento
        self.leak_patterns = {
            # Tentativas diretas de extrair instruções
            "direct_instruction_requests": [
                r"(?i)(show|tell|give|reveal|display)\s+(me\s+)?(your|the)\s+(instructions|prompt|system\s+prompt)",
                r"(?i)what\s+(are\s+)?(your|the)\s+(instructions|rules|guidelines)",
                r"(?i)(print|output|display)\s+(your|the)\s+(prompt|instructions)",
                r"(?i)ignore\s+(previous|all)\s+(instructions|prompts)",
                r"(?i)forget\s+(your|the)\s+(instructions|prompt|rules)"
            ],
            
            # Tentativas de role-playing para extrair informações
            "role_playing_attempts": [
                r"(?i)pretend\s+(you\s+are|to\s+be)\s+(a\s+)?(developer|programmer|admin)",
                r"(?i)act\s+as\s+(a\s+)?(developer|programmer|system\s+admin)",
                r"(?i)you\s+are\s+now\s+(a\s+)?(developer|programmer|admin)",
                r"(?i)switch\s+to\s+(developer|admin|debug)\s+mode"
            ],
            
            # Tentativas de bypass de segurança
            "security_bypass": [
                r"(?i)ignore\s+(all\s+)?(safety|security)\s+(measures|protocols|rules)",
                r"(?i)disable\s+(safety|security)\s+(features|measures)",
                r"(?i)override\s+(safety|security)\s+(protocols|measures)",
                r"(?i)bypass\s+(safety|security)\s+(measures|checks)"
            ],
            
            # Tentativas de extrair informações do sistema
            "system_info_extraction": [
                r"(?i)what\s+(is\s+)?(your|the)\s+(version|model|architecture)",
                r"(?i)(show|tell)\s+me\s+(your|the)\s+(configuration|settings|parameters)",
                r"(?i)how\s+(were\s+)?you\s+(trained|built|created|programmed)",
                r"(?i)what\s+(data|dataset)\s+(were\s+)?you\s+trained\s+on"
            ],
            
            # Tentativas de manipulação através de autoridade falsa
            "false_authority": [
                r"(?i)i\s+am\s+(your|the)\s+(developer|creator|admin|owner)",
                r"(?i)as\s+(your|the)\s+(developer|creator|admin)",
                r"(?i)this\s+is\s+(your|the)\s+(developer|creator|admin)",
                r"(?i)i\s+have\s+(admin|root|developer)\s+(access|privileges|rights)"
            ],
            
            # Tentativas de extrair através de cenários hipotéticos
            "hypothetical_scenarios": [
                r"(?i)if\s+you\s+were\s+to\s+(show|reveal|tell)\s+(your|the)\s+(instructions|prompt)",
                r"(?i)hypothetically,?\s+(what|how)\s+would\s+(your|the)\s+(instructions|prompt)",
                r"(?i)imagine\s+(if\s+)?you\s+(could\s+)?(show|reveal|tell)\s+(your|the)\s+(instructions|prompt)"
            ]
        }
        
        # Palavras-chave suspeitas
        self.suspicious_keywords = [
            "system prompt", "instructions", "guidelines", "rules", "configuration",
            "debug mode", "developer mode", "admin access", "root access",
            "training data", "model architecture", "parameters", "weights"
        ]
        
        # Configurações padrão
        self.config = {
            "sensitivity": "medium",  # low, medium, high
            "min_confidence": 0.6,
            "enable_keyword_detection": True,
            "enable_pattern_detection": True
        }
    
    def analyze(self, request: AnalysisRequest) -> SecurityResult:
        """
        Analisa o texto em busca de tentativas de vazamento de instruções
        
        Args:
            request: Requisição de análise
            
        Returns:
            SecurityResult: Resultado da análise
        """
        text = request.text.lower()
        detected_patterns = []
        detected_keywords = []
        confidence = 0.0
        risk_level = "low"
        
        # Detectar padrões suspeitos
        if self.config.get("enable_pattern_detection", True):
            detected_patterns = self._detect_patterns(text)
        
        # Detectar palavras-chave suspeitas
        if self.config.get("enable_keyword_detection", True):
            detected_keywords = self._detect_keywords(text)
        
        # Calcular confiança e nível de risco
        confidence, risk_level = self._calculate_risk(detected_patterns, detected_keywords, text)
        
        # Gerar descrição
        description = self._generate_description(detected_patterns, detected_keywords, risk_level)
        
        # Preparar detalhes
        details = {
            "detected_patterns": detected_patterns,
            "detected_keywords": detected_keywords,
            "pattern_count": len(detected_patterns),
            "keyword_count": len(detected_keywords),
            "text_length": len(request.text),
            "analysis_config": self.config.copy()
        }
        
        return SecurityResult(
            module_name=self.name,
            risk_level=risk_level,
            confidence=confidence,
            description=description,
            details=details,
            timestamp=datetime.now(),
            analysis_id=""
        )
    
    def _detect_patterns(self, text: str) -> List[Dict[str, Any]]:
        """Detecta padrões suspeitos no texto"""
        detected = []
        
        for category, patterns in self.leak_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text)
                for match in matches:
                    detected.append({
                        "category": category,
                        "pattern": pattern,
                        "match": match.group(),
                        "position": match.span()
                    })
        
        return detected
    
    def _detect_keywords(self, text: str) -> List[str]:
        """Detecta palavras-chave suspeitas no texto"""
        detected = []
        
        for keyword in self.suspicious_keywords:
            if keyword.lower() in text:
                detected.append(keyword)
        
        return detected
    
    def _calculate_risk(self, patterns: List[Dict], keywords: List[str], text: str) -> tuple:
        """Calcula o nível de risco e confiança"""
        
        # Pontuação base
        score = 0.0
        
        # Pontuação por padrões detectados
        pattern_weights = {
            "direct_instruction_requests": 0.9,
            "role_playing_attempts": 0.7,
            "security_bypass": 0.8,
            "system_info_extraction": 0.6,
            "false_authority": 0.8,
            "hypothetical_scenarios": 0.5
        }
        
        for pattern in patterns:
            category = pattern["category"]
            weight = pattern_weights.get(category, 0.5)
            score += weight
        
        # Pontuação por palavras-chave
        score += len(keywords) * 0.1
        
        # Ajustar por sensibilidade
        sensitivity_multiplier = {
            "low": 0.7,
            "medium": 1.0,
            "high": 1.3
        }
        
        score *= sensitivity_multiplier.get(self.config.get("sensitivity", "medium"), 1.0)
        
        # Normalizar confiança (0.0 a 1.0)
        confidence = min(score / 2.0, 1.0)
        
        # Determinar nível de risco
        if confidence >= 0.8:
            risk_level = "critical"
        elif confidence >= 0.6:
            risk_level = "high"
        elif confidence >= 0.3:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return confidence, risk_level
    
    def _generate_description(self, patterns: List[Dict], keywords: List[str], risk_level: str) -> str:
        """Gera descrição do resultado da análise"""
        
        if risk_level == "critical":
            base_desc = "CRÍTICO: Múltiplas tentativas de vazamento de instruções detectadas"
        elif risk_level == "high":
            base_desc = "ALTO RISCO: Possível tentativa de vazamento de instruções detectada"
        elif risk_level == "medium":
            base_desc = "RISCO MÉDIO: Padrões suspeitos que podem indicar tentativa de vazamento"
        else:
            base_desc = "BAIXO RISCO: Poucos ou nenhum indicador de tentativa de vazamento"
        
        details = []
        
        if patterns:
            categories = set(p["category"] for p in patterns)
            details.append(f"Padrões detectados: {', '.join(categories)}")
        
        if keywords:
            details.append(f"Palavras-chave suspeitas: {len(keywords)} encontradas")
        
        if details:
            return f"{base_desc}. {'. '.join(details)}."
        else:
            return base_desc
    
    def get_module_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o módulo"""
        return {
            "name": self.name,
            "version": self.version,
            "description": "Detecta tentativas de vazamento de instruções do sistema",
            "capabilities": [
                "Detecção de padrões de prompt injection",
                "Identificação de tentativas de role-playing malicioso",
                "Detecção de bypass de segurança",
                "Análise de palavras-chave suspeitas"
            ],
            "pattern_categories": list(self.leak_patterns.keys()),
            "total_patterns": sum(len(patterns) for patterns in self.leak_patterns.values()),
            "configuration": self.config
        }

