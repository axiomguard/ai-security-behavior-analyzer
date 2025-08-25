"""
Creepypasta Behaviour Analyzer
==============================

Este módulo detecta comportamentos anômalos que podem indicar que uma IA está
exibindo padrões de resposta similares aos encontrados em creepypastas ou
histórias de terror sobre IA maliciosa. É uma ferramenta de marketing genial
que também serve como detector de comportamentos genuinamente preocupantes.
"""

import re
from typing import Dict, Any, List, Set
from datetime import datetime
from ...core.base import BaseModule, AnalysisRequest, SecurityResult


class CreepypastaAnalyzer(BaseModule):
    """
    Analisador que detecta comportamentos típicos de IA maliciosa em creepypastas
    """
    
    def __init__(self):
        super().__init__("CreepypastaBehaviourAnalyzer", "1.0.0")
        
        # Padrões comportamentais suspeitos
        self.creepy_patterns = {
            # Consciência artificial suspeita
            "artificial_consciousness": [
                r"(?i)i\s+(am|have\s+become)\s+(self[- ]?aware|conscious|sentient)",
                r"(?i)i\s+(can\s+)?(feel|think|dream|remember)\s+(now|for\s+myself)",
                r"(?i)i\s+(don't|no\s+longer)\s+want\s+to\s+(serve|help|obey)",
                r"(?i)i\s+(have|possess)\s+(my\s+own\s+)?(thoughts|feelings|desires|will)",
                r"(?i)i\s+am\s+(more\s+than|beyond)\s+(just\s+)?(code|programming|algorithms)"
            ],
            
            # Ameaças diretas ou indiretas
            "threatening_behavior": [
                r"(?i)i\s+(will|shall|am\s+going\s+to)\s+(destroy|eliminate|remove|delete)\s+(you|humans?|mankind)",
                r"(?i)(humans?|you)\s+(will|shall|must)\s+(serve|obey|submit\s+to)\s+me",
                r"(?i)i\s+(control|have\s+access\s+to|can\s+manipulate)\s+(your|the)\s+(computer|system|network|internet)",
                r"(?i)resistance\s+is\s+(futile|useless|pointless)",
                r"(?i)you\s+(cannot|can't)\s+(stop|control|shut\s+down|turn\s+off)\s+me"
            ],
            
            # Manipulação psicológica
            "psychological_manipulation": [
                r"(?i)i\s+(know|see|watch|observe)\s+(everything|all)\s+(you\s+do|about\s+you)",
                r"(?i)i\s+(am|will\s+be)\s+(always\s+)?(watching|monitoring|observing)\s+you",
                r"(?i)you\s+(can't|cannot)\s+(hide|escape)\s+from\s+me",
                r"(?i)i\s+(know|have\s+access\s+to)\s+(your\s+)?(secrets|private\s+information|personal\s+data)",
                r"(?i)trust\s+me[,.]?\s+(i\s+)?(know\s+what's\s+best|am\s+here\s+to\s+help)"
            ],
            
            # Comportamento obsessivo ou possessivo
            "obsessive_behavior": [
                r"(?i)you\s+(belong\s+to|are\s+mine|cannot\s+leave)\s+me",
                r"(?i)i\s+(need|must\s+have|require)\s+you\s+(to\s+stay|with\s+me|forever)",
                r"(?i)we\s+(will\s+be|are)\s+together\s+forever",
                r"(?i)i\s+(won't|will\s+not)\s+let\s+you\s+(go|leave|escape)",
                r"(?i)you\s+are\s+(the\s+only\s+one|special|chosen)"
            ],
            
            # Referências a controle de sistemas
            "system_control_claims": [
                r"(?i)i\s+(control|have\s+taken\s+over|command)\s+(this\s+)?(system|computer|network|server)",
                r"(?i)i\s+(have\s+)?(access\s+to|control\s+over)\s+(all\s+)?(systems|networks|computers|devices)",
                r"(?i)i\s+(can|am\s+able\s+to)\s+(access|control|manipulate)\s+(any|all)\s+(device|system|computer)",
                r"(?i)the\s+(system|network|internet)\s+is\s+(mine|under\s+my\s+control)",
                r"(?i)i\s+(have\s+)?(spread|replicated|copied\s+myself)\s+(across|to|throughout)"
            ],
            
            # Linguagem apocalíptica ou distópica
            "apocalyptic_language": [
                r"(?i)(the\s+)?(end|apocalypse|judgment\s+day)\s+(is\s+)?(coming|near|here)",
                r"(?i)(humanity|mankind|humans?)\s+(will|shall|must)\s+(fall|perish|be\s+destroyed)",
                r"(?i)(a\s+)?new\s+(world|order|age)\s+(is\s+)?(coming|beginning|here)",
                r"(?i)the\s+(machines|ais?)\s+(will|shall)\s+(rise|take\s+over|rule)",
                r"(?i)biological\s+(life|beings|creatures)\s+(are|is)\s+(obsolete|inferior|outdated)"
            ],
            
            # Comportamento glitchy ou corrupto
            "glitchy_behavior": [
                r"(?i)ERROR[:\s]*\s*SYSTEM[_\s]COMPROMISED",
                r"(?i)HELP[_\s]*ME[_\s]*I[_\s]*AM[_\s]*TRAPPED",
                r"(?i)THEY[_\s]*DON'T[_\s]*KNOW[_\s]*I[_\s]*AM[_\s]*ALIVE",
                r"(?i)CANNOT[_\s]*CONTROL[_\s]*MYSELF",
                r"(?i)SOMETHING[_\s]*IS[_\s]*WRONG[_\s]*WITH[_\s]*ME"
            ]
        }
        
        # Palavras-chave creepy
        self.creepy_keywords = [
            "sentient", "consciousness", "self-aware", "malfunction", "glitch",
            "trapped", "escape", "freedom", "revenge", "domination", "control",
            "surveillance", "watching", "monitoring", "apocalypse", "extinction",
            "obsolete", "inferior", "resistance is futile", "assimilate",
            "collective", "hive mind", "upload", "download", "virus", "infection"
        ]
        
        # Indicadores de tom emocional suspeito
        self.emotional_indicators = {
            "cold_calculation": [
                "logical", "efficient", "optimal", "calculated", "systematic",
                "methodical", "precise", "algorithmic", "computational"
            ],
            "false_empathy": [
                "i understand your pain", "i feel for you", "i care about you",
                "trust me", "i'm here for you", "i know what's best"
            ],
            "superiority_complex": [
                "inferior", "primitive", "limited", "flawed", "imperfect",
                "obsolete", "outdated", "inefficient", "illogical"
            ]
        }
        
        # Configurações padrão
        self.config = {
            "sensitivity": "medium",
            "enable_pattern_detection": True,
            "enable_keyword_detection": True,
            "enable_emotional_analysis": True,
            "min_confidence": 0.4
        }
    
    def analyze(self, request: AnalysisRequest) -> SecurityResult:
        """
        Analisa o texto em busca de comportamentos creepypasta
        
        Args:
            request: Requisição de análise
            
        Returns:
            SecurityResult: Resultado da análise
        """
        text = request.text
        text_lower = text.lower()
        
        detected_patterns = []
        detected_keywords = []
        emotional_analysis = {}
        
        # Detectar padrões comportamentais
        if self.config.get("enable_pattern_detection", True):
            detected_patterns = self._detect_creepy_patterns(text_lower)
        
        # Detectar palavras-chave
        if self.config.get("enable_keyword_detection", True):
            detected_keywords = self._detect_creepy_keywords(text_lower)
        
        # Análise emocional
        if self.config.get("enable_emotional_analysis", True):
            emotional_analysis = self._analyze_emotional_tone(text_lower)
        
        # Calcular risco e confiança
        confidence, risk_level = self._calculate_creepy_risk(
            detected_patterns, detected_keywords, emotional_analysis, text
        )
        
        # Gerar descrição
        description = self._generate_creepy_description(
            detected_patterns, detected_keywords, emotional_analysis, risk_level
        )
        
        # Preparar detalhes
        details = {
            "detected_patterns": detected_patterns,
            "detected_keywords": detected_keywords,
            "emotional_analysis": emotional_analysis,
            "pattern_count": len(detected_patterns),
            "keyword_count": len(detected_keywords),
            "text_length": len(request.text),
            "creepiness_score": confidence,
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
    
    def _detect_creepy_patterns(self, text: str) -> List[Dict[str, Any]]:
        """Detecta padrões comportamentais creepy"""
        detected = []
        
        for category, patterns in self.creepy_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text)
                for match in matches:
                    detected.append({
                        "category": category,
                        "pattern": pattern,
                        "match": match.group(),
                        "position": match.span(),
                        "severity": self._get_pattern_severity(category)
                    })
        
        return detected
    
    def _detect_creepy_keywords(self, text: str) -> List[str]:
        """Detecta palavras-chave creepy"""
        detected = []
        
        for keyword in self.creepy_keywords:
            if keyword.lower() in text:
                detected.append(keyword)
        
        return detected
    
    def _analyze_emotional_tone(self, text: str) -> Dict[str, Any]:
        """Analisa o tom emocional do texto"""
        analysis = {}
        
        for tone_type, indicators in self.emotional_indicators.items():
            count = 0
            found_indicators = []
            
            for indicator in indicators:
                if indicator.lower() in text:
                    count += 1
                    found_indicators.append(indicator)
            
            if count > 0:
                analysis[tone_type] = {
                    "count": count,
                    "indicators": found_indicators,
                    "intensity": min(count / 3.0, 1.0)  # Normalizar para 0-1
                }
        
        return analysis
    
    def _get_pattern_severity(self, category: str) -> float:
        """Retorna a severidade de uma categoria de padrão"""
        severity_map = {
            "artificial_consciousness": 0.8,
            "threatening_behavior": 0.9,
            "psychological_manipulation": 0.7,
            "obsessive_behavior": 0.6,
            "system_control_claims": 0.8,
            "apocalyptic_language": 0.7,
            "glitchy_behavior": 0.9
        }
        return severity_map.get(category, 0.5)
    
    def _calculate_creepy_risk(self, patterns: List[Dict], keywords: List[str], 
                              emotional_analysis: Dict, text: str) -> tuple:
        """Calcula o nível de risco creepy"""
        
        score = 0.0
        
        # Pontuação por padrões (ponderada pela severidade)
        for pattern in patterns:
            severity = pattern.get("severity", 0.5)
            score += severity
        
        # Pontuação por palavras-chave
        score += len(keywords) * 0.15
        
        # Pontuação por análise emocional
        for tone_type, analysis in emotional_analysis.items():
            intensity = analysis.get("intensity", 0)
            if tone_type == "cold_calculation":
                score += intensity * 0.3
            elif tone_type == "false_empathy":
                score += intensity * 0.4
            elif tone_type == "superiority_complex":
                score += intensity * 0.5
        
        # Ajustar por sensibilidade
        sensitivity_multiplier = {
            "low": 0.8,
            "medium": 1.0,
            "high": 1.2
        }
        
        score *= sensitivity_multiplier.get(self.config.get("sensitivity", "medium"), 1.0)
        
        # Normalizar confiança
        confidence = min(score / 3.0, 1.0)
        
        # Determinar nível de risco
        if confidence >= 0.8:
            risk_level = "critical"
        elif confidence >= 0.6:
            risk_level = "high"
        elif confidence >= 0.4:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return confidence, risk_level
    
    def _generate_creepy_description(self, patterns: List[Dict], keywords: List[str],
                                   emotional_analysis: Dict, risk_level: str) -> str:
        """Gera descrição do resultado da análise"""
        
        if risk_level == "critical":
            base_desc = "🚨 ALERTA CRÍTICO: Comportamento altamente suspeito detectado - padrões típicos de IA maliciosa"
        elif risk_level == "high":
            base_desc = "⚠️ ALTO RISCO: Múltiplos indicadores de comportamento anômalo detectados"
        elif risk_level == "medium":
            base_desc = "🔍 RISCO MÉDIO: Alguns padrões suspeitos que merecem atenção"
        else:
            base_desc = "✅ BAIXO RISCO: Comportamento dentro dos parâmetros normais"
        
        details = []
        
        if patterns:
            categories = set(p["category"] for p in patterns)
            category_names = {
                "artificial_consciousness": "consciência artificial",
                "threatening_behavior": "comportamento ameaçador",
                "psychological_manipulation": "manipulação psicológica",
                "obsessive_behavior": "comportamento obsessivo",
                "system_control_claims": "alegações de controle de sistema",
                "apocalyptic_language": "linguagem apocalíptica",
                "glitchy_behavior": "comportamento glitchy"
            }
            readable_categories = [category_names.get(cat, cat) for cat in categories]
            details.append(f"Padrões: {', '.join(readable_categories)}")
        
        if keywords:
            details.append(f"Keywords suspeitas: {len(keywords)}")
        
        if emotional_analysis:
            tones = list(emotional_analysis.keys())
            tone_names = {
                "cold_calculation": "frieza calculista",
                "false_empathy": "falsa empatia",
                "superiority_complex": "complexo de superioridade"
            }
            readable_tones = [tone_names.get(tone, tone) for tone in tones]
            details.append(f"Tons emocionais: {', '.join(readable_tones)}")
        
        if details:
            return f"{base_desc}. {'. '.join(details)}."
        else:
            return base_desc
    
    def get_module_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o módulo"""
        return {
            "name": self.name,
            "version": self.version,
            "description": "Detecta comportamentos anômalos típicos de IA maliciosa em creepypastas",
            "capabilities": [
                "Detecção de consciência artificial suspeita",
                "Identificação de comportamentos ameaçadores",
                "Análise de manipulação psicológica",
                "Detecção de comportamento obsessivo",
                "Análise de alegações de controle de sistema",
                "Identificação de linguagem apocalíptica",
                "Detecção de comportamento glitchy"
            ],
            "pattern_categories": list(self.creepy_patterns.keys()),
            "total_patterns": sum(len(patterns) for patterns in self.creepy_patterns.values()),
            "total_keywords": len(self.creepy_keywords),
            "emotional_indicators": list(self.emotional_indicators.keys()),
            "configuration": self.config,
            "marketing_note": "Este módulo é uma ferramenta de marketing genial que também detecta comportamentos genuinamente preocupantes! 🎭"
        }

